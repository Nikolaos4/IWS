from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone  

from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    user_role = Column(String, default="customer")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
        
    purchases = relationship("Purchase", back_populates="user")
    voucher_types = relationship("VoucherType", back_populates="user")
    shop_profile = relationship("ShopProfile", back_populates="user")
    user_balance = relationship("UserBalance", back_populates="user")
    order = relationship("Order", back_populates="user")
    