
from app.schemes.login_scheme import ResponseUsers
import pytest
from app.config import settings
from jose import jwt


   

def test_admin(test_login,client):
    
    res = client.get("/admin/" , headers={"Authorization":f"Bearer {test_login['access_token']}"})
    
    response = res.json()
    assert res.status_code == 200
    print(response)
    response_user = response[0]
    
    # Check if the response data matches the test_login data
    assert response_user['id'] == test_login['id']
    assert response_user['roles'] == test_login['role']
    
    
def test_delete(client, test_login,test_users):
    res = client.delete(f"/admin/{test_users['id']}", headers={"Authorization":f"Bearer {test_login['access_token']}"} )
    assert res.status_code == 204 
    