import os
from models.models import User
from fastapi_sqlalchemy import db
from fastapi import Header, HTTPException, status, APIRouter, Depends
import schema
from database import get_db
from sqlalchemy.orm import Session
from aux.hashing import verify_password
from fastapi.security import OAuth2PasswordRequestForm
from aux.token import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = db.query(User).filter_by(name=request.username).first()
    if not db_user:
        # TODO: The class is expecting headers ? check this bug
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    if not verify_password(db_user.db_password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    access_token = create_access_token(data={"sub": db_user.name})
    return {"access_token": access_token, "token_type": "bearer"}
