from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base

class VoucherPasport(Base):
    __tablename__ = "voucher_pasports"
    voucher_pasport_id = Column(Integer, primary_key=True, index = True)
    purchase_id = Column(Integer, ForeignKey("purchases.purchase_id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)

    purchase = relationship("Purchase", back_populates="voucher_pasport")
    order = relationship("Order", back_populates="voucher_pasport")
