from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    purchase_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    vouch_type_id = Column(Integer, ForeignKey("voucher_types.vouch_type_id"), nullable=False)
    voucher_count = Column(Integer, nullable=False)
    all_price = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="purchases")
    voucher_type = relationship("VoucherType", back_populates="purchases")


