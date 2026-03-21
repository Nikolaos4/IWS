from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.purchases import router as purchases_router
from app.api.vouchers import router as vouchers_router

__all__ = [
    "auth_router", 
    "users_router", 
    "purchases_router", 
    "vouchers_router"
]