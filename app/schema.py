
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Annotated, Literal

class BasePost(BaseModel):
    title: str
    content: str

class Post(BasePost):
    public: bool = True
    pass

class User_response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class Postesponse(BasePost):
    id: int
    public: bool
    owner_id: int
    owner: User_response
    class Config:
        from_attributes = True

class PostOut(BasePost):
    id: int
    public: bool
    owner_id: int
    owner: User_response
    Likes: int
    class Config:
        from_attributes = True

class User(BaseModel):
    email: EmailStr
    password: str


class CreateUser(User):
    pass

class User_login(User):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenID(BaseModel):
    id: int


class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]