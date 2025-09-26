from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import Base, engine # Keep engine for metadata creation
from app.api.routes import router
from contextlib import asynccontextmanager # Import asynccontextmanager


# Define an async context manager for application lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown event (optional, but good practice for cleanup)
    # await engine.dispose() # SQLAlchemy handles connection closing automatically


app = FastAPI(lifespan=lifespan) # Pass the lifespan context manager to FastAPI

origins = [
    "http://localhost",
    "http://localhost:32100",
    "https://sweetshop-incubyte.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")