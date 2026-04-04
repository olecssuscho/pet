from fastapi import Depends,APIRouter,Request,Form
from database import get_db
from dbmodels import Task,User
from models import TaskModels
import dbmodels
from sqlalchemy.orm import Session
from auth import get_current_user
from fastapi.templating import Jinja2Templates
from auth import user_shema,decode_token

router=APIRouter()

templates = Jinja2Templates(directory="templates")

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

# HTML сторінка 
@router.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/task_list")
def get_tasks_page(request: Request, db: Session = Depends(get_db)):
    tasks = db.query(dbmodels.Task).all()

    return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks
    })
  
@router.post("/task_list")
def add_to_db(request: Request,name:str=Form(),description:str=Form(), db:Session=Depends(get_db)):
    db.add(Task(name=name,description=description))
    db.commit()
    tasks = db.query(dbmodels.Task).all()
    return templates.TemplateResponse("task_list.html",{
        "request": request,
        "tasks": tasks
    })
 
@router.put("/task_list/{id}")
def Update(request: Request, id: int, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    db_task = db.query(dbmodels.Task).filter(dbmodels.Task.id == id).first()
    if not db_task:
        return templates.TemplateResponse("task_list.html", {
            "request": request,
            "tasks": db.query(dbmodels.Task).all(),
            "error": f"Task {id} not found"
        })

    db_task.name = name
    db_task.description = description
    db.commit()
    db.refresh(db_task)

    tasks = db.query(dbmodels.Task).all()
    return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks
    })
  
@router.delete("/task_list/{id}")
def delete_task(request: Request,id: int, db: Session = Depends(get_db)):
    db_deleted=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
        tasks = db.query(dbmodels.Task).all()
        return templates.TemplateResponse("task_list.html", {
        "request": request,
        "tasks": tasks
    })
    else:
        return templates.TemplateResponse("task_list.html", {
            "request": request,
            "tasks": db.query(dbmodels.Task).all(),
            "error": f"Task {id} not found"
        })
    
