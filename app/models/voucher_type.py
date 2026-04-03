from sqlalchemy import Column, Integer, String,  ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base 

class VoucherType(Base):
    __tablename__ = "voucher_types"
    voucher_type_id = Column(Integer, primary_key=True, index=True)
    voucher_name = Column(String, nullable=False)
    discount = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="voucher_types")
    purchases = relationship("Purchase", back_populates="voucher_type")

