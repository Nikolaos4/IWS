from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.models.purchase import Purchase
from app.models.voucher_type import VoucherType
from app.models.user_balance import UserBalance
from app.models.voucher_pasport import VoucherPasport
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/purchases", tags=["purchases"])


@router.get("/my", response_model=List[PurchaseResponse])
async def get_my_purchases(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    purchases = db.query(Purchase).filter(Purchase.user_id == current_user.user_id).all()
    return purchases


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
    if current_user.user_role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can purchase vouchers"
        )
    

    voucher_type = db.query(VoucherType).filter(VoucherType.voucher_type_id == purchase_data.voucher_type_id).first()
    
    if not voucher_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher type not found"
        )

    # Создаём запись о покупке
    db_purchase = Purchase(
        user_id=current_user.user_id,
        voucher_type_id=purchase_data.voucher_type_id,
        period=30 # временно, потом добавим выбор срока
    )
    db.add(db_purchase)
    db.flush()
    for i in range(purchase_data.voucher_count):
        db_voucher_pasport = VoucherPasport(
            purchase_id=db_purchase.purchase_id
        )
        db.add(db_voucher_pasport)

    # Обновляем баланс пользователя
    user_balance = db.query(UserBalance).filter(
        UserBalance.user_id == current_user.user_id,
        UserBalance.voucher_type_id == purchase_data.voucher_type_id
    ).first()

    if user_balance:
        user_balance.voucher_count += purchase_data.voucher_count

    else:
        db_balance = UserBalance(
            user_id=current_user.user_id,
            voucher_type_id=purchase_data.voucher_type_id,
            voucher_count=purchase_data.voucher_count
        )
        db.add(db_balance)   

    # Сохраняем изменения в БД
    db.commit()
    db.refresh(db_purchase)
    
    return db_purchase