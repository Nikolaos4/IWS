from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.models.voucher_type import VoucherType
from app.schemas.voucher_type import VoucherTypeCreate, VoucherTypeUpdate, VoucherTypeResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/voucher-types", tags=["voucher-types"])


@router.post("/", response_model = VoucherTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_voucher_type(
    voucher_type_data: VoucherTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if (current_user.user_role != "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only administrators can create voucher types")
    
    existing_type = db.query(VoucherType).filter(VoucherType.voucher_name == voucher_type_data.voucher_name).first()
    if existing_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Voucher type with this name already exists")
    
    db_voucher_type = VoucherType(
        voucher_name = voucher_type_data.voucher_name,
        discount = voucher_type_data.discount,
        price = voucher_type_data.price,
        created_by = current_user.user_id
    )

    db.add(db_voucher_type)
    db.commit()
    db.refresh(db_voucher_type)

    return db_voucher_type



@router.get("/", response_model=List[VoucherTypeResponse])
async def get_all_voucher_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    voucher_types = db.query(VoucherType).offset(skip).limit(limit).all()
    return voucher_types



@router.get("/{voucher_type_id}", response_model=VoucherTypeResponse)
async def get_voucher_type_by_id(
    voucher_type_id: int,
    db: Session = Depends(get_db)
):
    """
    Получение вида талона по ID.
    """
    voucher_type = db.query(VoucherType).filter(VoucherType.voucher_type_id == voucher_type_id).first()
    if not voucher_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher type not found"
        )
    return voucher_type    



@router.put("/{voucher_type_id}", response_model=VoucherTypeResponse)
async def update_voucher_type(
    voucher_type_id: int,
    voucher_type_data: VoucherTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновление вида талона (только для админа).
    """
    # Проверяем права
    if current_user.user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can update voucher types"
        )
    
    # Находим вид талона
    voucher_type = db.query(VoucherType).filter(VoucherType.voucher_type_id == voucher_type_id).first()
    if not voucher_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher type not found"
        )
    
    # Обновляем поля (только те, которые переданы)
    if voucher_type_data.voucher_name is not None:
        # Проверяем, не занято ли новое имя
        existing = db.query(VoucherType).filter(
            VoucherType.voucher_name == voucher_type_data.voucher_name,
            VoucherType.voucher_type_id != voucher_type_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Voucher type with this name already exists"
            )
        voucher_type.voucher_name = voucher_type_data.voucher_name
    
    if voucher_type_data.discount is not None:
        voucher_type.discount = voucher_type_data.discount
    
    if voucher_type_data.price is not None:
        voucher_type.price = voucher_type_data.price
    
    db.commit()
    db.refresh(voucher_type)
    
    return voucher_type



@router.delete("/{voucher_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voucher_type(
    voucher_type_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Удаление вида талона (только для админа).
    """
    # Проверяем права
    if current_user.user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can delete voucher types"
        )
    
    # Находим вид талона
    voucher_type = db.query(VoucherType).filter(VoucherType.voucher_type_id == voucher_type_id).first()
    if not voucher_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voucher type not found"
        )
    
    if voucher_type.purchases:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Cannot delete voucher type that has purchases"
    )
    
    db.delete(voucher_type)
    db.commit()
    
    return None