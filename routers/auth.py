
import  models, utils,oauth2,schemas
from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import get_db
import sys
sys.path.append("..") 



router = APIRouter(tags=["authentication"])


@router.post("/login",response_model= schemas.Token)
async def login(user_cardentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_cardentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid cardntials")
    if not utils.verify(user_cardentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid cardntials")
        
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return{"access_token": access_token,"token_type": "bearer"}
