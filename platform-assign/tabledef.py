from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///tutorial.db', echo=True)
Base = declarative_base()


########################################################################
class User(Base):
    """"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tnum = Column(String)
    tname = Column(String)
    platform = Column(String)
    time = Column(String)
    # add fields in parameters-------------------------------------------------
    def __init__(self, tnum, tname,platform,time):
        """"""
        self.tnum = tnum
        self.tname = tname
        self.platform = platform
        self.time=time
#  create tables
Base.metadata.create_all(engine)