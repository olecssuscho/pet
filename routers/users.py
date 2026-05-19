from fastapi import Depends,APIRouter
from dependensy import get_db,get_current_user
from shemas.models import UserModels
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from services.users import *
from shemas.responces import UserResponse
from security import create_access_token

router=APIRouter()

@router.get("/user/get_all",response_model=list[UserResponse])
def get_users(user:User=Depends(get_current_user),db: Session = Depends(get_db)):
    return get_users_service(db)

@router.post("/user/register")
def register(user:UserModels,db: Session=Depends(get_db)):
    return register_service(user,db)

@router.post("/user/login")
def login_to_accses(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_to_accses_service(form_data,db)

@router.delete("/user/delete_user")
def delete_user(id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return delete_user_service(id,user.id,db)

@router.post("/user/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    return refresh_token_service(refresh_token, db)

