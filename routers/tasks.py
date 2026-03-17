from fastapi import Depends,APIRouter
from database import get_db
from dbmodels import Task
from models import TaskModels
import dbmodels
from sqlalchemy.orm import Session
from auth import get_current_user

router=APIRouter()

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return db.query(dbmodels.Task).all()

@router.post("/task/post")
def add_to_db(task:TaskModels,db: Session=Depends(get_db),token:str=Depends(get_current_user)):
    if  db.query(dbmodels.User).filter(dbmodels.User.token == token).first():
        db.add(Task(**task.model_dump()))
        db.commit()
        return "Sucsses"
    else:
        return "User in not authorized"

@router.put("/task/put")
def Update(id:int,task:TaskModels,db: Session=Depends(get_db)):
    db_task=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_task:
        db_task.name=task.name
        db_task.description=task.description
        db.commit()
        return db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    else:
        return "Wrong id"

@router.delete("/task/delete")
def delete_from_db(id: int,db: Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"