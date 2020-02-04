import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *


engine = create_engine('sqlite:///tutorial.db', echo=True)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()

user = User("1210", "venkatadri express","3","14:21 ")
session.add(user)

user = User("1122", "garibradh","4","10:42 ")
session.add(user)

#user = User("jumpiness", "python","a@gmail.com")
#session.add(user)

#user = User("test", "test","abcd@gmail.com")
#session.add(user)
# commit the record the database
#session.commit()

#teacher = Teacher("manohar","password")
#session.add(teacher)

#teacher = Teacher("manohar","manohar")
#session.add(teacher)

session.commit()

session.commit()