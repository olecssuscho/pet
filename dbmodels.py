from sqlalchemy import Column,Integer,String,DateTime,VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Task(Base):

    __tablename__="todo"

    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String)
    description = Column(String)
    
class User(Base):
    
    __tablename__="Users"
    
    id = Column(Integer,autoincrement=True,primary_key=True)
    login= Column(String)
    password= Column(String)
    token= Column(String)