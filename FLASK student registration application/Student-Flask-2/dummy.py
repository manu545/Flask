import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///database.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

teacher = Teacher("admin", "password")
session.add(teacher)

teacher = Teacher("python", "python")
session.add(teacher)


# commit the record the database
session.commit()

session.commit()