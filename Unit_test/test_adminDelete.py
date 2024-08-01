import pytest
from app.schemes.login_scheme import ResponseLogin
from app.config import settings
from jose import jwt
from .database import client,session
@pytest.fixture
def test_user(client):
    new_data = {
        "firstname": "Nashel",
        "lastname": "Mashumba",
        "age": 20,
        "sex": "male",
        "password": "123456",
        "email": "nashelmashumba32@gmail.com"
    }
    res = client.post("/users/", json=new_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = new_data['password']
    return new_user

@pytest.fixture
def test_login(client, test_user):
    res = client.post("/login/", json={
        "firstname": test_user['firstname'],
        "email": test_user['email'],
        "password": test_user['password']
    })
    
    print(res.json())
    login_res = ResponseLogin(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    role = payload.get("role")
   
    print(test_user['roles'])
    assert id == test_user['id']
    assert role == test_user['roles']
    assert res.status_code == 200
    assert login_res.token_type == "Bearer"
    
    return {
        "access_token": login_res.access_token,
        "id": id,
        "role": role
    }

@pytest.fixture
def admin_user(client):
    admin_data = {
        "firstname": "Admin",
        "lastname": "User",
        "age": 30,
        "sex": "male",
        "password": "adminpassword",
        "email": "adminuser@example.com",
        "roles": ["admin"]
    }
    res = client.post("/users/", json=admin_data)
    new_admin = res.json()
    new_admin['password'] = admin_data['password']
    assert res.status_code == 201
    return new_admin

@pytest.fixture
def admin_login(client, admin_user):
    res = client.post("/login/", json={
        "firstname":admin_user['firstname'],
        "email": admin_user['email'],
        "password": admin_user['password']
    })
    assert res.status_code == 200
    login_res = ResponseLogin(**res.json())
    return {
        "access_token": login_res.access_token,
        "id": admin_user['id'],
        "role": admin_user['roles']
    }

def test_admin(test_login, client):
    res = client.get("/admin/", headers={"Authorization": f"Bearer {test_login['access_token']}"})
    
    response = res.json()
    assert res.status_code == 200
    print(response)
    response_user = response[0]
    
    # Check if the response data matches the test_login data
    assert response_user['id'] == test_login['id']
    assert response_user['roles'] == test_login['role']

def test_delete(client, admin_login, test_user):
    # Ensure admin has the right to delete users
    headers = {"Authorization": f"Bearer {admin_login['access_token']}"}
    
    # Delete the test user created
    res = client.delete(f"/admin/{test_user['id']}/", headers=headers)
    
    assert res.status_code == 204  # Assuming 204 No Content for successful deletion
    
    # Verify the user was deleted
    res = client.get(f"/users/{test_user['id']}/", headers=headers)
    assert res.status_code == 404  # Assuming 404 Not Found if the user does not exist
