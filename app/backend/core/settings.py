from pydantic_settings import BaseSettings
from pydantic import validator
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Qdrant Vector Database
    QDRANT_URL: str
    
    # Together AI
    TOGETHER_API_KEY: str
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # API Settings
    API_TITLE: str = "AREADERA API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Celery Settings
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())