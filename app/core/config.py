import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "Parts Unlimited API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./parts_unlimited.db")

    # API settings
    API_V1_STR: str = "/api/v1"

    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]  # In production, specify actual origins


settings = Settings()