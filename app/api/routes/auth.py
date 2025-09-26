from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession # Changed from Session

from app.crud import user as crud_user
from app.schemas import user as schema_user
from app.schemas import token as schema_token
from app.core.security import create_access_token, verify_password
from app.api import deps
from app.api.response_util import standard_response

router = APIRouter()

@router.post("/register")
async def register(user: schema_user.UserCreate, db: AsyncSession = Depends(deps.get_db)): # Made async, db: AsyncSession
    db_user = await crud_user.get_user_by_email(db, email=user.email) # Added await
    if db_user:
        return standard_response(False, "Email already registered", data=None, error="Email already registered")
    user_obj = await crud_user.create_user(db=db, user=user) # Added await
    return standard_response(True, "User registered successfully", data=user_obj)

@router.post("/login")
async def login(user: schema_user.UserLogin, db: AsyncSession = Depends(deps.get_db)): # Made async, db: AsyncSession
    db_user = await crud_user.get_user_by_email(db, email=user.email) # Added await
    if not db_user or not verify_password(user.password, db_user.passwordHash):
        return standard_response(False, "Incorrect email or password", data=None, error="Incorrect email or password")
    access_token_data = {"sub": str(db_user.id), "role": db_user.role.value}
    access_token = create_access_token(data=access_token_data)
    token = {"access_token": access_token, "token_type": "bearer"}
    return standard_response(True, "Login successful", data=token)
