from datetime import datetime ,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext
from config import settings

contex=CryptContext(schemes=["argon2", "bcrypt"],deprecated = "auto")

def hash_password(password:str):
    return contex.hash(password)

def check_password(password :str, compare_password :str):
    return contex.verify(password,compare_password)
    
def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type":"access"})
    expire=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"type":"refresh"})
    expire=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,settings.SECRET_KEY,settings.ALGORITHM)

def decode_token(token:str):
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
    


