from pydantic import BaseModel, Field
from datetime import datetime

class PurchaseBase(BaseModel):
    user_id: int
    voucher_type_id: int
    voucher_count: int = Field(..., gt=0, le=100, description="Количество талонов (от 1 до 100)")

class PurchaseCreate(PurchaseBase):
    pass

class PurchaseResponse(PurchaseBase):
    id: int
    user_id: int
    price: int  # в копейках
    status: str
    created_at: datetime

    class Config:
        from_attributes = True  