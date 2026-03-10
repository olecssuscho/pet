from fastapi import Depends,FastAPI
from database import engine,SessionLocal
from dbmodels import Task,User
from models import TaskModels,UserModels
import dbmodels
from sqlalchemy.orm import Session
from auth import hash_password,check_password,create_token,decode_token,get_current_user,user_shema


app=FastAPI()

dbmodels.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(dbmodels.Task).all()


@app.post("/autorization/post")
def add_to_db(task:TaskModels,db: Session=Depends(get_db),token:str=Depends(get_current_user)):
    if  db.query(dbmodels.User).filter(dbmodels.User.token == token).first():
        db.add(Task(**task.model_dump()))
        db.commit()
        return "Sucsses"
    else:
        return "User in not authorized"


@app.put("/put")
def Update(id:int,task:TaskModels,db: Session=Depends(get_db)):
    db_task=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_task:
        db_task.name=task.name
        db_task.description=task.description
        db.commit()
        return db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    else:
        return "Wrong id"


@app.delete("/delete")
def delete_from_db(id: int,db: Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"

#
#Login and others
#

@app.post("/login")
def login(user:UserModels,db: Session=Depends(get_db)):
    token=create_token(user)
    db.add(User(**user.model_dump(),token=token))
    db.commit()
    return token

@app.delete("/delete_user")
def delete_user(id:int,db:Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.User).filter(dbmodels.User.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"

@app.delete("/deleteall")
def delete_all(db:Session=Depends(get_db)):
    db.query(dbmodels.User).delete()
    db.commit()
    return "Sucsses"

@app.post("/autorization")
def autorization(token:str,db:Session=Depends(get_db)):
    return get_current_user(token)

