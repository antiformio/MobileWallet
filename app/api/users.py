from models.models import User

from schema import User as SchemaUser
from fastapi_sqlalchemy import db
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from app.api.auth import auth_required
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()

# TODO CREATE CONTROLLERS (FETCH DATA)
#  AND REPOSITORY FILE HOLDING THE LOGIC ON CREATING DELETING ETC FOR ALL MODELS
#   THEN THE VIEW CALLS THE CONTROLLER, AND THE CONTROLLER CALLS THE REPOSITORY


@router.get("/users/", dependencies=[Depends(auth_required)], tags=["Users"])
async def get_users():
    return db.session.query(User).all()


@router.get("/user/{user_id}", dependencies=[Depends(auth_required)], tags=["Users"])
async def get_user(user_id: int):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return user


@router.post("/add-user/", response_model=SchemaUser)
async def create_user(user: SchemaUser):
    db_user = User(
        name=user.name, db_username=user.db_username, db_password=user.db_password
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user


@router.delete("/user/{user_id}", dependencies=[Depends(auth_required)], tags=["Users"])
async def delete_wallet(user_id: int):
    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    db.session.delete(user)
    db.session.commit()
    return HTTPException(status_code=200, detail="User deleted")
