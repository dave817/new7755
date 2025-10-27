"""
Configuration settings for the dating chatbot
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # SenseChat API credentials
    SENSENOVA_ACCESS_KEY_ID: str
    SENSENOVA_SECRET_ACCESS_KEY: str
    SENSENOVA_API_KEY: str
    MODEL_NAME: str = "SenseChat-Character-Pro"

    # API endpoints
    API_BASE_URL: str = "https://api.sensenova.cn/v1/llm"
    CHARACTER_CHAT_ENDPOINT: str = "/character/chat-completions"

    # Database
    DATABASE_URL: str = "sqlite:///./dating_chatbot.db"

    # API settings
    MAX_NEW_TOKENS: int = 1024
    RATE_LIMIT_RPM: int = 60
    TOKEN_EXPIRY_SECONDS: int = 1800  # 30 minutes

    # LINE Bot Configuration
    LINE_CHANNEL_SECRET: str = ""
    LINE_CHANNEL_ACCESS_TOKEN: str = ""
    LINE_BOT_NAME: str = "纏綿悱惻 - 聊出激情吧!"
    LINE_BOT_DESCRIPTION: str = "The most interesting dating chatbot on LINE"

    # Application URLs
    APP_BASE_URL: str = "http://localhost:8000"
    SETUP_UI_PATH: str = "/ui2"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Feature Flags
    FREE_MESSAGES_PER_DAY: int = 20
    PREMIUM_PRICE_USD: float = 9.99
    REFERRALS_FOR_UNLIMITED: int = 2  # Refer 2 friends → unlimited messages

    # CORS
    CORS_ORIGINS: list = ["*"]

    # Monitoring (optional)
    SENTRY_DSN: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
