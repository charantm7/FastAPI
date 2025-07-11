import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from fastapi import FastAPI, status, Response


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(dbname='FastAPI', user='charantm', host='localhost', cursor_factory=RealDictCursor, password='Charantm@2005')

        cur = conn.cursor()
        print("Database connection was successful....")
        break

    except Exception as e:
        print(f"Connection Failed with error: {e}")


# Crud Operations

my_posts = [{'title':'car', 'content':'This is car', 'public':True, 'id':1}]
    
        
class Post(BaseModel):
    title: str
    content: str
    public: bool = True 
    tag: str


@app.get('/')
async def home():
    return {"message":"hello World"}

@app.get('/posts')
def get_post():

    # database operation
    cur.execute(""" select * from post""")
    all_post = cur.fetchall()

    # local storage
    # if not my_posts:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post Found")
    return all_post


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(data: Post):

    cur.execute(
        """insert into post (title, content, tag ) values (%s, %s, %s) returning *""",(data.title, data.content, data.tag) 
    )
    created_post = cur.fetchone()
    conn.commit()
    # local storage
    # created_post = data.dict()
    # created_post['id'] = randrange(1, 1000)
    # my_posts.append(created_post)

    return created_post


@app.get('/posts/{id}')
def get_single_post(id: int, res: Response):

    cur.execute(
        """select * from post where id = %s""", (str(id))
    )
    single_post = cur.fetchone()

    # local storage
    # post = []
    # for p in my_posts:
    #     if p['id'] == id:   
    #         return p
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post Available with this ID - {id}")

    #     # res.status_code = status.HTTP_404_NOT_FOUND
    #     # return f"No Post Available with this ID - {id}"
    # else:
    #     return post
    return single_post
        
    
@app.delete('/posts/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int):

    cur.execute(
        """delete from post where id = %s returning *""", (str(id))
    )
    deleted_post = cur.fetchone()
    conn.commit()

    # local storage
    # for i, p in enumerate(my_posts):
    #     if p['id'] == id:
    #         my_posts.pop(i)
    #         return f"Post with ID - {id} has been Deleted!"

    # return f"No post with ID - {id} is available to delete!"
    return deleted_post


@app.put('/posts/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):

    cur.execute(
        """update post set title = %s, content = %s, tag = %s where id = %s returning *""", (post.title, post.content, post.tag, str(id))
    )
    updated_post = cur.fetchone()
    conn.commit()
    # local storage
    # for index, p in enumerate(my_posts):
    #     if p['id'] == id:
    #         updated = post.dict()
    #         updated['id'] = id
    #         my_posts[index] = updated
    #         return updated
        
    # return f"Post not found with ID - {id} to update"
    return updated_post

    

    
    