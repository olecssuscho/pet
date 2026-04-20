from fastapi import Depends,APIRouter
from dependensy import get_db,user_shema
from shemas.models import UserModels
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.user import *

router=APIRouter()

@router.get("/user/get_all")
def get_users(token:str=Depends(user_shema),db: Session = Depends(get_db)):
    return get_users_service(token,db)

@router.post("/user/register")
def login(user:UserModels,db: Session=Depends(get_db)):
    return login_service(user,db)

@router.post("/user/login")
def login_to_accses(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_to_accses_service(form_data,db)

@router.delete("/user/delete_user")
def delete_user(id:int,token:str=Depends(user_shema),db:Session=Depends(get_db)):
    return delete_user_service(id,token,db)

@router.delete("/user/deleteall")
def delete_all(token:str=Depends(user_shema),db:Session=Depends(get_db)):
    return delete_all_service(token,db)
