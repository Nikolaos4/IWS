from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.db.database import Base

class ShopProfile(Base):
    __tablename__ = "shop_profiles"

    shop_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    shop_name = Column(String, nullable=False)
    premium_sub = Column(Boolean, default=False)