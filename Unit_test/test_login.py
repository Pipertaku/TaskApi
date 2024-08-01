
import pytest
from app.schemes.login_scheme import ResponseLogin
from app.config import settings
from jose import jwt


@pytest.fixture
def test_login(client,test_user):
    res = client.post("/login/", json = {
        "firstname":test_user['firstname'],
        "email":test_user['email'],
        "password":test_user['password']
    })
    
    print(res.json())
    login_res = ResponseLogin(**res.json())
    payload =  jwt.decode(login_res.access_token,settings.secret_key, algorithms=[settings.algorithm])
    id:int = payload.get("user_id")
    role:str =payload.get("role")
   
    print(test_user['roles'])
    assert id == test_user['id']
    assert role == test_user['roles']
    assert res.status_code ==200
    assert login_res.token_type =="Bearer"
    
    
    return {
        "access_token":login_res.access_token,
        "id":id,
        "role":role
    }  