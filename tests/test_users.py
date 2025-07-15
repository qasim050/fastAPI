import schemas
import pytest
from jose import jwt
from config import settings

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "hello world"
    

    
def test_create_users(client):
    res = client.post(
        "/users/",json={"email": "qsalh@gmail.com","password":"Aaa234234"} 
    )
    
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "qsalh@gmail.com"
    assert res.status_code == 201
    
def test_login(client,test_create_user):
    print(test_create_user)
    login_res = client.post(
        "/login", data={"username" : test_create_user["email"], "password":test_create_user["password"]})
    
    token = login_res.json().get("access_token")
    
    payload = jwt.decode(token, key=settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    id: int = payload.get("user_id")
    assert id == test_create_user["id"]
    assert login_res.json().get("token_type") == "bearer"
    assert login_res.status_code == 200
    
    
@pytest.mark.parametrize("email, password, status_code", [
('wrongemail@gmail.com', 'password123', 403),
('sanjeev@gmail.com', 'wrongpassword', 403),
('wrongemail@gmail.com', 'wrongpassword', 403),
(None, 'password123', 422),
('sanjeev@gmail.com', None, 422)])
def test_incorrect_login(client,test_create_user,email, password, status_code):
    res = client.post(
        "/login",data = {"username": email,"password": password}
    )
    assert res.status_code == status_code
    # assert res.json().get("detail") == "invalid cardntials"
    
    