from models.models import User
from fastapi_sqlalchemy import db
from fastapi import Header, HTTPException, status, APIRouter
import schema
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from aux.hashing import verify_password


# def verify_password(user, password):
#     # Could have used hashed passwords
#     return user.db_password == password


async def auth_required(
    username: str = Header(default=None), password: str = Header(default=None)
):
    user = db.session.query(User).filter_by(db_username=username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    if not verify_password(user, password):
        raise HTTPException(status_code=400, detail="Invalid password")
    return user


router = APIRouter()


@router.post("/login", tags=["Authentication"])
def login(request: schema.Login, db: Session = Depends(get_db)):
    db_user = db.query(User).filter_by(name=request.name).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not verify_password(db_user.db_password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    return db_user
