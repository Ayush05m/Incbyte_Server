from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.purchase import PurchaseCreate
from app.crud.purchase import create_purchase, verify_payment
from app.models.user import User
from app.api.response_util import standard_response

router = APIRouter()

@router.post("/initiate")
async def initiate_purchase(
    *, 
    db: AsyncSession = Depends(deps.get_db),
    purchase_in: PurchaseCreate,
    current_user: User = Depends(deps.get_current_user)
):
    purchase, order = await create_purchase(db=db, purchase=purchase_in, user_id=current_user.id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Sweet not found")
    return standard_response(True, "Purchase initiated successfully", data={"purchase": purchase, "order": order})

@router.post("/verify")
async def verify_payment_endpoint(
    *, 
    db: AsyncSession = Depends(deps.get_db),
    order_id: str,
    payment_id: str,
    signature: str
):
    if not await verify_payment(db=db, order_id=order_id, payment_id=payment_id, signature=signature):
        raise HTTPException(status_code=400, detail="Payment verification failed")
    return standard_response(True, "Payment successful", data=None)
