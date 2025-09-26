from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession # Changed from Session
from typing import AsyncGenerator # Added for async generator

from app.crud import user as crud_user
from app.models import user as model_user
from app.schemas import token as schema_token
from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import AsyncSessionLocal # Changed from SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_db() -> AsyncGenerator[AsyncSession, None]: # Changed to async
    async with AsyncSessionLocal() as session: # Changed to async with
        yield session # Changed to yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)): # Changed db type hint
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schema_token.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    user = await crud_user.get_user(db, user_id=int(token_data.id)) # crud_user.get_user needs to be awaited
    if user is None:
        raise credentials_exception
    return user

def role_middleware(role: str):
    async def check_role(current_user: model_user.User = Depends(get_current_user)): # Changed to async
        print(current_user.role.value)
        if current_user.role.value != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"The user does not have the required {role} role"
            )
        return current_user
    return check_role
