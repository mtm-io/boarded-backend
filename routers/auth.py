
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.pyd.user import UserInDB
from dependencies import db_dependency
from models.alchemy.user import User
from models.pyd.user import UserIn, UserInDB
from utils import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, authenticate_user, create_access_token, create_refresh_token, get_password_hash

router = APIRouter(
    tags=["auth"],
)


@router.post('/token', description="Get access token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
        user = await authenticate_user(form_data.username, form_data.password, db)
        if not user:
               raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data= {"sub" : user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

        return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", description="Register a new user")
async def register(user: UserIn, db: db_dependency):
    # check if user already exists
    existing_user = db.query(User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create access token
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

     # Create refresh token
    refresh_token = create_refresh_token(
        data={"sub": db_user.username, "refresh": True},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": db_user.username,
            "email": db_user.email
        }
    }