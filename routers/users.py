from fastapi import Depends,APIRouter,Form,HTTPException
from database import get_db
from dbmodels import User
from models import UserModels
import dbmodels
from sqlalchemy.orm import Session
from auth import create_token,check_password,hash_password

router=APIRouter()

@router.post("/user/login")
def login(user:UserModels,db: Session=Depends(get_db)):
    token=create_token(user.dict())
    newpassword=hash_password(user.password)
    user.password=newpassword
    db.add(User(**user.model_dump(),token=token))
    db.commit()
    return token

@router.delete("/user/delete_user")
def delete_user(id:int,db:Session=Depends(get_db)):
    db_deleted=db.query(dbmodels.User).filter(dbmodels.User.id==id).first()
    if db_deleted:
        db.delete(db_deleted)
        db.commit()
    else:
        return"Wrong id"
    return"Sucsses"

@router.delete("/user/deleteall")
def delete_all(db:Session=Depends(get_db)):
    db.query(dbmodels.User).delete()
    db.commit()
    return "Sucsses"

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if check_password(password, user.password) != "Verify completed":
        raise HTTPException(status_code=400, detail="Wrong password")
    token = create_token({"login":user.login,"password":user.password})
    return {"access_token": token, "token_type": "bearer"}