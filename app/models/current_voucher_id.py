from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Current_voucher(Base):
    __tablename__ = "current_voucher";
    current_voucher_id = Column(Integer, primary_key=True, index=True);
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False);
    voucher_type_id = Column(Integer, ForeignKey("voucher_types.voucher_type_id"), nullable=False);
    purchase_id = Column(Integer, ForeignKey("purchases.purchase_id"), nullable=False);
    period = Column(Integer, nullable=False);
    status = Column(String);
    pass