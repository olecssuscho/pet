from fastapi import Depends,HTTPException,status
from dependensy import get_db
from shemas.dbmodels import User
from shemas.models import UserModels
import shemas.dbmodels as dbmodels
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from security import create_access_token,check_password,hash_password,create_refresh_token,decode_token

def get_users_service(db: Session) -> UserResponce:
    return db.query(dbmodels.User.login).all()

def login_service(user:UserModels,db: Session):
    if db.query(dbmodels.User.login).filter(User.login==user.login).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Login is used")
    access_token=create_access_token({"login":user.login})
    newpassword=hash_password(user.password)
    user.password=newpassword
    db.add(User(**user.model_dump(),token=access_token))
    db.commit()
    return access_token

def login_to_accses_service(form_data: OAuth2PasswordRequestForm , db: Session ):
    user_db = db.query(User).filter(User.login == form_data.username).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    decode_user=decode_token(user_db.token)
    if not check_password(form_data.password,user_db.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    if not decode_user:
       user_db.token = create_refresh_token({"login":form_data.username})
       db.commit()
    return {"access_token": user_db.token, "token_type": "bearer"}

def delete_user_service(id:int,user:int,db:Session):
    db_deleted=db.query(dbmodels.User).filter(dbmodels.User.id==id).first()
    if not db_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if db_deleted.id!=user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User not found")
    db.delete(db_deleted)
    db.commit()
    return"Sucsses"


