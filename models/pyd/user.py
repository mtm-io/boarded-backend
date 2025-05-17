from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr | None = None

class UserInDB(User):
    hashed_password: str | None = None
    id: str | None = None

class UserIn(User):
    password: str


class RefreshToken(BaseModel):
    refresh_token: str