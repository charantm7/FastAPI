from fastapi import FastAPI, Response, status, Depends
from typing import Optional, List
from fastapi.exceptions import HTTPException
from . import models, schema, utils
from .settings import engine, get_db
from sqlalchemy.orm import Session
from .routers import user, post, auth


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# CRUD Operation

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return {'Message':'Welcome Abroad'}
