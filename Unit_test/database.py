from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database_connection import get_by,Base

 


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.Db_username}:{settings.Db_password}@{settings.Db_host}:{settings.Db_port}/{settings.Db_name}_Test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False,autocommit =False, bind =engine)
Base.metadata.create_all(bind=engine)

def override_get_by():
    db = TestingSessionLocal()
    
    try:
        
        
        yield db
    finally:
        db.close()

app.dependency_overrides[get_by] = override_get_by

        