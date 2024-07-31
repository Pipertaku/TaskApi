from pydantic import BaseModel, EmailStr
from typing import List

class Post_Users(BaseModel):
    firstname: str
    lastname: str
    age: int
    sex: str
    password: str
    email: EmailStr

class ResponseUsers(BaseModel):
    id: int
    firstname: str
    email: EmailStr
    roles: list[str]

    class Config:
        from_orm = True
