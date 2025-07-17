from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, utils, Oauth2
from ..settings import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])



def user_validation_for_login(username, password, db):

    user = db.query(models.User).filter(models.User.email == username).first()

    if not user or not utils.verify(password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    token = Oauth2.create_access_token({"user_id":user.id})

    return token
    


@router.post('/login')
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    jwt_access_token = user_validation_for_login(credentials.username, credentials.password, db)


    return {"access_token": jwt_access_token, "token_type": "bearer"}

    



