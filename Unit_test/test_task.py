import pytest
from jose import jwt    
from app.schemes.task_scheme import ResponsePost,Response_Delete_Task


def test_create(authorized_client):
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
    
        
def test_gettasks(authorized_client, test_createtasks):
    res = authorized_client.get("/tasks/")
    print("the viewing results", res.json())
    
    assert res.status_code==200
    
def test_updatetask(authorized_client,test_createtasks):
    
    task_data = {
        "title":"CSS",
        "description":"learning to be good yoo!",
        "status":"pending",
        "priority":"high"
    }
    res = authorized_client.put(f"/tasks/{test_createtasks['id']}", json = task_data)
    
    response = ResponsePost(** res.json())
    print("the scheme=>",response)
    assert res.status_code ==200
    assert response.title == "CSS"
    
    
def test_deletetasks(authorized_client, test_createtasks):
    res = authorized_client.delete(f"/tasks/{test_createtasks['id']}")
    
    
    assert res.status_code==204
    