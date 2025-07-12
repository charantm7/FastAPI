
from email.policy import HTTP
import stat
from fastapi import status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from httpx import get
from sqlalchemy.orm import Session
from .. import schema, models, utils
from ..settings import get_db

router = APIRouter()


@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schema.User_response)
def create_user(user: schema.CreateUser, db: Session = Depends(get_db)):

    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user.email} already exists"
        )
    hashed_pass = utils.hashed(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/users/{id}', response_model=schema.User_response)
def get_user(id: int, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID - {id} doesn't exists!")
    return user

@router.delete('/users/{id}')
def delete_user(id:int, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id - {id} does not exists! ')

    user_query.delete(synchronize_session=False)

    db.commit()

    return f"User with ID - {id} Deleted!"

