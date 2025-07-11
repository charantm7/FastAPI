from pydantic import BaseModel

class BasePost(BaseModel):
    title: str
    content: str

class Post(BasePost):
    pass

class Postesponse(BasePost):
    public: bool

    class Config:
        orm_mode = True