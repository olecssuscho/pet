from datetime import datetime ,timedelta
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from passlib.context import CryptContext
from fastapi.security import OAuth2AuthorizationCodeBearer

SUPER_SECRET_KEY="Your secret key"
ALGORIPHM="HS256"
TIME_LIVE="30"

contex=CryptContext(schemes=["bcrypt"],deprecated = "auto")
user_shema= OAuth2AuthorizationCodeBearer(tokenUrl="login")

def hash_password(password):
    return contex.hash(password)

def check_password(password, hashpassword):
    if contex.verify(password,hashpassword):
        return "Verify completed"
    else:
        return "wrong password"
    
def create_token(data: dict):
    to_encode = data.copy()
    execute_to=datetime.utcnow() + timedelta(minutes=TIME_LIVE)
    to_encode.update({"exp":execute_to})
    return jwt.encode(to_encode,SUPER_SECRET_KEY,ALGORIPHM)

def decode_token(token:str):
    try:
        payload = jwt.decode(token,SUPER_SECRET_KEY,[ALGORIPHM])
        return payload
    except JWTError:
        return None
    
def get_current_user(token:str=Depends(user_shema)):
    payload=decode_token(token)
    if payload == None:
        raise HTTPException( status_code= status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credencial")
    else:
        return payload
    



