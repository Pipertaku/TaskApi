from ..schemes.task_scheme import Post,ResponsePost,Response_Delete_Task
from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database_connection import get_by
from ..models import  Task,User
from typing import List
from ..aouth2 import  get_current_user



route= APIRouter(prefix='/tasks',
                 tags=['Task'])


@route.post("/",response_model=ResponsePost, status_code=status.HTTP_201_CREATED)
def  create_task(task:Post, db:Session = Depends(get_by), current_user:int = Depends(get_current_user)):
    new_task = Task(**task.dict(),user_id = current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return(new_task)

@route.get("/",response_model=List[ResponsePost], status_code=status.HTTP_200_OK)
def get_tasks(db:Session = Depends(get_by), current_user:int = Depends(get_current_user)):
    tasks_query = db.query(Task).filter(Task.user_id == current_user.id).all()
    
    # Im now unpacking the data from the database
    # tasks =[]
    # for task in tasks_query:
    #     task_dict = task.__dict__.copy()
        
    #     tasks.append(ResponsePost(**task_dict))  
    
    return tasks_query

@route.put("/{id}",response_model=ResponsePost,status_code=status.HTTP_200_OK)
def upadete_task (id:int, task_update:Post, db:Session= Depends(get_by), current_user:int = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id ==id ).first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="not found")
    for key,value in task_update.dict().items():
        setattr(task,key,value)
    db.commit()
    db.refresh(task)
    
    return task

@route.delete("/{id}",response_model=Response_Delete_Task,status_code=status.HTTP_200_OK  )
def delete_task(id:int, db:Session = Depends(get_by), current_user:int = Depends(get_current_user)):
    
    task = db.query(Task).filter( Task.id== id ).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=" id not found")
    
    db.delete(task)
    db.commit()
    
    return {"message":"task deleted yoo!"}

    
    

    
    