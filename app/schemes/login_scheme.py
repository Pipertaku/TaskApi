from pydantic import BaseModel,EmailStr
from ..schemes.users_scheme import ResponseUsers
from typing import List

class Post_login(BaseModel):
    firstname:str
    email:EmailStr
    password:str
    
class ResponseLogin(BaseModel):
   access_token:str
   token_type:str
    
   class Config:
        from_orm=True
        
        
class TokenData(BaseModel):
    id: int
    role:List[str]
    

    class Config:
        from_orm = True
        
    
    