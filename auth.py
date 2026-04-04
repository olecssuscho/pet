from datetime import datetime ,timedelta
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from dbmodels import User
from config import settings

contex=CryptContext(schemes=["argon2", "bcrypt"],deprecated = "auto")
user_shema= OAuth2PasswordBearer(tokenUrl="/user/sing_up")

def hash_password(password:str):
    return contex.hash(password)

def check_password(password :str, compare_password :str):
    return contex.verify(password,compare_password)
    
def create_token(data: dict):
    to_encode = data.copy()
    expire=datetime.utcnow() + timedelta(minutes=settings.TIME_LIVE)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SUPER_SECRET_KEY,settings.ALGORIPHM)

def decode_token(token:str):
    try:
        payload = jwt.decode(token,settings.SUPER_SECRET_KEY,[settings.ALGORIPHM])
        return payload
    except JWTError:
        return None
    
def get_current_user(token:str=Depends(user_shema), db: Session = Depends(get_db)):
    payload=decode_token(token)
    if not payload or "login" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        user=db.query(User).filter(User.login == payload["login"]).first()
        return user

