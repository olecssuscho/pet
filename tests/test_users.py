import pytest 
from fastapi.testclient import TestClient
from main import app

user =TestClient(app)

def test_register_user():
    responce = user.post("/user/register", json={"login": "test", "password":"test"})
    assert responce.status_code == 200

def test_login_user():
    user.post("/user/register", json={"login": "string2", "password":"string2"})
    responce = user.post("/user/login", data={"username": "string2", "password":"string2"})
    assert responce.status_code == 200
    assert "access_token" in responce.json()
    assert "refresh_token" in responce.json()

def test_get_me():
    user.post("/user/register", json={"login": "string2", "password":"string2"})
    responce = user.post("/user/login", data={"username": "string2", "password":"string2"})
    token=responce.json()["access_token"]

    responce = user.get("/user/me", headers={"Authorization":f"Bearer {token}"})
    assert responce.status_code == 200
    assert responce.json()["login"] == "string2"

def test_refresh_token():
    user.post("/user/register", json={"login": "string2", "password":"string2"})
    responce = user.post("/user/login", data={"username": "string2", "password":"string2"})
    access_token=responce.json()["access_token"]
    refresh_token = responce.json()["refresh_token"]
    ref_responce = user.post("/user/refresh", params={"refresh_token": refresh_token})
    acs_responce = user.post("/user/refresh", params={"refresh_token": access_token})
    assert ref_responce.status_code == 200
    assert acs_responce.status_code == 401