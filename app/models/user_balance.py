from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserBalance(Base):
    __tablename__ = "user_balance";
    user_balance_id = Column(Integer, primary_key=True, index=True);
    user_id = Column(Integer, ForeignKey("users.user_id"));
    voucher_type_id = Column(Integer,  ForeignKey("voucher_types.voucher_type_id"), nullable=False);
    voucher_count = Column(Integer, nullable=False);

    user = relationship("User", back_populates="user_balance");
    voucher_type = relationship("VoucherType", back_populates="user_balance")

