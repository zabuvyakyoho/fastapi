from fastapi import APIRouter, FastAPI, Depends, HTTPException, Path, status
from models import Todos, Users
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user
from .auth import bcrypt_context
from passlib.context import CryptContext


router = APIRouter(
        prefix='/users',
        tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChangePasswordRequest(BaseModel):
    new_password: str = Field(min_length=6)

class ChangeNumberRequest(BaseModel):
    new_phone_number: str = Field(min_length=6)


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_record = db.query(Users).filter(Users.id == user.get('id')).first()
    print(user_record)
    return user_record


@router.put('/password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(user: user_dependency, db:db_dependency, 
                          change_password_request: ChangePasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_model.hashed_password = bcrypt_context.hash(change_password_request.new_password)
    db.add(user_model)
    db.commit()
    return {"message": "Password updated successfully"}

@router.put('/phone_number/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def phone_number(user: user_dependency, db:db_dependency, 
                          change_phone_number: ChangeNumberRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    return {"message": "Phone number updated successfully"}


