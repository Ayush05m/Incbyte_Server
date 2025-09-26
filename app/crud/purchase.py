from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseCreate
from app.models.sweet import Sweet
from app.utils.razorpay_utils import client

async def create_purchase(db: AsyncSession, purchase: PurchaseCreate, user_id: int):
    result = await db.execute(select(Sweet).filter(Sweet.id == purchase.sweet_id))
    sweet = result.scalars().first()
    if not sweet:
        return None

    total_price = sweet.price * purchase.quantity

    order_data = {
        "amount": int(total_price * 100),  # Amount in paise
        "currency": "INR",
        "receipt": f"receipt_order_{user_id}_{purchase.sweet_id}",
    }

    order = client.order.create(data=order_data)

    db_purchase = Purchase(
        user_id=user_id,
        sweet_id=purchase.sweet_id,
        quantity=purchase.quantity,
        total_price=total_price,
        order_id=order["id"],
    )
    db.add(db_purchase)
    await db.commit()
    await db.refresh(db_purchase)
    return db_purchase, order

async def verify_payment(db: AsyncSession, order_id: str, payment_id: str, signature: str):
    try:
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        client.utility.verify_payment_signature(params_dict)
        # Payment is successful, update purchase status if needed
        # For now, we are not updating any status
        return True
    except Exception as e:
        return False
