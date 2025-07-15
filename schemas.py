import datetime
from pydantic import BaseModel,EmailStr
from typing import Optional
from pydantic.types import conint
class PostBase(BaseModel):
    title: str
    content: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    

    class Config:
        from_attributes = True
        
class PostCreate(PostBase):
    published: bool = True
    pass

class ReturnPost(PostBase):
    id: int
    user_id: int
    published: bool 
    owner : UserOut
    class Config:
        from_attributes = True
class PostOut(BaseModel):
    Post: ReturnPost
    votes : int
    class Config:
        from_attributes = True
    
class CreateUser(BaseModel):
    email: EmailStr
    password:str
    

class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
class Token(BaseModel):
    access_token : str
    token_type : str
class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id : int
    dir : int
    