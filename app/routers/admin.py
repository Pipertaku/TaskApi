from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..database_connection import get_by
from ..models import User
from ..schemes.users_scheme import ResponseUsers, Response_Users
from ..aouth2 import get_current_user

route = APIRouter(prefix="/admin", tags=['Admin'])

@route.get("/", response_model=Response_Users, status_code=status.HTTP_200_OK)
def view_users(
    db: Session = Depends(get_by),
    current_user: User = Depends(get_current_user),
    limit: int = Query(2, gt=0),
    page: int = Query(1, gt=0),
    search: Optional[str] = Query(None)
):
    offset = (page - 1) * limit
    
    user = db.query(User).filter(User.id == current_user.id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not any(role.role_name == "admin" for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    # Build query for users
    query = db.query(User)
    
    if search:
        search_lower = search.lower()
        query = query.filter(
            or_(
                User.firstname.ilike(f"%{search_lower}%"),
                User.email.ilike(f"%{search_lower}%")
            )
        )

    users_query = query.offset(offset).limit(limit).all()
    total_users = query.count()
    total_pages = ((total_users + limit) - 1) // limit

    # Serialize users using Pydantic model
    users = []
    for user in users_query:
        roles = [role.role_name for role in user.roles]
        user_dict = {
            "id": user.id,
            "firstname": user.firstname,
            "email": user.email,
            "roles": roles
        }
        users.append(ResponseUsers(**user_dict))
    
    return {
        "users": users,
        "total_pages": total_pages,
        "current_page": page,
    }

@route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_by), current_user: User = Depends(get_current_user)):
    if not any(role.role_name == "admin" for role in current_user.roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    user_to_delete = db.query(User).filter(User.id == id).first()
    
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_to_delete.id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admins cannot delete themselves")

    db.delete(user_to_delete)
    db.commit()
    
    return {"message": "User deleted successfully!"}
