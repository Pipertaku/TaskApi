from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database_connection import get_by
from ..models import User, Role, Permission
from ..schemes.users_scheme import Post_Users, ResponseUsers
from ..password_hashing import hashingpassword

# Create a new FastAPI router for user-related endpoints
router = APIRouter(prefix="/users", tags=["User"])

def admin_exists(db: Session = Depends(get_by)):
    # Check if there is already an admin user in the database
    admin_role = db.query(Role).filter(Role.role_name == "admin").first()
    if admin_role:
        admin_user = db.query(User).filter(User.roles.contains(admin_role)).first()
        return True
    return False

@router.post("/", response_model=ResponseUsers, status_code=status.HTTP_201_CREATED)
def create_user(user: Post_Users, db: Session = Depends(get_by), check_admin: bool = Depends(admin_exists)):
    # Check if the user already exists
    user_query = db.query(User).filter(User.email == user.email).first()
    if user_query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists!")

    # Hash the user's password
    hash_password = hashingpassword(user.password)
    user.password = hash_password

    # Determine the user role
    if check_admin == False:
        # No admin exists yet, create an admin role if necessary
        
        
      user_role = db.query(Role).filter(Role.role_name == "admin").first()
      
      if not user_role:
            user_role = Role(role_name="admin")
            db.add(user_role)
            db.commit()
            db.refresh(user_role)
            
            # Define and assign permissions to the admin role
            admin_permissions = [
                'create_user', 'read_user', 'update_user', 'delete_user',
                'create_role', 'read_role', 'update_role', 'delete_role',
                'create_task', 'read_task', 'update_task', 'delete_task', 'assign_task',
                'create_project', 'read_project', 'update_project', 'delete_project', 'assign_project',
                'manage_settings', 'access_logs',
                'view_reports', 'export_data',
                'send_notifications'
            ]
            for action in admin_permissions:
                permission = db.query(Permission).filter(Permission.actions == action).first()
                if not permission:
                    permission = Permission(actions=action)
                    db.add(permission)            
                user_role.permissions.append(permission)
            db.commit()
    else:
        # Admin exists, create an 'is_regular' role if necessary
        user_role = db.query(Role).filter(Role.role_name == "is_regular").first()
        if not user_role:
            user_role = Role(role_name="is_regular")
            db.add(user_role)
            db.commit()
            db.refresh(user_role)
            
            # Define and assign permissions to the regular role
            regular_permissions = [
                'create_task', 'read_task', 'update_task', 'delete_task',
                'read_project', 'update_project',  
                'update_profile', 'change_password',
                'view_notifications'
            ]
            for action in regular_permissions:
                permission = db.query(Permission).filter(Permission.actions == action).first()
                if not permission:
                    permission = Permission(actions=action)
                    db.add(permission)
                user_role.permissions.append(permission)
            db.commit()

    # Create a new user instance and assign the determined role
    new_user = User(**user.dict())
    new_user.roles.append(user_role)

    try:
        # Add the new user to the database and commit the transaction
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        # Rollback in case of any database integrity errors
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating user")

    # Prepare and return the response data
    response_data = {
        "id": new_user.id,
        "firstname": new_user.firstname,
        "email": new_user.email,
        "roles": [role.role_name for role in new_user.roles]
    }

    return response_data


