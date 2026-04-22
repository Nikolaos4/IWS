from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Базовая схема — общие поля для всех вариантов
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    user_role: str = "customer"  # значение по умолчанию

# Схема для регистрации — добавляет пароль
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

# Схема для входа (отдельно, так как не нужен email и роль)
class UserLogin(BaseModel):
    username: str
    password: str

# Схема для ответа — все поля, которые мы отдаём клиенту (без пароля)
class UserResponse(UserBase):
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # позволяет создавать объект из SQLAlchemy модели (важно!)

# Схемы для JWT токенов
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None