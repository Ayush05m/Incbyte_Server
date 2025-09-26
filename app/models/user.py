from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import datetime

from app.db.session import Base

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    passwordHash = Column(String)
    role = Column(Enum(UserRole), default=UserRole.user)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    purchases = relationship("Purchase", back_populates="user")
