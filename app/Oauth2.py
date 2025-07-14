
import os
from jose import JWTError, jwt
from datetime import datetime , timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from app import models
from . import schema
from sqlalchemy.orm import Session
from .settings import get_db


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Schema to get token from header
Oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):

    # get the data from the user to encode
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({'exp':expire}) #update the data with the expire time

    # create toke by adding the data, secrete key, algorithm
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


# token validation
def validate_access_token(token: str):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get('user_id')

        if user_id is None:
            raise credentials_exception
        
        return schema.TokenID(id=user_id)

    except JWTError:
        raise credentials_exception
    

def get_current_user(token: str = Depends(Oauth2_schema), db: Session = Depends(get_db)):

    valid_token = validate_access_token(token)  

    user = db.query(models.User).filter(models.User.id == valid_token.id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    

    return user









