from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.purchase import Purchase
from app.models.voucher_pasport import VoucherPasport
from app.schemas.voucher_pasport import VoucherPasportResponse

router = APIRouter(prefix="/voucher_pasport", tags=["voucher_pasport"])


@router.get("/my", response_model=List[VoucherPasportResponse])
async def get_my_voucher_pasports(
    used: bool = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    purchase_ids = db.query(Purchase.purchase_id).filter(
        Purchase.user_id == current_user.user_id
    ).subquery()

    query = db.query(VoucherPasport).filter(
        VoucherPasport.purchase_id.in_(purchase_ids)
    )

    if used is True:
        query = query.filter(VoucherPasport.order_id.isnot(None))
    elif used is False:
        query = query.filter(VoucherPasport.order_id.is_(None))

    return query.all()


@router.get("", response_model=List[VoucherPasportResponse])
async def get_all_voucher_pasports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all voucher passports"
        )

    return db.query(VoucherPasport).all()