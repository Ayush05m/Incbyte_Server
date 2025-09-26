from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base

class Sweet(Base):
    __tablename__ = 'sweets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    imageUrl = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    purchases = relationship("Purchase", back_populates="sweet")
