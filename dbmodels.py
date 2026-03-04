from sqlalchemy import Column,Integer,String,DateTime,VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()

class Task(Base):

    __tablename__="todo"

    id = Column(Integer,primary_key=True)
    name = Column(String)
    description = Column(String)
    
