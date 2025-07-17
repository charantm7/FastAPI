from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .settings import engine
from .routers import user, post, auth, vote


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origin = ['https://www.google.com/']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers =["*"]
)

# CRUD Operation

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'Message':'Welcome Abroad'}
