from datetime import datetime ,timedelta
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from dbmodels import User

SUPER_SECRET_KEY="Your secret key"
ALGORIPHM="HS256"
TIME_LIVE=30

contex=CryptContext(schemes=["argon2", "bcrypt"],deprecated = "auto")
user_shema= OAuth2PasswordBearer(tokenUrl="/user/sing_up")

def hash_password(password:str):
    return contex.hash(password)

def check_password(password :str, compare_password :str):
    if contex.verify(password,compare_password):
        return "Verify completed"
    else:
        return "Wrong password"
    
def create_token(data: dict):
    to_encode = data.copy()
    expire=datetime.utcnow() + timedelta(minutes=TIME_LIVE)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SUPER_SECRET_KEY,ALGORIPHM)

def decode_token(token:str):
    try:
        payload = jwt.decode(token,SUPER_SECRET_KEY,[ALGORIPHM])
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

