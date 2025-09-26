from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession # Changed from Session
from typing import List
from app.api.response_util import standard_response

from app.crud import user as crud_user
from app.schemas import user as schema_user
from app.api import deps

router = APIRouter()

@router.get("/")
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(deps.get_db)): # Made async, db: AsyncSession
    users = await crud_user.get_users(db, skip=skip, limit=limit) # Added await
    return standard_response(True, "Users fetched successfully", data=users)

@router.get("/me")
async def read_users_me( # Made async
    current_user: schema_user.User = Depends(deps.get_current_user)
):
    return standard_response(True, "Current user fetched successfully", data=current_user)

@router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(deps.get_db)): # Made async, db: AsyncSession
    db_user = await crud_user.get_user(db, user_id=user_id) # Added await
    if db_user is None:
        return standard_response(False, "User not found", data=None, error="User not found")
    return standard_response(True, "User fetched successfully", data=db_user)
