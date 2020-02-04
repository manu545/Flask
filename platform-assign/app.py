from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from flask import Flask,g
from sqlalchemy.orm import sessionmaker
from tabledef import *



engine = create_engine('sqlite:///tutorial.db', echo=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route('/')
def home():
        return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    engine = create_engine('sqlite:///tutorial.db', echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()
    POST_USERNAM = str(request.form['usern'])
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    tname=""
    tnum=""
    platform=""
    time=""
    query = s.query(User).filter(User.tnum.in_([POST_USERNAM]))
    result = query.first()
    if result:
        for instance in session.query(User).filter(User.tnum == POST_USERNAM):
            tname = instance.tname
            tnum = instance.tnum
            platform = instance.platform
            time=instance.time
            return render_template('open.html', tname=tname,tnum=tnum,platform=platform,time=time,ch=0)
    else:
        return render_template('search.html',ch=1)


@app.route('/login')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/log', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return redirect(url_for('open'))
    else:
        flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/add", methods=['POST'])
def register():
    POST_USER = str(request.form['tnum'])
    POST_PASS = str(request.form['tname'])
    POST_PASS1 = str(request.form['platform'])
    email = str(request.form['time'])
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.tnum.in_([POST_USER]))
    result = query.first()

    if result:
        return render_template('add.html', er=1)

    else:

            engine = create_engine('sqlite:///tutorial.db', echo=True)
            Sessions = sessionmaker(bind=engine)
            session = Sessions()

            user = User(POST_USER, POST_PASS,POST_PASS1, email)
            session.add(user)
            session.commit()
            session.commit()
            return redirect(url_for('open'))


@app.route("/view")
def open():
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    tnum=[]
    tname=[]
    platform=[]
    tm=[]


    for instance in session.query(User).order_by(User.id):
        #print(instance.name, instance.fullname)
       tnum.append(instance.tnum)
       tname.append(instance.tname)
       platform.append(instance.platform)
       tm.append(instance.time)

    k=len(tnum)
    return render_template('view.html', name=tnum,pa=tname,em=platform,tm=tm,k=k)

@app.route("/delete" ,methods=['POST'])
def delete():
    engine = create_engine('sqlite:///tutorial.db', echo=True)
    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()
    userde = str(request.form['delid'])



    for name in session.query(User).filter(User.tnum == userde):
        session.delete(name)
        session.commit()
    return redirect(url_for('open'))


@app.route('/addt')
def addt():
    return render_template('add.html')




if __name__ == "__main__":
   ''''' app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)'''''
   app.debug = True
   app.run()
   app.run(debug=True)