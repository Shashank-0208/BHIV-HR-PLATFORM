from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Configuration - Use environment variables
    gateway_service_url: str = "http://localhost:8000"
    gateway_url: str = "http://localhost:8000"  # Alias for tools.py
    api_key_secret: str = "<YOUR_API_KEY>"
    
    # Production URLs
    langgraph_service_url: str = "https://bhiv-hr-langgraph.onrender.com"
    gateway_production_url: str = "https://bhiv-hr-gateway-ltg0.onrender.com"
    
    # Database - Use environment variable with fallback
    database_url: str = "postgresql://bhiv_user:your_password@db:5432/bhiv_hr"
    
    # JWT Secrets (must match gateway service)
    jwt_secret_key: str = "<YOUR_JWT_SECRET>"
    candidate_jwt_secret_key: str = "<YOUR_CANDIDATE_JWT_SECRET>"
    
    # Gemini AI
    gemini_api_key: str = "<YOUR_GEMINI_API_KEY>"
    gemini_model: str = "gemini-pro"
    
    # Twilio
    twilio_account_sid: str = "<YOUR_TWILIO_ACCOUNT_SID>"
    twilio_auth_token: str = "<YOUR_TWILIO_AUTH_TOKEN>"
    twilio_whatsapp_number: str = "<YOUR_WHATSAPP_NUMBER>"
    
    # Gmail
    gmail_email: str = "<YOUR_GMAIL_EMAIL>"
    gmail_app_password: str = "<YOUR_GMAIL_APP_PASSWORD>"
    
    # Telegram
    telegram_bot_token: str = "<YOUR_TELEGRAM_BOT_TOKEN>"
    telegram_bot_username: str = "<YOUR_TELEGRAM_BOT_USERNAME>"
    
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