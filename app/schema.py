
from datetime import datetime
from pydantic import BaseModel, EmailStr

class BasePost(BaseModel):
    title: str
    content: str

class Post(BasePost):
    pass
class Postesponse(BasePost):
    public: bool
    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class User_response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True