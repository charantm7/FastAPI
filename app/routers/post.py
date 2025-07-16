from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from .. import schema, models, Oauth2
from ..settings import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# get all public posts
@router.get('/', response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, search: str = ""):

    # it is the sub query to get the likes with the post id to join with the 
    vote_subq = db.query(models.Vote.post_id, func.count(models.Vote.post_id).label("likes")).group_by(models.Vote.post_id).subquery()


    vote = db.query(models.Post, vote_subq.c.likes)\
    .options(joinedload(models.Post.owner))\
        .join(vote_subq, models.Post.id == vote_subq.c.post_id, isouter=True)\
                .filter(models.Post.title.contains(search), models.Post.public == True)\
                    .limit(limit).all()


    result = []
    

    for post , likes in vote:
        post_dict = post.__dict__.copy()
        post_dict['Likes'] = likes or 0
        post_dict['owner'] = post.owner.__dict__
        result.append(post_dict)

    return result

# get the posts of current users
@router.get('/my/', response_model=List[schema.PostOut])
def get_current_user_post(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    
    vote_subq = db.query(models.Vote.post_id, func.count(models.Vote.post_id).label("likes")).group_by(models.Vote.post_id).subquery()


    vote = db.query(models.Post, vote_subq.c.likes)\
    .options(joinedload(models.Post.owner))\
        .join(vote_subq, models.Post.id == vote_subq.c.post_id, isouter=True)\
                .filter(models.Post.owner_id == current_user.id).all()
    
    result = []
    for post , likes in vote:
        post_dict = post.__dict__.copy()
        post_dict['Likes'] = likes or 0
        post_dict['owner'] = post.owner.__dict__
        result.append(post_dict)

    return result

# to create a posts
@router.post('/', response_model=schema.Postesponse)
def create_post( post: schema.Post, current_user: int = Depends(Oauth2.get_current_user), db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# to get a single posts
@router.get('/{id}', response_model=List[schema.PostOut])
def get_single_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    vote_subq = db.query(models.Vote.post_id, func.count(models.Vote.post_id).label("likes")).group_by(models.Vote.post_id).subquery()


    vote_query = db.query(models.Post, vote_subq.c.likes)\
    .options(joinedload(models.Post.owner))\
        .join(vote_subq, models.Post.id == vote_subq.c.post_id, isouter=True)\
                .filter(models.Post.id == id)
    
    vote = vote_query.first()
    
    result = []
    if vote:
        post , likes = vote

        if post.public != True and post.owner_id != current_user.id:

            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'This post with ID - {id} does not exists!')
    
        post_dict = post.__dict__.copy()
        post_dict['Likes'] = likes or 0
        post_dict['owner'] = post.owner.__dict__
        result.append(post_dict)
    else:
        print(vote)

    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID - {id} not found!')


    return result

#  delete the posts
@router.delete('/{id}')
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id - {id} not found!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not Authorized to Delete!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {'message':f'Post deleted with id {id}'}


# update the posts
@router.put('/{id}', response_model=schema.Postesponse)
def update_post(post:schema.Post, id:int, db:Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    get_post = post_query.first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id - {id} not found!")
    
    if get_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not Authorized to Update!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


