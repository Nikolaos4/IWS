from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.voucher_pasport import VoucherPasport
from app.schemas.voucher_pasport import VoucherPasportResponse

router = APIRouter(prefix="/voucher_pasport", tags=["voucher_pasport"])

@router.get("", response_model=List[VoucherPasportResponse])
async def get_voucher_pasports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if (current_user.user_role != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="only admins can view voucher passports"
        )
    
    pasports = db.query(VoucherPasport).all()
    return pasports