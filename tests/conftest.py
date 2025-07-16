from fastapi.testclient import TestClient
from main import app
import models
from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import get_db ,Base,engine
import pytest
from oauth2 import create_access_token

DATABASE_URL = f'mysql+mysqlconnector://{settings.DATABASE_USERNAME}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'



engine = create_engine(DATABASE_URL)

test_local_session = sessionmaker(autoflush=False,autocommit = False,bind=engine)





@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = test_local_session()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():

        try:    
            yield session
        finally:
          session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture
def test_create_user(client):
    user_data = {"email": "asim@gmail.com", "password": "Aaa43214321"}
    res = client.post("/users/",json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
@pytest.fixture
def test_create_user2(client):
    user_data = {"email": "asim2@gmail.com", "password": "Aaa43214321"}
    res = client.post("/users/",json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user   
@pytest.fixture
def token(test_create_user):
    return create_access_token({"user_id" : test_create_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
** client.headers,
"Authorization": f"Bearer {token}"}

    return client



@pytest.fixture
def test_posts(test_create_user, session,test_create_user2):
    posts_data = [{
            "title": "first title",
            "content": "first content",
            "user_id": test_create_user['id']
                        },
            {"title": "2nd title",
            "content": "2nd content",
            "user_id": test_create_user['id']},

            {
            "title": "3rd title",
            "content": "3rd content",
            "user_id": test_create_user['id']

                        },

            {
            "title": "4rd title",
            "content": "4rd content",
            "user_id": test_create_user2['id']

                        }]
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model,posts_data)

    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts

