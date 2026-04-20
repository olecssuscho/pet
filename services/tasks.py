from fastapi import Depends
from dependensy import get_db,user_shema,get_current_user
from shemas.dbmodels import Task
from shemas.models import TaskModels
import shemas.dbmodels as dbmodels
from sqlalchemy.orm import Session
from security import decode_token


def get_tasks_server(token:str=Depends(user_shema),db: Session = Depends(get_db)):
    payload=decode_token(token)
    user_id=(db.query(dbmodels.User.id).filter(dbmodels.User.login==payload["login"]).first()[0])   
    return db.query(dbmodels.Task).filter(Task.user_id==user_id).all()

def add_to_db_server(task:TaskModels,token:str=Depends(user_shema),db: Session=Depends(get_db)):
    payload=decode_token(token)
    user_id=(db.query(dbmodels.User.id).filter(dbmodels.User.login==payload["login"]).first()[0])
    db.add(Task(**task.model_dump(),user_id=user_id))
    db.commit()
    return "Sucsses"

def update_server(id:int,task:TaskModels,token:str=Depends(user_shema),db: Session=Depends(get_db)):
    db_task=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    payload=decode_token(token)
    user_id=(db.query(dbmodels.User.id).filter(dbmodels.User.login==payload["login"]).first()[0])
    if db_task.user_id==user_id:
        db_task.name=task.name
        db_task.description=task.description
        db_task.status=task.status
        db.commit()
        return db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    else:
        return "Wrong id"
    
def delete_from_db_server(id: int,token:str=Depends(user_shema),db: Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    payload=decode_token(token)
    user_id=(db.query(dbmodels.User.id).filter(dbmodels.User.login==payload["login"]).first()[0])
    if db_deleted.user_id==user_id:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"

def delete_from_db_all_server(token:str=Depends(user_shema),db: Session=Depends(get_db)):
    db.query(dbmodels.Task).delete()
    db.commit()
    return "Sucsses"