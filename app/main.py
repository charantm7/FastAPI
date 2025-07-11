import email
from fastapi import FastAPI, Response, status, Depends
from typing import Optional, List
from fastapi.exceptions import HTTPException
from . import models, schema
from .settings import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# CRUD Operation

@app.get('/')
def root():
    return {'Message':'Welcome Abroad'}

@app.get('/posts', response_model=List[schema.Postesponse])
def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    
    return post

@app.post('/posts', response_model=schema.Postesponse)
def create_post( post: schema.Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get('/posts/{id}', response_model=schema.Postesponse)
def get_single_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with ID - {id} not found!')
    
    return post


@app.delete('/posts/{id}')
def delete_posts(id: int, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id - {id} not found!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {'message':f'Post deleted with id {id}'}



@app.put('/posts/{id}', response_model=schema.Postesponse)
def update_post(post:schema.Post, id:int, db:Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    get_post = post_query.first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id - {id} not found!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schema.User_response)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user.email} already exists"
        )

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


