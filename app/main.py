from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi.exceptions import HTTPException


app = FastAPI()

# Crud Operations

my_posts = [{'title':'car', 'content':'This is car', 'public':True, 'id':1}]
    
        
class Post(BaseModel):
    title: str
    content: str
    public: bool = True 


@app.get('/')
async def home():
    return {"message":"hello World"}

@app.get('/posts')
def get_post():
    if not my_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post Found")
    return my_posts


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(data: Post):
    created_post = data.dict()
    created_post['id'] = randrange(1, 1000)
    my_posts.append(created_post)

    return created_post


@app.get('/posts/{id}')
def get_single_post(id: int, res: Response):
    post = []
    for p in my_posts:
        if p['id'] == id:   
            return p
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post Available with this ID - {id}")

        # res.status_code = status.HTTP_404_NOT_FOUND
        # return f"No Post Available with this ID - {id}"
    else:
        return post
        
    
@app.delete('/posts/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int):

    for i, p in enumerate(my_posts):
        if p['id'] == id:
            my_posts.pop(i)
            return f"Post with ID - {id} has been Deleted!"


    return f"No post with ID - {id} is available to delete!"


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):

    for index, p in enumerate(my_posts):
        if p['id'] == id:
            updated = post.dict()
            updated['id'] = id
            my_posts[index] = updated
            return updated
        
    return f"Post not found with ID - {id} to update"

    

    
    