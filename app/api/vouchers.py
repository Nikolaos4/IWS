from fastapi import APIRouter, Depends
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/vouchers", tags=["vouchers"])

@router.get("/balance")
async def get_voucher_balance(current_user: User = Depends(get_current_user)):
    """
    Получить текущий баланс талонов.
    
    Возвращает количество доступных талонов.
    """
    return {"balance": current_user.voucher_balance}

@router.get("")
async def get_my_vouchers(current_user: User = Depends(get_current_user)):
    """
    Получить список всех талонов пользователя.
    
    Пока возвращает только баланс. В будущем здесь будет список конкретных талонов.
    """
    return {
        "total_balance": current_user.voucher_balance,
        "vouchers": []  # TODO: добавить модель Voucher
    }