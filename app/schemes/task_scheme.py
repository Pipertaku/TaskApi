from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List

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
      from_attributes=True



class Response_Post(BaseModel):
    task:List[ResponsePost]
    total_pages:int
    total_tasks:int
    current_page:int

    class Config:
        from_attributes=True

    
class Response_Delete_Task(BaseModel):
    message:str
    
    class Config:
        from_attributes =True
        