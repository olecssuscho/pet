from fastapi import Depends,FastAPI
from database import engine,SessionLocal
from dbmodels import Task
from models import TaskModels
import dbmodels
from sqlalchemy.orm import Session
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


@app.post("/post")
def add_to_db(task:TaskModels,db: Session=Depends(get_db)):
    db.add(Task(**task.model_dump()))
    db.commit()
    return "Sucsses"


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
    db_task=db.query(dbmodels.Task).filter(dbmodels.Task.id==id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"
        