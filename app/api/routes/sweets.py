from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession # Changed from Session
from typing import List, Optional

from app.crud import sweet as crud_sweet
from app.schemas import sweet as schema_sweet
from app.api import deps
from app.models.user import User
from app.api.response_util import standard_response
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", dependencies=[Depends(deps.get_current_user)])
async def create_sweet(
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    imageUrl: Optional[str] = Form(None),
    image_file: UploadFile = File(None),
    db: AsyncSession = Depends(deps.get_db)
): # Made async, db: AsyncSession
    sweet = schema_sweet.SweetCreate(
        name=name,
        category=category,
        description=description,
        price=price,
        quantity=quantity,
        imageUrl=imageUrl
    )
    logger.info(f"Creating sweet with data: {sweet}")
    if image_file:
        logger.info(f"Image file provided: {image_file.filename}")
    db_sweet = await crud_sweet.get_sweet_by_name(db, name=sweet.name) # Added await
    if db_sweet:
        return standard_response(False, "Sweet name already registered", data=None, error="Sweet name already registered")
    sweet_obj = await crud_sweet.create_sweet(db=db, sweet=sweet, image_file=await image_file.read() if image_file else None) # Added await
    return standard_response(True, "Sweet created successfully", data=sweet_obj)

@router.get("/", dependencies=[Depends(deps.get_current_user)])
async def read_sweets(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(deps.get_db)): # Made async, db: AsyncSession
    sweets = await crud_sweet.get_sweets(db, skip=skip, limit=limit) # Added await
    return standard_response(True, "Sweets fetched successfully", data=sweets)

@router.get("/search", dependencies=[Depends(deps.get_current_user)])
async def search_sweets( # Made async
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(deps.get_db) # db: AsyncSession
):
    sweets = await crud_sweet.search_sweets(db, name=name, category=category, min_price=min_price, max_price=max_price) # Added await
    return standard_response(True, "Sweets search successful", data=sweets)

@router.put("/{sweet_id}", dependencies=[Depends(deps.role_middleware("admin"))])
async def update_sweet(
    sweet_id: int,
    name: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    quantity: Optional[int] = Form(None),
    imageUrl: Optional[str] = Form(None),
    image_file: UploadFile = File(None),
    db: AsyncSession = Depends(deps.get_db)
): # Made async, db: AsyncSession
    sweet = schema_sweet.SweetUpdate(
        name=name,
        category=category,
        description=description,
        price=price,
        quantity=quantity,
        imageUrl=imageUrl
    )
    logger.info(f"Updating sweet with id {sweet_id} with data: {sweet}")
    if image_file:
        logger.info(f"Image file provided: {image_file.filename}")
    db_sweet = await crud_sweet.get_sweet(db, sweet_id=sweet_id) # Added await
    if not db_sweet:
        return standard_response(False, "Sweet not found", data=None, error="Sweet not found")
    sweet_obj = await crud_sweet.update_sweet(db=db, sweet_id=sweet_id, sweet=sweet, image_file=await image_file.read() if image_file else None) # Added await
    return standard_response(True, "Sweet updated successfully", data=sweet_obj)

@router.delete("/{sweet_id}", response_model=schema_sweet.Sweet, dependencies=[Depends(deps.role_middleware("admin"))])
async def delete_sweet(sweet_id: int, db: AsyncSession = Depends(deps.get_db)): # Made async, db: AsyncSession
    db_sweet = await crud_sweet.get_sweet(db, sweet_id=sweet_id) # Added await
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return await crud_sweet.delete_sweet(db=db, sweet_id=sweet_id)

@router.post("/{sweet_id}/restock", response_model=schema_sweet.Sweet, dependencies=[Depends(deps.role_middleware("admin"))])
async def restock_sweet(sweet_id: int, restock: schema_sweet.SweetRestock, db: AsyncSession = Depends(deps.get_db)): # Made async, db: AsyncSession
    db_sweet = await crud_sweet.restock_sweet(db, sweet_id=sweet_id, quantity=restock.quantity) # Added await
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return db_sweet
