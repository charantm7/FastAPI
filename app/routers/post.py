from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schema, models, Oauth2
from ..settings import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/', response_model=List[schema.Postesponse])
def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    
    return post

@router.post('/', response_model=schema.Postesponse)
def create_post( post: schema.Post, current_user: int = Depends(Oauth2.get_current_user), db: Session = Depends(get_db)):

    print(current_user.email)

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get('/{id}', response_model=schema.Postesponse)
def get_single_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID - {id} not found!')
    
    return post


@router.delete('/{id}')
def delete_posts(id: int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id - {id} not found!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {'message':f'Post deleted with id {id}'}



@router.put('/{id}', response_model=schema.Postesponse)
def update_post(post:schema.Post, id:int, db:Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    get_post = post_query.first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id - {id} not found!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


