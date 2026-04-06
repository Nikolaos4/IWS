from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.voucher_type import VoucherType
from app.models.shop_voucher_type import ShopVoucherType
from app.models.user import User
from app.models.shop_profile import ShopProfile
from app.schemas.shop_voucher_type import ChooseShopVoucherType, ShopVoucherTypeItem, ShopVoucherTypeResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/choose_voucher", tags=["choose_voucher"])

@router.post("", response_model=ShopVoucherTypeResponse)
async def add_voucher_types_to_shop(
    shop_vouchers: ChooseShopVoucherType,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_role != "shop":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only shop can choose a profile"
        )
    
    user_shop = db.query(ShopProfile).filter(ShopProfile.user_id == current_user.user_id).first()

    if not user_shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user does not have a shop"
        )
    
    add_voucher = []
    for vt_id in shop_vouchers.voucher_type_ids:
        current_vt = db.query(VoucherType).filter(VoucherType.voucher_type_id == vt_id).first()
        if not(current_vt):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This type of voucher does not exist"
            )
        
        existing = db.query(ShopVoucherType).filter(ShopVoucherType.voucher_type_id == vt_id, ShopVoucherType.shop_id == user_shop.shop_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This type of voucher has already been selected"
            )
        
        shop_voucher = ShopVoucherType(
            shop_id=user_shop.shop_id,
            voucher_type_id=vt_id
        )
        db.add(shop_voucher)
        add_voucher.append(shop_voucher)
    db.commit()

    for item in add_voucher:
        db.refresh(item)

    return ShopVoucherTypeResponse(
        shop_id=user_shop.shop_id,
        added_vouchers=[ShopVoucherTypeItem(voucher_id=v.voucher_type_id) for v in add_voucher]
    )
