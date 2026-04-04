from pydantic import BaseModel, Field

class ShopProfileBase(BaseModel):
    shop_name: str = Field(..., min_length=0, max_length=100, description="Название магазина (от 1 до 100)")
    premium_sub: bool = Field(default=False, description="Премиум-подписка")

class CreateShopProfile(ShopProfileBase):
    pass

class ShopProfileResponse(ShopProfileBase):
    shop_id: int
    user_id: int
    
    class Config:
        from_attributes = True 