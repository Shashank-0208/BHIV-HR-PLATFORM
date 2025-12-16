from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Configuration - Environment Variables
    gateway_service_url: str = "http://gateway:8000"  # Maps to GATEWAY_SERVICE_URL
    api_key_secret: str = ""
    
    # Service URLs
    langgraph_service_url: str = "http://langgraph:9001"
    
    # Database
    database_url: str = ""
    
    # JWT Secrets
    jwt_secret_key: str = ""
    candidate_jwt_secret_key: str = ""
    
    # Gemini AI
    gemini_api_key: str = ""
    gemini_model: str = "gemini-pro"
    
    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_number: str = "+14155238886"
    
    # Gmail
    gmail_email: str = ""
    gmail_app_password: str = ""
    
    # Telegram
    telegram_bot_token: str = ""
    telegram_bot_username: str = ""
    
    # Environment
    environment: str = "production"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Credential validation for production
if settings.environment == "production":
    required = [
        "gemini_api_key",
        "twilio_account_sid",
        "gmail_email",
        "telegram_bot_token"
    ]
    for req in required:
        if not getattr(settings, req):
            logger.warning(f"⚠️ Missing {req} - some features will be unavailable")