from datetime import datetime, timedelta
from random import randint

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *

users, projects = [], []

engine = create_engine('sqlite:///demo.db')



Session = sessionmaker(bind=engine)
session = Session()

for user in users:
    row = Users(**user)
    session.add(row)
    
for upload in uploads:
    row = Uploads(**upload)
    session.add(row)

session.commit()