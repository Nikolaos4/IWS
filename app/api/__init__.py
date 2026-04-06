from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.purchases import router as purchases_router
from app.api.vouchers import router as vouchers_router
from app.api.voucher_types import router as voucher_types_router 
from app.api.shop_profile import router as shop_profile_router 
from app.api.choose_voucher import router as choose_voucher_router 

__all__ = [
    "auth_router", 
    "users_router", 
    "purchases_router", 
    "vouchers_router",
    "voucher_types_router"  
    "shop_profile_router", 
    "choose_voucher_router "
]