from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.user import UserResponse
from app.schemas.user_balance import BalanceItem
from app.api.auth import get_current_user
from app.models.user import User
from app.models.user_balance import UserBalance

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/me/balance", response_model=List[BalanceItem])
async def get_my_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(UserBalance).filter(UserBalance.user_id == current_user.user_id).all()