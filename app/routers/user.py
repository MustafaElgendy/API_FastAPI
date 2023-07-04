from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from typing import List


router = APIRouter(
    prefix= "/users",
    tags= ['Users']
)
# For Users 
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.User)
def create_user(user: schemas.CreateUser ,db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    exist_email = db.query(models.User).filter(models.User.email == new_user.email).first()
    if exist_email :
        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                            detail=f"your Email '{new_user.email}' is already in use")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    if user.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.get("/{id}", response_model= schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"User with id: {id} was not found")
    return user