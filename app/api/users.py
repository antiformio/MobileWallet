import schema
from models.models import User

from schema import User as SchemaUser
from fastapi_sqlalchemy import db
from fastapi import Depends, HTTPException, status, APIRouter
from aux.hashing import bcrypt_password
from aux.oauth2 import get_current_user
from typing import List


router = APIRouter(tags=["Users"])

# TODO CREATE SERVICE LAYER ARCHITECTURE (FETCH DATA)
#   check https://camillovisini.com/article/abstracting-fastapi-services/

# TODO async orm 

# TODO Add response models to all user and wallet 

@router.get("/users/", response_model=List[SchemaUser])
async def get_users(current_user: schema.User = Depends(get_current_user)):
    return db.session.query(User).all()


@router.get("/user/{user_id}")
async def get_user(user_id: int, current_user: schema.User = Depends(get_current_user)):
    if user := db.session.query(User).filter_by(id=user_id).first():
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No user found"
        )


@router.post("/add-user/", response_model=SchemaUser)
async def create_user(
    user: SchemaUser
):
    db_user = User(
        name=user.name,
        db_username=user.db_username,
        db_password=bcrypt_password(user.db_password),
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user


@router.delete("/user/{user_id}")
async def delete_user(
    user_id: int, current_user: schema.User = Depends(get_current_user)
):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No user found"
        )
    db.session.delete(user)
    db.session.commit()
    return HTTPException(status_code=200, detail="User deleted")
