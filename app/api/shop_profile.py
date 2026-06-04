from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.shop_profile import ShopProfile
from app.models.shop_voucher_type import ShopVoucherType
from app.models.voucher_type import VoucherType
from app.schemas.shop_profile import CreateShopProfile, ShopProfileResponse
from app.schemas.voucher_type import VoucherTypeResponse
from app.api.auth import get_current_user

from typing import List

router = APIRouter(prefix="/shop_profile", tags=["shop_profile"])


@router.get("", response_model=List[ShopProfileResponse])
async def get_all_shops(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    shops = db.query(ShopProfile).offset(skip).limit(limit).all()
    return shops

@router.post("", response_model=ShopProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_shop_profile(
    shop_data: CreateShopProfile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if (current_user.user_role != "shop"):
        raise HTTPException (
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only shop can have a profile"
        )
    
    existing_shop_name = db.query(ShopProfile).filter(ShopProfile.shop_name == shop_data.shop_name).first()

    if existing_shop_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shop with this name already exists"
        )

    db_shop_profile = ShopProfile(
        user_id=current_user.user_id,
        shop_name=shop_data.shop_name,
        premium_sub=shop_data.premium_sub
    )

    db.add(db_shop_profile)
    db.commit()
    db.refresh(db_shop_profile)

    return db_shop_profile



@router.get("/{shop_id}", response_model=List[VoucherTypeResponse])
async def get_shop_vouchers(
    shop_id: int,
    db: Session = Depends(get_db)
):
    current_shop = db.query(ShopProfile).filter(ShopProfile.shop_id == shop_id).first()
    if not(current_shop):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    
    shop_voucher_types = db.query(ShopVoucherType).filter(ShopVoucherType.shop_id == shop_id).all()

    voucher_type_ids = [svt.voucher_type_id for svt in shop_voucher_types]

    all_voucher_types = db.query(VoucherType).filter(VoucherType.voucher_type_id.in_(voucher_type_ids)).all()

    return all_voucher_types
