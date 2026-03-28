from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class Blocking(Base):
    __tablename__ = "blocking"

    user_id = Column(Integer, ForeignKey("users.id"))
    blocking_by = Column(Integer, ForeignKey("users.id"))
    reason = Column(String, nullable=True)