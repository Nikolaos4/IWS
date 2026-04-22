from pydantic import BaseModel, Field
from typing import Optional

class VoucherPasportResponse(BaseModel):
    voucher_pasport_id: int = Field(...)
    purchase_id: int = Field(...)
    order_id: Optional[int] = None