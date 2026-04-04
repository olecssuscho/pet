from fastapi import Depends,APIRouter,Form,HTTPException,status
from database import get_db
from dbmodels import User
from models import UserModels
import dbmodels
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import create_token,check_password,hash_password,user_shema

router=APIRouter()

@router.get("/user/get_all")
def get_users(password:str=Depends(user_shema),db: Session = Depends(get_db)):
    return db.query(dbmodels.User).all()

@router.post("/user/register")
def login(user:UserModels,db: Session=Depends(get_db)):
    if db.query(dbmodels.User.login).filter(User.login==user.login).first():
        return HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Login is used")
    token=create_token({"login":user.login})
    newpassword=hash_password(user.password)
    user.password=newpassword
    db.add(User(**user.model_dump(),token=token))
    db.commit()
    return token

@router.post("/user/sing_up")
def login_to_accses(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.login == form_data.username).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="User not found")
    if not check_password(form_data.password,user_db.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    return {"access_token": user_db.token, "token_type": "bearer"}

@router.delete("/user/delete_user")
def delete_user(id:int,password:str=Depends(user_shema),db:Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.User).filter(dbmodels.User.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"

@router.delete("/user/deleteall")
def delete_all(password:str=Depends(user_shema),db:Session=Depends(get_db)):
    db.query(dbmodels.User).delete()
    db.commit()
    return "Sucsses"

