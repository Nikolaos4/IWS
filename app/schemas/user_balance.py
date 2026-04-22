from pydantic import BaseModel

class BalanceBase(BaseModel):
    user_id: int;
    voucher_type_id: int
    voucher_counter: int

class BalanceResponse(BalanceBase):
    pass