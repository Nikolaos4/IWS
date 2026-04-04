from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class ShopProfile(Base):
    __tablename__ = "shop_profiles"

    shop_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    shop_name = Column(String, nullable=False)
    premium_sub = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="shop_profile")
    shop_voucher_type = relationship("ShopVoucherType", back_populates="shop_profile")
