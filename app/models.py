from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, func
from datetime import datetime, timedelta
from .database_connection import Base
from sqlalchemy.orm import Relationship

role_permission = Table(
    'role_permission', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete="CASCADE"), primary_key=True)
)

role_users = Table(
    'role_users', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, nullable=False, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    sex = Column(String, server_default='male')
    password = Column(String, nullable=False)
    tasks = Relationship("Task", back_populates="user",cascade="all, delete-orphan")
    roles = Relationship("Role", secondary=role_users, back_populates="users")

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, server_default='pending', nullable=False)
    priority = Column(String, server_default='high', nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    due_date = Column(DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=7))
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = Relationship("User", back_populates="tasks")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, nullable=False)
    users = Relationship("User", secondary=role_users, back_populates="roles")
    permissions = Relationship("Permission", secondary=role_permission, back_populates="roles")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    actions = Column(String, unique=True)
    roles = Relationship("Role", secondary=role_permission, back_populates="permissions")
