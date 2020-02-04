from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from app import roles_users
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


########################################################################
class Teacher(UserMixin):
    """"""
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    email=Column(String)
    password = Column(String)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # add fields in parameters-------------------------------------------------
    def __init__(self, first_name,email, password,roles):
        """"""
        self.self = self
        self.first_name = first_name
        self.email=email
        self.password = password
        self.roles=roles

# create tables
Base.metadata.create_all(engine)