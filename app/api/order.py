from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.db.database import get_db
from app.models.user import User
from app.models.user_balance import UserBalance
from app.models.shop_profile import ShopProfile
from app.models.shop_voucher_type import ShopVoucherType
from app.models.purchase import Purchase
from app.models.voucher_type import VoucherType
from app.models.voucher_pasport import VoucherPasport
from app.models.order import Order
from app.schemas.order import CreateOrder, OrderResponse
from app.api.auth import get_current_user


router = APIRouter(prefix="/order", tags=["order"])

@router.post("", response_model=OrderResponse)
async def make_order(
    order_data: CreateOrder,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_role != "customer":
        raise HTTPException (
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can use vouchers in the store"
        )
    
    current_voucher_pasport = db.query(VoucherPasport).filter(VoucherPasport.voucher_pasport_id == order_data.voucher_pasport_id).first()
    if not(current_voucher_pasport) or (current_voucher_pasport.order_id != None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher not found or has already been used"
        )
    
    purch_of_voucher = db.query(Purchase).filter(Purchase.purchase_id == current_voucher_pasport.purchase_id).first()
    if (purch_of_voucher.user_id != current_user.user_id) :
        raise HTTPException (
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have this voucher"
        )

    type_of_voucher = purch_of_voucher.voucher_type_id;

    #Логика для магазина
    shop_voucher = db.query(ShopVoucherType).filter(
        ShopVoucherType.shop_id == order_data.shop_id,
        ShopVoucherType.voucher_type_id == type_of_voucher
    ).first()

    if not shop_voucher:
        raise HTTPException (
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cann't use this voucher type in this store"
        )
    
    db_order = Order(
        user_id=current_user.user_id,
        shop_id=order_data.shop_id,
        voucher_pasport_id=current_voucher_pasport.voucher_pasport_id,
        created_at=datetime.now(timezone.utc) 
    )
    db.add(db_order)
    db.flush()
    current_voucher_pasport.order_id = db_order.order_id

    user_balance = db.query(UserBalance).filter(UserBalance.user_id == current_user.user_id, UserBalance.voucher_type_id == type_of_voucher).first()
    if not user_balance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance for this voucher type"
        )
    user_balance.voucher_count -= 1

    db.commit()
    db.refresh(db_order)
    return db_order
