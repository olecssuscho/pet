import pytest 
from fastapi.testclient import TestClient
from main import app

user =TestClient(app)

def test_get_tasks():
    responce = user.post("/user/login", data={"username": "string", "password":"string"})
    token=responce.json()["access_token"]
    task=user.get("/task/get_all",
                  headers={"Authorization":f"Bearer {token}"})
    assert task.status_code==200

def test_add_to_db():
    responce = user.post("/user/login", data={"username": "string", "password":"string"})
    token=responce.json()["access_token"]
    
    task=user.post("/task/post", 
                   json={"name":"test","description":"test","status":"new"}, 
                   headers={"Authorization":f"Bearer {token}"})
    assert task.status_code ==200

def test_update():
    responce = user.post("/user/login", data={"username": "string", "password":"string"})
    token=responce.json()["access_token"]
    
    task_add=user.post("/task/post", 
                   json={"name":"test","description":"test","status":"new"}, 
                   headers={"Authorization":f"Bearer {token}"})

    task_id=task_add.json()["id"]

    task=user.put("/task/put",
                    params={"id":task_id},
                    json={"name":"test2","description":"test2","status":"in_progress"}, 
                    headers={"Authorization":f"Bearer {token}"})
    assert task.status_code ==200

def test_delete():
    responce = user.post("/user/login", data={"username": "string", "password":"string"})
    token=responce.json()["access_token"]
    
    task_add=user.post("/task/post", 
                   json={"name":"test","description":"test","status":"new"}, 
                   headers={"Authorization":f"Bearer {token}"})

    task_id=task_add.json()["id"]
    
    task=user.delete("/task/delete",
                    params={"id":task_id},
                    headers={"Authorization":f"Bearer {token}"})
    assert task.status_code ==200
