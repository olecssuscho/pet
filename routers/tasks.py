from fastapi import Depends,APIRouter
from database import get_db
from dbmodels import Task
from models import TaskModels
import dbmodels
from sqlalchemy.orm import Session
from auth import get_current_user
from auth import user_shema,decode_token

router=APIRouter()

@router.get("/task/get_all")
def get_tasks(token:str=Depends(user_shema),db: Session = Depends(get_db)):
    payload=decode_token(token)
    user_id=(db.query(dbmodels.User.id).filter(dbmodels.User.login==payload["login"]).first()[0])   
    return db.query(dbmodels.Task).filter(Task.user_id==user_id).all()

@router.post("/task/post")
def add_to_db(task:TaskModels,token:str=Depends(user_shema),db: Session=Depends(get_db)):
    payload=decode_token(token)
    user_id=(db.query(dbmodels.User.id).filter(dbmodels.User.login==payload["login"]).first()[0])
    db.add(Task(**task.model_dump(),user_id=user_id))
    db.commit()
    return "Sucsses"

@router.put("/task/put")
def Update(id:int,task:TaskModels,token:str=Depends(user_shema),db: Session=Depends(get_db)):
    db_task=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_task:
        db_task.name=task.name
        db_task.description=task.description
        db_task.status=task.status
        db.commit()
        return db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    else:
        return "Wrong id"

@router.delete("/task/delete")
def delete_from_db(id: int,token:str=Depends(user_shema),db: Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"

@router.delete("/task/delete_all")
def delete_from_db(token:str=Depends(user_shema),db: Session=Depends(get_db)):
    db.query(dbmodels.Task).delete()
    db.commit()
    return "Sucsses"


