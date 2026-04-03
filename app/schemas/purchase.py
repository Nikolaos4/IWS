from pydantic import BaseModel, Field
from datetime import datetime

class PurchaseBase(BaseModel):
    voucher_type_id: int
    voucher_count: int = Field(..., gt=0, le=100, description="Количество талонов (от 1 до 100)")

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseResponse(PurchaseBase):
    purchase_id: int
    user_id: int
    all_price: int  
    period: int
    created_at: datetime

    class Config:
        from_attributes = True  