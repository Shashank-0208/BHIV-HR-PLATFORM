from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Configuration - Use environment variables
    gateway_service_url: str = "http://gateway:8000"  # Default for Docker
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
    gemini_api_key: str = "your_gemini_api_key_here"
    gemini_model: str = "gemini-pro"
    
    # Twilio
    twilio_account_sid: str = "your_twilio_account_sid"
    twilio_auth_token: str = "your_twilio_auth_token"
    twilio_whatsapp_number: str = "your_whatsapp_number"
    
    # Gmail
    gmail_email: str = "your_gmail_email"
    gmail_app_password: str = "your_gmail_app_password"
    
    # Telegram
    telegram_bot_token: str = "your_telegram_bot_token"
    telegram_bot_username: str = "your_telegram_bot_username"
    
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