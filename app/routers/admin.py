from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from ..database_connection import get_by
from ..models import User
from ..schemes.users_scheme import ResponseUsers, Response_Users
from ..aouth2 import get_current_user

route = APIRouter(prefix="/admin", tags=['Admin'])

@route.get("/", response_model=Response_Users, status_code=status.HTTP_200_OK)
def view_users(db: Session = Depends(get_by), current_user: User= Depends(get_current_user),
               limit:int=Query(2, gt=0),
               page: int =Query(1,gt =0)):
    offset= (page-1)* limit
    
    
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not any(role.role_name == "admin" for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
        

    # Fetch all users
    users_query = db.query(User).offset(offset).limit(limit).all()
    total_users = db.query(User).count()
    tota_pages = ((total_users+ limit)-1)//2
    
    
    
    # Serialize users using Pydantic model
    
    users = []
    for user in users_query:
        # Convert roles from Role objects to a list of role names (strings)
        roles = [role.role_name for role in user.roles]
        user_dict = {
            "id": user.id,
            "firstname": user.firstname,
            "email": user.email,
            "roles": roles
        }
        users.append(ResponseUsers(**user_dict))
    
    return {
        "users":users,
        "total_pages":tota_pages,
        "current_page": page,
    }


@route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_by), current_user: User = Depends(get_current_user),
                ):
    # Verify the current user is an admin
    if not any(role.role_name == "admin" for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    # Fetch the user to be deleted
    user_to_delete = db.query(User).filter(User.id == id).first()
    
    # Check if the user exists
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Prevent the admin from deleting themselves
    if user_to_delete.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admins cannot delete themselves")

    # Delete the user
    db.delete(user_to_delete)
    db.commit()
    
    return {"message": "User deleted successfully!"}