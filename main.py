from fastapi import Depends,FastAPI
from database import engine,SessionLocal,get_db
from dbmodels import Task,User
from models import TaskModels,UserModels
import dbmodels
from sqlalchemy.orm import Session
from auth import hash_password,check_password,create_token,decode_token,get_current_user,user_shema
from routers import tasks,users

app=FastAPI()

dbmodels.Base.metadata.create_all(bind=engine)

app.include_router(tasks.router)
app.include_router(users.router)



