Im doing unit test on the admin how can I do that but first hear me idea

I make the test_login as pytest fixture 
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
     

and my code for test_admin is from .database import session,client
from app.schemes.login_scheme import ResponseUsers
import pytest
from app.schemes.login_scheme import ResponseLogin
from app.config import settings
from jose import jwt
from Unit_test.test_login import test_login
from app.models import User


def test_admin(client, test_login):
    res = client.get("/admin/" )
    
    
    assert User.id == test_login[id]
    assert User.roles._role_name == test_login['role']
        

and the error i got is ================================================ test session starts ================================================
platform win32 -- Python 3.12.4, pytest-8.3.2, pluggy-1.5.0
rootdir: C:\Users\Nashel\Desktop\Task
plugins: anyio-4.4.0
collected 2 items


Unit_test\test_admin.py E

====================================================== ERRORS ======================================================= 
___________________________________________ ERROR at setup of test_login ____________________________________________ 
file C:\Users\Nashel\Desktop\Task\Unit_test\test_login.py, line 24
  def test_login(client,test_user):
  def test_login(client,test_user):
E       fixture 'test_user' not found
>       available fixtures: anyio_backend, anyio_backend_name, anyio_backend_options, cache, capfd, capfdbinary, caplog, capsys, capsysbinary, client, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, session, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
>       use 'pytest --fixtures [testpath]' for help on them.

C:\Users\Nashel\Desktop\Task\Unit_test\test_login.py:24
============================================== short test summary info ============================================== 
ERROR Unit_test/test_admin.py::test_login
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
=========================================== 7 warnings, 1 error in 3.41s ============================================ 
