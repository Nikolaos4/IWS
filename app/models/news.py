from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class News(Base):
    __tablename__ = "news"

    news_id = Column(Integer, primary_key=True, index=True)

    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)