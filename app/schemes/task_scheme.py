from pydantic import BaseModel
from datetime import datetime, timedelta

class Post(BaseModel):
    title: str
    description: str
    status: str
    priority: str

class ResponsePost(Post):
    id: int
    created_at: datetime
    due_date: datetime
    user_id:int


    class Config:
        from_orm = True

    
class Response_Delete_Task(BaseModel):
    message:str
    
    class Config:
        from_attributes =True
        