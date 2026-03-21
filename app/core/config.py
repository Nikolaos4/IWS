import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/talon_app")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()