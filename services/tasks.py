from fastapi import HTTPException,status
from shemas.dbmodels import Task
from shemas.models import TaskModels
import shemas.dbmodels as dbmodels
from sqlalchemy.orm import Session

def get_tasks_server(user_id:int,db: Session): 
    return db.query(dbmodels.Task).filter(Task.user_id==user_id).all()

def add_to_db_server(task:TaskModels,user_id:int,db: Session):
    db.add(Task(**task.model_dump(),user_id=user_id))
    db.commit()
    return "Sucsses"

def update_server(id:int,task:TaskModels,user_id:int,db: Session):
    db_task=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_task ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    if db_task.user_id==user_id:
        db_task.name=task.name
        db_task.description=task.description
        db_task.status=task.status
        db.commit()
        return db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
    
def delete_from_db_server(id: int,user_id:int,db: Session):
    db_deleted=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_deleted ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Task not found")
    if db_deleted.user_id==user_id:
        db.delete(db_deleted)
        db.commit()
        return"Sucsses"
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
