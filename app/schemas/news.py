from pydantic import BaseModel, Field
from typing import Optional

class NewsBase(BaseModel):
    title: str = Field(..., max_length=100, description="Заголовок новости")
    content: str = Field(..., description="Текст новости")

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100, description="Заголовок новости")
    content: Optional[str] = Field(None, description="Текст новости")

class NewsCreateResponse(NewsBase):
    news_id: int

    class Config:
        from_attributes = True