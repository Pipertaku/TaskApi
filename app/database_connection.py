from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.Db_username}:{settings.Db_password}@{settings.Db_host}:{settings.Db_port}/{settings.Db_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,autocommit =False, bind =engine)
Base = declarative_base()

def get_by():
    db = SessionLocal()
    
    try:
        
        
        yield db
    finally:
        db.close()
        
    

