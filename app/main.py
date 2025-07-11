from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, Depends
from fastapi.params import Body
from httpx import delete
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi.exceptions import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .settings import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get('/')
def root():
    return {'Message':'Welcome Abroad'}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    
    return {'message':post}

@app.post('/posts')
def create_post( post: Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get('/posts/{id}')
def get_single_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

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



@app.put('/posts/{id}')
def update_post(post:Post, id:int, db:Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    get_post = post_query.first()

    if not get_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id - {id} not found!")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {'updated': post_query.first()}


