import models , schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException , Depends,APIRouter
from sqlalchemy.orm import Session ,KeyFuncDict
from database import get_db
from typing import List,Optional
import sys
from sqlalchemy import func
sys.path.append("..") 

router = APIRouter(
    prefix="/posts",
    tags= ["posts"]
)

# @router.get("/")
# async def root():
#     return {"message": "hello world!"}



# Endpoint to get postss
# @router.get("/",response_model= List[schemas.ReturnPost])
@router.get("/",response_model= List[schemas.PostOut])
async def get_posts(db : Session = Depends(get_db),limit:int = 10,skip:int = 0,searsh:Optional[str]=""):
    # mycursor.execute("SELECT * FROM posts")
    # post = mycursor.fetchall()
    result = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(searsh)).limit(limit).offset(skip).all()
    # post = db.query(models.Post).filter(models.Post.title.contains(searsh)).limit(limit).offset(skip).all()
    print(result)

    return result


# Endpoint to create a new post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ReturnPost)
async def create_posts(post: schemas.PostCreate,db : Session = Depends(get_db),
                       current_user :int = Depends(oauth2.get_current_user)):
    # mycursor.execute("INSERT INTO posts (title,contect) VALUES (%s ,%s)",(new_post.title,new_post.content))
    # myconnect.commit()
    print(current_user)
    new_post = models.Post(user_id =current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}",response_model=schemas.PostOut)
async def get_posts(id:int,db : Session = Depends(get_db)):
    # mycursor.execute("SELECT * FROM posts WHERE id = %s" ,(str(id),))
    # post = mycursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"the post of id: {id} is not found")
    return post


    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db),
                     current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.ReturnPost)
async def update_post(id: int, post_data: schemas.PostCreate, db: Session = Depends(get_db),
                     current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} not found"
        )
    
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    
    post_query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()



    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    # mycursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),))
    # update_data = mycursor.fetchone()
    return  post_query.first()
        