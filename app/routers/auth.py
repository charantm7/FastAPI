from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schema, models, utils
from ..settings import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(credentials: schema.User_login, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')

    return {'message': 'user found in database'}