import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# Load environment variables from .env file
load_dotenv()

# ----------------------------------------------------------------------
# ✅ 1. Parse and validate DATABASE_URL
# ----------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL environment variable is not set")

# Ensure it uses asyncpg for async support
if not DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# ----------------------------------------------------------------------
# ✅ 2. Remove incompatible query parameters for asyncpg
# ----------------------------------------------------------------------
parsed_url = urlparse(DATABASE_URL)
query_params = parse_qs(parsed_url.query)

# Remove unsupported asyncpg parameters
query_params.pop('sslmode', None)
query_params.pop('channel_binding', None)

# Rebuild query string
new_query_string = urlencode(query_params, doseq=True)
DATABASE_URL = urlunparse(parsed_url._replace(query=new_query_string))

# ----------------------------------------------------------------------
# ✅ 3. Create async SQLAlchemy engine
# ----------------------------------------------------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=False,           # Set to True only during debugging
    pool_size=10,         # Optional: base pool size
    max_overflow=20,      # Optional: extra connections allowed
    pool_recycle=1800,    # Recycle connections after 30 mins
    pool_pre_ping=True    # Check if connection is alive before using
)

# ----------------------------------------------------------------------
# ✅ 4. Create session maker and base class
# ----------------------------------------------------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

# ----------------------------------------------------------------------
# ✅ 5. Dependency for getting DB session
# ----------------------------------------------------------------------
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
