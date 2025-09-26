from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sweet_id = Column(Integer, ForeignKey("sweets.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    purchase_date = Column(DateTime, default=datetime.utcnow)
    order_id = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="purchases")
    sweet = relationship("Sweet", back_populates="purchases")
