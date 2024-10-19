import os
from datetime import timedelta

class Settings:
    PROJECT_NAME: str = "FastMSG"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "test1234")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5433)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fast_msg")
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "test")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_TIME = timedelta(minutes=480)


settings = Settings()
