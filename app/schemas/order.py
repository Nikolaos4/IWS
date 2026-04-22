from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CreateOrder(BaseModel):
    shop_id: int
    voucher_pasport_id: int

class OrderResponse(CreateOrder):
    user_id: int
    order_id: int
    created_at: datetime