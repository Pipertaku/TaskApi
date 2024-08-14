from ..schemes.users_scheme import Post_Users,ResponseUsers
from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database_connection import get_by
from ..models import User ,role_users
from ..password_hashing import verifypassword
from ..schemes.login_scheme import ResponseLogin,Post_login
from ..aouth2 import create_access_token, get_current_user

router = APIRouter(prefix="/login",
                   tags=["Authentication"])


@router.post("/",response_model= ResponseLogin, status_code=status.HTTP_200_OK)
def login(user:Post_login, db:Session= Depends(get_by)):  
    
        
        new_user = db.query(User).outerjoin(role_users, User.id == role_users.c.user_id).filter(
        User.email == user.email , User.firstname == user.firstname).first()
        if not new_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found!")
        
        if not verifypassword(user.password,new_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="wrong credentials!")
        
        roles = [role.role_name for role in new_user.roles]
        
        access_token = create_access_token(data={"user_id":new_user.id,
                                                 "role":roles})
    
        return {"access_token":access_token,"token_type":"Bearer"}
    
        
        
     



