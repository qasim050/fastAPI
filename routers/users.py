import models , schemas,utils
from fastapi import FastAPI,Response,status,HTTPException , Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
import sys
sys.path.append("..") 

router = APIRouter(
    prefix= "/users",
    tags= ["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.CreateUser,db : Session = Depends(get_db)):

    
    hashed_pass = utils.hash(user.password)
    
  
    new_user = models.User(**user.model_dump())
    new_user.password = hashed_pass
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id : int ,db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id : {id} not found")
    return user