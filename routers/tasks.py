from fastapi import Depends,APIRouter
from dependensy import get_db,user_shema,get_current_user
from shemas.models import TaskModels
from sqlalchemy.orm import Session
from services.tasks import get_tasks_server,add_to_db_server,update_server,delete_from_db_server,delete_from_db_all_server

router=APIRouter()

@router.get("/task/get_all")
def get_tasks(user:str=Depends(get_current_user),db: Session = Depends(get_db)):
    return get_tasks_server(user.id,db)
    
@router.post("/task/post")
def add_to_db(task:TaskModels,user:str=Depends(get_current_user),db: Session=Depends(get_db)):
    return add_to_db_server(task,user.id,db)

@router.put("/task/put")
def Update(id:int,task:TaskModels,user:str=Depends(get_current_user),db: Session=Depends(get_db)):
    return update_server(id,task,user.id,db)

@router.delete("/task/delete")
def delete_from_db(id: int,user:str=Depends(get_current_user),db: Session=Depends(get_db)):
    return delete_from_db_server(id,user.id,db)

@router.delete("/task/delete_all")
def delete_from_db(user:str=Depends(get_current_user),db: Session=Depends(get_db)):
    return delete_from_db_all_server(user.id,db)


