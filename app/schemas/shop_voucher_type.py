from pydantic import BaseModel, Field
from typing import List, Optional

class ChooseShopVoucherType(BaseModel):
    voucher_type_ids: List[int] = Field(..., min_length=1, description="Список ID видов талонов")

class ShopVoucherTypeItem(BaseModel):
    voucher_id: int
    class Config:
        from_attributes = True

class ShopVoucherTypeResponse(BaseModel):
    shop_id: int
    added_vouchers: List[ShopVoucherTypeItem]
    class Config:
        from_attributes = True