from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mysql

from config import settings
from sqlalchemy import create_engine
DATABASE_URL = f'mysql+mysqlconnector://{settings.DATABASE_USERNAME}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'


engine = create_engine(DATABASE_URL)

engine = create_engine(f'{settings.DATABASE_USERNAME}+mysqlconnector://root:@/{settings.DATABASE_NAME}')
local_session = sessionmaker(autoflush=False,autocommit = False,bind=engine)
Base = declarative_base()

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
try:
    myconnect = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="api",
)
    mycursor = myconnect.cursor()
    print("good s")
except Exception as error:
    print(f"fild {error}")