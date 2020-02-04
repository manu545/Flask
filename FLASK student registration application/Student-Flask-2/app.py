from flask import Flask, render_template, redirect, url_for
from flask import flash
from flask import request
from wtforms.fields.html5 import DateField
from flask_admin.contrib.sqla import ModelView
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, validators
from werkzeug.security import generate_password_hash , check_password_hash
from wtforms import StringField, PasswordField, IntegerField, TextField, DateField
from wtforms.validators import InputRequired, email, length, optional, EqualTo, ValidationError, Regexp, NumberRange
from flask_admin import Admin
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#from tabledef import *
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin ,UserMixin
from flask_security.utils import encrypt_password,verify_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin.form import SecureForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_user import UserMixin

from flask_security.forms import LoginForm
from flask_security.forms import RegisterForm



app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECURITY_PASSWORD_SALT'] = 'BarryAllen'
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)
Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login1'

#admin = Admin(app, name='Student Registration App', template_mode='bootstrap3')
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

class User(UserMixin, db.Model):
   #print(UserMixin)
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(15), unique=True)
   email = db.Column(db.String(50), unique=True)
   password = db.Column(db.String(160))
   fname = db.Column(db.String(50))
   lname = db.Column(db.String(50))
   roll = db.Column(db.Integer)
   phone = db.Column(db.Integer)
   addr = db.Column(db.String(50))
   pin = db.Column(db.Integer)
   city = db.Column(db.String(50))
   birthdate = db.Column(db.Date)
   pname = db.Column(db.String(50))
   pnum = db.Column(db.Integer)
   active = db.Column(db.Boolean())
   roles = db.relationship('Role', secondary=roles_users,
                           backref=db.backref('users', lazy='dynamic'))

   def has_roles(self, *args):
       return set(args).issubset({role.name for role in self.roles})


def __init__(self, username, email, password, fname, lname, roll, phone, addr, pin, city, birthdate, pname, pnum,active):
    """"""
    self.username = username
    self.email = email
    self.password = password
    self.fname = fname
    self.lname = lname
    self.roll = roll
    self.phone = phone
    self.addr = addr
    self.pin = pin
    self.city = city
    self.birthdate = birthdate
    self.pname = pname
    self.pnum = pnum
    self.active=True




# add fields in parameters-------------------------------------------------



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

class MyModelView(sqla.ModelView):
    form_base_class = SecureForm
    column_searchable_list = ('username', 'email', 'fname', 'lname', 'roll', 'phone', 'addr', 'pin', 'city', 'birthdate', 'pname', 'pnum')

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    def on_model_change(self, form, User, is_created=False):
            d=form.password.data
            e=len(d)
            if(e<=30):
               password_hash = encrypt_password(form.password.data)
               User.password = password_hash
               #print('hiiiiiiiiii')




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm1(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), length(min=4, max=12)])
    password = PasswordField('Password',validators=[InputRequired(), length(min=8, max=160)])

class RegisterForm1(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), length(min=4, max=12)])
    email = StringField('Email',validators=[InputRequired(), email(message='Invalid E-mail'), length(max=50)])
    password = PasswordField('Password',validators=[InputRequired(), EqualTo('confirm', message='Passwords must match'), length(min=8, max=160)])
    confirm = PasswordField('Password(again)')

    def validate_username(self, field):
        # count the number of user ids for that username
        # if it's not 0, there's a user with that username already
        if db.session.query(db.func.count(User.id)).filter_by(username=field.data).scalar():
            raise ValidationError('This username is already taken')


    def validate_email(self, field):
    # count the number of user ids for that username
    # if it's not 0, there's a user with that username already
        if db.session.query(db.func.count(User.id)).filter_by(email=field.data).scalar():
            raise ValidationError('This e-mail is already taken')


class ProfileForm(FlaskForm):
    fname = StringField('First name',validators=[length(max=25), Regexp(r'^[A-Za-z]+$'), optional()])
    lname = StringField('Last name',validators=[length(max=25), Regexp(r'^[A-Za-z]+$'), optional()])
    roll = StringField('Roll Number',validators=[Regexp('^[1-8]{1}[0-9]{9}$'), optional()])
    phone = StringField('Phone Number', validators=[Regexp('^[2-9]{1}[0-9]{9}$'), optional()])
    addr = StringField('Address', validators=[length(max=50), optional()])
    pin = StringField('PIN Code', validators=[Regexp('^[1-8]{2}[0-9]{4}$'), optional()])
    city = StringField('City', validators=[length(max=25), Regexp(r'^[A-Za-z]+$'), optional()])
    birthdate = DateField('Birthday', format='%d/%m/%Y', validators=[optional()])
    pname = StringField('Parent Name', validators=[length(min=4, max=25), Regexp(r'^[A-Za-z]+$'), optional()])
    pnum = StringField('Parent Number', validators=[Regexp('^[2-9]{1}[0-9]{9}$'), optional()])


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('home.html', name=current_user.username)

    return render_template('test.html')

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('home.html',name=current_user)

@app.route("/signup", methods=['GET','POST'])
def signup():
 forme = RegisterForm1()

 if request.method == 'POST' and forme.validate_on_submit():
      pw_hash = encrypt_password(forme.password.data)
      new_user = User(username=forme.username.data, email=forme.email.data, password=pw_hash)
      db.session.add(new_user)
      db.session.commit()
      return redirect(url_for('thanks'))

 return render_template('signup.html',forme=forme)



@app.route('/login1',  methods=['GET','POST'])
def login1():
 forme = LoginForm1()
 d=e=""
 if request.method == 'POST' and forme.validate_on_submit():

     user = User.query.filter_by(username=forme.username.data).first()
     e=forme.password.data
     if user:
         d = user.password
         if verify_password(e,d):
             login_user(user)
             return render_template('home.html',name=current_user.username)
     flash('Invalid credentials')

 return render_template('login1.html', forme=forme,a=d,b=e )

@app.route('/thanks')
def thanks():
    return render_template('regsuc.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    d=current_user.username
    forme = ProfileForm(obj = current_user)
    if request.method == 'POST' and forme.validate_on_submit():
        forme.populate_obj(current_user)
        db.session.commit()
        return render_template('added.html',name=d)
    return render_template('profile.html', form=forme, name=d)


@app.route('/form')
def form():
    d=current_user.username
    engine = create_engine('sqlite:///database.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    fnamee = ""
    lnamee = ""
    email = ""
    pa=roll=addr=pin=city=bd=pnum=pname=""
    user = User.query.filter_by(username=d).first()
    if user:
        for name in session.query(User).filter(User.username == d):
            name2 = name.username
            pa = name.password
            email = name.email
            fnamee=name.fname
            lnamee=name.lname
            roll=name.roll
            phone=name.phone
            addr=name.addr
            pin=name.pin
            city=name.city
            bd=name.birthdate
            pname=name.pname
            pnum=name.pnum
            return render_template('view.html', name=name2, passw=pa, fna=fnamee, lna=lnamee, email=email, pnum=pnum,roll=roll,phone=phone,addr=addr,
                                   pin=pin,city=city,bd=bd,pname=pname)
    else:
             return render_template('check.html',name=current_user.username)


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            username='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

        db.session.commit()
    return




@app.route('/logout')
def logout():
    logout_user()
    return render_template('test.html')



admin = flask_admin.Admin(
    app,
    'Example: Auth',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
#admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))



if __name__ == '__main__':
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    #build_sample_db()
    app.debug = True
    app.run()
    app.run(debug=True)
