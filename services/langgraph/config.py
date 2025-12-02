from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Configuration - Local Docker URLs
    gateway_service_url: str = "http://gateway:8000"
    gateway_url: str = "http://gateway:8000"  # Alias for tools.py
    api_key_secret: str = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    
    # Production URLs (Reference only)
    langgraph_service_url: str = "http://langgraph:9001"
    gateway_production_url: str = "https://bhiv-hr-gateway-ltg0.onrender.com"
    
    # Database - Local Docker
    database_url: str = "postgresql://bhiv_user:bhiv_local_password_2025@db:5432/bhiv_hr"
    
    # JWT Secrets (Production values)
    jwt_secret_key: str = "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA"
    candidate_jwt_secret_key: str = "candidate_jwt_secret_key_2025"
    
    # Gemini AI (Real credentials)
    gemini_api_key: str = "AIzaSyC8vbb0qAgcFlHw6fA14Ta6Nr7zsG5ELIs"
    gemini_model: str = "gemini-pro"
    
    # Twilio (Real credentials)
    twilio_account_sid: str = "<TWILIO_ACCOUNT_SID>"
    twilio_auth_token: str = "<TWILIO_AUTH_TOKEN>"
    twilio_whatsapp_number: str = "+14155238886"
    
    # Gmail (Real credentials)
    gmail_email: str = "shashankmishra0411@gmail.com"
    gmail_app_password: str = "krho jird yikm huzy"
    
    # Telegram (Updated real credentials)
    telegram_bot_token: str = "8260513283:AAFoYOeQKEcYdoFOtBTi7ZgsuPt_YNlgvCo"
    telegram_bot_username: str = "BHIV_HR_PLATFORM_ASSISTANT_bot"
    
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