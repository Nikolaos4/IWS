from pydantic import BaseModel

class BalanceItem(BaseModel):
    user_balance_id: int
    voucher_type_id: int
    voucher_count: int

    class Config:
        from_attributes = True

class BalanceResponse(BaseModel):
    balances: list[BalanceItem]