import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database_connection import get_by,Base 
from fastapi.testclient import TestClient
from app.main import app 
from app.schemes.login_scheme import ResponseLogin
from jose import jwt
from app.aouth2 import create_access_token
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.Db_username}:{settings.Db_password}@{settings.Db_host}:{settings.Db_port}/{settings.Db_name}_Test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False,autocommit =False, bind =engine)



@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()
    
    
@pytest.fixture
def client(session):
    def override_get_by():
        
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_by]= override_get_by
    yield TestClient(app)
    
# #########################################User_Fixtutre############################################
@pytest.fixture
def test_user(client):
    new_data ={
        "firstname": "Nashel",
        "lastname": "Mashumba",
        "age": 20,
        "sex":"male",
        "password": "123456",
        "email": "nashelmashumba32@gmail.com"
    }
    res = client.post("/users/", json= new_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = new_data['password']
    return new_user
# ##################################Login_Fixture########################################################
@pytest.fixture
def test_login(client,test_user):
    res = client.post("/login/", json = {
        "firstname":test_user['firstname'],
        "email":test_user['email'],
        "password":test_user['password']
    })
    
    login_res = ResponseLogin(**res.json())
    payload =  jwt.decode(login_res.access_token,settings.secret_key, algorithms=[settings.algorithm])
    id:int = payload.get("user_id")
    role:str =payload.get("role")
   

    return {
        "access_token":login_res.access_token,
        "id":id,
        "role":role
    }  
#  #########################
@pytest.fixture
def test_users(client):
    new_data ={
        "firstname": "Takunda",
        "lastname": "Mashumba",
        "age": 20,
        "sex":"male",
        "password": "123456",
        "email": "nashelmashumba5@gmail.com"
    }
    res = client.post("/users/", json= new_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = new_data['password']
    return new_user
##########################Token############################################################
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id'],
                                "role":test_user['roles']})
    
    
@pytest.fixture
def authorized_client(client,token):
    client.headers={
        ** client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

# ##############################Inseting data########################################################
@pytest.fixture
def test_createtasks(authorized_client):
    tasks_data = {
        "title":"HTML",
        "description":"learning to be good yoo!",
        "status":"pending",
        "priority":"high"
    }
    res = authorized_client.post("/tasks/",json=tasks_data)
     
     
    response = res.json()
    
    assert res.status_code == 201
    
    return response