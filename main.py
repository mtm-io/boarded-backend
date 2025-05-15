
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import Base, engine
from dependencies import db_dependency
from models.alchemy.user import User
from models.pyd.user import UserIn, UserInDB
from routers import cards, users
from utils import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_password_hash

app = FastAPI()

## binding the database and models from alchemy/ submodule
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(cards.router)


@app.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
        user = await authenticate_user(form_data.username, form_data.password, db)
        if not user:
               raise HTTPException(status_code=400, detail="Incorrect username or password")
        user_db = UserInDB( username=user.username, email=user.email, hashed_password=user.hashed_password)
        access_token = create_access_token(data= {"sub" : user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

        
        return {"access_token": access_token, "token_type": "bearer"}


@app.post("/fake_register")
async def fake_register(user: UserIn, db: db_dependency):
        db_User = User(username=user.username, hashed_password=get_password_hash(user.password), email=user.email)
        db.add(db_User)
        db.commit()

        return {"user": user}