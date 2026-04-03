from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VoucherTypeBase(BaseModel):
    voucher_name: str = Field(..., min_length=3,max_length=100)
    discount: int = Field(..., ge=0, le=100, description="Скидка в процентах (0-100)")
    price: int = Field(..., ge=0, description="Цена за один талон")

class VoucherTypeCreate(VoucherTypeBase):
    pass

class VoucherTypeUpdate(BaseModel):
    voucher_name: Optional[str] = Field(None, min_length=3, max_length=100)
    discount: Optional[int] = Field(None, ge=0, le=100)
    price: Optional[int] = Field(None, gt=0)

class VoucherTypeResponse(VoucherTypeBase):
    voucher_type_id: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

