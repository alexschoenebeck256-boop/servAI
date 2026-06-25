import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ServAI API"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "servai")
    SQLALCHEMY_DATABASE_URI: Optional[str] = os.getenv("DATABASE_URL")

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    VECTOR_DB_URL: str = os.getenv("VECTOR_DB_URL", "http://localhost:8001")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "mock-key")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "mock-key")

    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "mock-sid")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "mock-token")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")

    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", os.getenv("STRIPE_API_KEY", "mock-key"))

    SERVICETITAN_CLIENT_ID: str = os.getenv("SERVICETITAN_CLIENT_ID", "")
    SERVICETITAN_CLIENT_SECRET: str = os.getenv("SERVICETITAN_CLIENT_SECRET", "")
    SERVICETITAN_TENANT_ID: str = os.getenv("SERVICETITAN_TENANT_ID", "")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SQLALCHEMY_DATABASE_URI:
            self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
