from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.shop_profile import ShopProfile
from app.schemas.shop_profile import CreateShopProfile, ShopProfileResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/shop_profile", tags=["shop_profile"])

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
