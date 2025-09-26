from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.sweet import Sweet
from app.schemas.sweet import SweetCreate, SweetUpdate
from app.crud.purchase import create_purchase
from app.schemas.purchase import PurchaseCreate
import logging

logger = logging.getLogger(__name__)

async def get_sweet(db: AsyncSession, sweet_id: int):
    result = await db.execute(select(Sweet).filter(Sweet.id == sweet_id))
    return result.scalar_one_or_none()

async def get_sweet_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(Sweet).filter(Sweet.name.ilike(name)))
    return result.scalar_one_or_none()

async def get_sweets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Sweet).offset(skip).limit(limit))
    return result.scalars().all()

from app.utils.image_uploader import upload_image

async def create_sweet(db: AsyncSession, sweet: SweetCreate, image_file: bytes = None):
    if image_file:
        image_url = await upload_image(image_file)
        if image_url:
            sweet.imageUrl = image_url
        else:
            logger.error("Image upload failed")
            sweet.imageUrl = None
    
    db_sweet = Sweet(**sweet.dict())
    db.add(db_sweet)
    try:
        await db.commit()
        await db.refresh(db_sweet)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating sweet: {e}")
        return None
    return db_sweet

async def search_sweets(db: AsyncSession, name: Optional[str] = None, category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    query = select(Sweet)
    if name:
        query = query.filter(Sweet.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Sweet.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(Sweet.price >= min_price)
    if max_price is not None:
        query = query.filter(Sweet.price <= max_price)
    result = await db.execute(query)
    return result.scalars().all()

async def update_sweet(db: AsyncSession, sweet_id: int, sweet: SweetUpdate, image_file: bytes = None):
    db_sweet = await get_sweet(db, sweet_id)
    if db_sweet:
        update_data = sweet.dict(exclude_unset=True)
        
        if image_file:
            image_url = await upload_image(image_file)
            if image_url:
                db_sweet.imageUrl = image_url
                if 'imageUrl' in update_data:
                    del update_data['imageUrl']
            else:
                logger.error("Image upload failed during update")

        for key, value in update_data.items():
            setattr(db_sweet, key, value)
        
        try:
            await db.commit()
            await db.refresh(db_sweet)
        except Exception as e:
            await db.rollback()
            logger.error(f"Error updating sweet: {e}")
            return None
    return db_sweet

async def delete_sweet(db: AsyncSession, sweet_id: int):
    db_sweet = await get_sweet(db, sweet_id)
    if db_sweet:
        await db.delete(db_sweet)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            logger.error(f"Error deleting sweet: {e}")
            return None
    return db_sweet

async def purchase_sweet(db: AsyncSession, sweet_id: int, quantity: int, user_id: int):
    db_sweet = await get_sweet(db, sweet_id)
    if not db_sweet:
        return None
    if db_sweet.quantity < quantity:
        raise ValueError("Not enough stock")
    db_sweet.quantity -= quantity
    purchase = PurchaseCreate(sweet_id=sweet_id, quantity=quantity)
    await create_purchase(db, purchase, user_id)
    try:
        await db.commit()
        await db.refresh(db_sweet)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error purchasing sweet: {e}")
        return None
    return db_sweet

async def restock_sweet(db: AsyncSession, sweet_id: int, quantity: int):
    db_sweet = await get_sweet(db, sweet_id)
    if not db_sweet:
        return None
    db_sweet.quantity += quantity
    try:
        await db.commit()
        await db.refresh(db_sweet)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error restock_sweet: {e}")
        return None
    return db_sweet
