#python -m uvicorn main:app --reload --port 8001 
from fastapi import FastAPI
# from pydantic import BaseModel
# import models
from database import engine
from routers import users,posts,auth,votes
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)   
app = FastAPI()
origins = ["*"]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
       

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)