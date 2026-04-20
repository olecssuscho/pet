from fastapi import Depends,HTTPException,status
from dependensy import get_db,user_shema
from shemas.dbmodels import User
from shemas.models import UserModels
import shemas.dbmodels as dbmodels
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from security import create_access_token,check_password,hash_password,create_refresh_token,decode_token

def get_users_service(token:str=Depends(user_shema),db: Session = Depends(get_db)):
    return db.query(dbmodels.User).all()

def login_service(user:UserModels,db: Session=Depends(get_db)):
    if db.query(dbmodels.User.login).filter(User.login==user.login).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Login is used")
    access_token=create_access_token({"login":user.login})
    newpassword=hash_password(user.password)
    user.password=newpassword
    db.add(User(**user.model_dump(),token=access_token))
    db.commit()
    return access_token

def login_to_accses_service(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.login == form_data.username).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    decode_user=decode_token(user_db.token)
    if not check_password(form_data.password,user_db.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    if not decode_user:
       user_db.token = create_refresh_token({"login":form_data.username})
    return {"access_token": user_db.token, "token_type": "bearer"}

def delete_user_service(id:int,token:str=Depends(user_shema),db:Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.User).filter(dbmodels.User.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"

def delete_all_service(token:str=Depends(user_shema),db:Session=Depends(get_db)):
    db.query(dbmodels.User).delete()
    db.commit()
    return "Sucsses"