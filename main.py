from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.core.config import settings
from app.models import user, voucher_type, purchase, shop_voucher_type, user_balance, voucher_pasport, order, refresh_token
from app.api import auth_router, users_router, purchases_router, vouchers_router, voucher_types_router, shop_profile_router, news_router, choose_voucher_router, voucher_pasport_router, order_router


# Создаём таблицы в базе данных (только для разработки!)
# Если таблицы уже существуют, они не будут пересозданы
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables ready!")

# Создаём экземпляр приложения FastAPI
app = FastAPI(
    title="Talon App API",
    description="API для приложения с талонами на скидки",
    version="0.1.0",
    docs_url="/docs",      # документация Swagger
    redoc_url="/redoc"     # альтернативная документация ReDoc
)

# Настройка CORS (Cross-Origin Resource Sharing)
# Разрешает фронтенду (например, React приложению) обращаться к нашему API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры с префиксом /api/v1
# Теперь все эндпоинты будут доступны по адресу /api/v1/...
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(purchases_router, prefix="/api/v1")
app.include_router(vouchers_router, prefix="/api/v1")
app.include_router(voucher_types_router, prefix="/api/v1")
app.include_router(shop_profile_router, prefix="/api/v1")
app.include_router(news_router, prefix="/api/v1")
app.include_router(choose_voucher_router, prefix="/api/v1")
app.include_router(voucher_pasport_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")

# Корневой эндпоинт (проверка, что сервер работает)
@app.get("/")
async def root():
    return {
        "message": "Welcome to Talon App API",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_v1": "/api/v1"
    }

# Эндпоинт для проверки здоровья сервера
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Talon App API"}

# Если запускаем файл напрямую (не через uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True          
    )