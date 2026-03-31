from fastapi import FastAPI
from database import engine
import dbmodels
from routers import tasks,users
from fastapi.templating import Jinja2Templates
app=FastAPI()

dbmodels.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")
app.include_router(tasks.router)
app.include_router(users.router)



