
from datetime import datetime
from pydantic import BaseModel, EmailStr

class BasePost(BaseModel):
    title: str
    content: str

class Post(BasePost):
    public: bool = True
    pass

class Postesponse(BasePost):
    id: int
    public: bool
    owner_id: int
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

class Token(BaseModel):
    access_token: str
    token_type: str
class TokenID(BaseModel):
    id: int

