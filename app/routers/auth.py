from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schema, models, utils, Oauth2
from ..settings import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    
    # create jwt access token
    jwt_access_token = Oauth2.create_access_token({'user_id':user.id})

    #validate token


    return {"access_token": jwt_access_token, "token_type": "bearer"}

    



