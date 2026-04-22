from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.auth import get_current_user
from app.models.user import User
from app.models.user_balance import UserBalance
from app.schemas.user_balance import BalanceResponse
from app.db.database import get_db

router = APIRouter(prefix="/vouchers", tags=["vouchers"])

@router.get("/balance", response_model=list[BalanceResponse])
def get_voucher_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_balances = db.query(UserBalance).filter(
        UserBalance.user_id == current_user.user_id
    ).all()   # получаем все записи баланса пользователя

    result = []
    for balance in user_balances:
        result.append(BalanceResponse(
            user_id=current_user.user_id,
            voucher_type_id=balance.voucher_type_id,
            voucher_counter=balance.voucher_count   # количество, а не ID
        ))
    return result