from database import SessionLocal
from shemas.dbmodels import User
from fastapi.security import OAuth2PasswordBearer
from security import decode_token

from fastapi import status,HTTPException,Depends
from sqlalchemy.orm import Session

user_shema= OAuth2PasswordBearer(tokenUrl="/user/login")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token:str=Depends(user_shema), db: Session = Depends(get_db)):
    payload=decode_token(token)
    if not payload or "login" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        user=db.query(User).filter(User.login == payload["login"]).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User with that credentials no found")
        return user