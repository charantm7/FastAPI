from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schema, settings, Oauth2, models

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

# getting the input from the user
# we will get the post id and the dir of the post 1/0

@router.post("/", status_code=status.HTTP_200_OK)
def vote(vote: schema.Vote, db: Session = Depends(settings.get_db), current_user: int = Depends(Oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    get_votes = vote_query.first()

    if (vote.dir == 1):
        if get_votes:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="You already voted on this post")
        
        add_votes = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(add_votes)
        db.commit()

        return f"Vote added Successfully to Post {vote.post_id}"
    
    else:
        if not get_votes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Can not find the vote on post with ID - {vote.post_id}")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return f"Your vote on the post id - {vote.post_id} has been deleted!"
