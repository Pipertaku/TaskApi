
from datetime import datetime, timedelta, timezone
from jose import jwt , JWTError
from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .schemes.login_scheme import TokenData
from .config import settings
from  .database_connection import get_by
from sqlalchemy.orm import Session
from .models import User



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES =settings.access_token_expire_minutes


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
def verify_access_token(token:str,credential_exception):
    try:
        payload =  jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        id:int = payload.get("user_id")
        role:str =payload.get("role")
        
        if id  and role is None:
        
          raise credential_exception
        token_data = TokenData(id =id, role = role)
        
    except JWTError:
        raise credential_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_by)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail ="Could not validate the credentials",
                                         headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(User).filter(User.id == token.id).first()
    if not user:
        raise credential_exception
    return user
    
    
        