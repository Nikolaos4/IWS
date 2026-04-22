from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class Order(Base):
    __tablename__ = "orders";
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shop_profiles.shop_id"), nullable=False)
    voucher_pasport_id = Column(Integer, ForeignKey("voucher_pasports.voucher_pasport_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="order")
    shop = relationship("ShopProfile", back_populates="order")
    voucher_pasport = relationship("VoucherPasport", back_populates="order")