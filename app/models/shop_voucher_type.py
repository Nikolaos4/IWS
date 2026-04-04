from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ShopVoucherType(Base): 
    __tablename__ = "shop_prifile_types";
    shop_voucher_id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shop_profiles.shop_id"), nullable=False)
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.voucher_type_id"), nullable=False)

    shop_profile = relationship("ShopProfile", back_populates="shop_voucher_type")
    voucher_type = relationship("VoucherType", back_populates="shop_voucher_type")
