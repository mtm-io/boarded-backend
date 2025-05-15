import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    hosted_games = relationship("HostedGame", back_populates="host_user")
