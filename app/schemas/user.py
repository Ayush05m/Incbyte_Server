from pydantic import BaseModel
from app.models.user import UserRole
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(BaseModel):
    id: int
    role: UserRole
    createdAt: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
