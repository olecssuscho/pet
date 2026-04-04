from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()
class User(Base):
    
    __tablename__="Users"
    
    id = Column(Integer,autoincrement=True,primary_key=True)
    login= Column(String)
    password= Column(String)
    token= Column(String)

    
class Task(Base):

    __tablename__="todo"

    id = Column(Integer,autoincrement=True,primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id=Column(Integer,ForeignKey(User.id),nullable=False)
    
