from fastapi import FastAPI,Response,status,HTTPException , Depends, APIRouter
import models , schemas,oauth2,database
from sqlalchemy.orm import Session

router = APIRouter(
    prefix= "/votes",
    tags= ["votes"]
)
@router.post("/",status_code= status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session = Depends(database.get_db),current_user :int = Depends(oauth2.get_current_user) ):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id , models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user} have alerdy voted on post with id {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id ,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"massege":"successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found vote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"massege":"successfully deleted vote"}