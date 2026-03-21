from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.purchase import Purchase
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/purchases", tags=["purchases"])

# Цена одного талона в копейках (100 рублей = 10000 копеек)
PRICE_PER_VOUCHER = 10000  # 100 рублей

@router.post("", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase(
    purchase_data: PurchaseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Купить талоны.
    
    - Увеличивает баланс пользователя
    - Создаёт запись в таблице покупок
    - Возвращает данные о покупке
    """
    
    # Проверяем, что пользователь — покупатель (не магазин)
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can purchase vouchers"
        )
    
    # Создаём запись о покупке
    db_purchase = Purchase(
        user_id=current_user.id,
        voucher_count=purchase_data.voucher_count,
        price=purchase_data.voucher_count * PRICE_PER_VOUCHER,
        status="completed"
    )
    
    # Обновляем баланс пользователя
    current_user.voucher_balance += purchase_data.voucher_count
    
    # Сохраняем изменения в БД
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    
    return db_purchase