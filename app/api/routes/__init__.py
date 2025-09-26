from app.api.routes import auth, users, sweets, purchases

from fastapi import APIRouter
router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(sweets.router, prefix="/sweets", tags=["sweets"])
router.include_router(purchases.router, prefix="/purchases", tags=["purchases"])
