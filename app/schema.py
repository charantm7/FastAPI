
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
        from_attributes = True

class User(BaseModel):
    email: EmailStr
    password: str


class CreateUser(User):
    pass

class User_response(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class User_login(User):
    pass