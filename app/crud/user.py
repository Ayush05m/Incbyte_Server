from sqlalchemy.ext.asyncio import AsyncSession # Changed from Session
from sqlalchemy import select # Added for async queries
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user(db: AsyncSession, user_id: int): # Made async
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str): # Made async
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalar_one_or_none()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100): # Made async
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: UserCreate): # Made async
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, passwordHash=hashed_password, username=user.username)
    db.add(db_user)
    await db.commit() # Await commit
    await db.refresh(db_user) # Await refresh
    return db_user
