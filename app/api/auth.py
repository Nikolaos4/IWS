from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings

# Создаём роутер с префиксом /auth и тегом для документации
router = APIRouter(prefix="/auth", tags=["authentication"])

# Настройка OAuth2 схемы для получения токена
# tokenUrl указывает, где находится эндпоинт для логина
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    
    - Проверяет, что email и username не заняты
    - Хеширует пароль
    - Сохраняет пользователя в базу
    - Возвращает данные пользователя (без пароля)
    """
    
    # Проверяем, не занят ли email
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Проверяем, не занят ли username
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Хешируем пароль
    hashed_password = get_password_hash(user_data.password)
    
    # Создаём объект пользователя
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        password=hashed_password,
        user_role=user_data.user_role  # role приходит из схемы, по умолчанию "customer"
    )
    
    # Сохраняем в базу
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Обновляем объект, чтобы получить id и другие поля БД
    
    return db_user  # SQLAlchemy модель автоматически преобразуется в UserResponse


@router.post("/login", response_model = Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not(user) or not(verify_password(form_data.password, user.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not(user.is_active):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Зависимость для получения текущего пользователя по токену.
    
    Используется в других эндпоинтах для авторизации.
    """
    from app.core.security import decode_token
    
    # Декодируем токен
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Извлекаем username из payload
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Ищем пользователя в базе
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.post("/logout")
async def logout():
    """
    Выход из системы.
    
    JWT токены не могут быть отозваны на сервере без черного списка.
    Клиент должен просто удалить токен.
    """
    return {"message": "Successfully logged out"}