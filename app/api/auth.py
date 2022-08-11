from models.models import User
from fastapi_sqlalchemy import db
from fastapi import Header, HTTPException


def verify_password(user, password):
    # Could have used hashed passwords
    return user.db_password == password


async def auth_required(
    username: str = Header(default=None), password: str = Header(default=None)
):
    user = db.session.query(User).filter_by(db_username=username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")
    if not verify_password(user, password):
        raise HTTPException(status_code=400, detail="Invalid password")
    return user
