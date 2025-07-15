from fastapi.testclient import TestClient
from main import app

from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database import get_db ,Base,engine
import pytest


DATABASE_URL = f'mysql+mysqlconnector://{settings.DATABASE_USERNAME}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'



engine = create_engine(DATABASE_URL)

test_local_session = sessionmaker(autoflush=False,autocommit = False,bind=engine)





@pytest.fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = test_local_session()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client(session):
    def override_get_db():

        try:    
            yield session
        finally:
          session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
