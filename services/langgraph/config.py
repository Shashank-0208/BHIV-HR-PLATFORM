from pydantic_settings import BaseSettings
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API Configuration
    gateway_url: str = "http://localhost:8000"
    api_key_secret: str = "<YOUR_API_KEY>"
    langgraph_port: int = 9001
    
    # Production URLs
    langgraph_production_url: str = "https://bhiv-hr-langgraph.onrender.com"
    gateway_production_url: str = "https://bhiv-hr-gateway-ltg0.onrender.com"
    
    # Database
    database_url: str = "postgresql://bhiv_user:password@localhost:5432/bhiv_hr"
    
    # JWT Secrets (must match gateway service)
    jwt_secret_key: str = "<YOUR_JWT_SECRET_KEY>"
    candidate_jwt_secret: str = "<YOUR_CANDIDATE_JWT_SECRET>"
    
    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    
    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_number: str = ""
    
    # Gmail
    gmail_email: str = ""
    gmail_app_password: str = ""
    
    # Telegram
    telegram_bot_token: str = ""
    telegram_bot_username: str = ""
    
    # Environment
    environment: str = "development"
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
        "openai_api_key",
        "twilio_account_sid",
        "gmail_email",
        "telegram_bot_token"
    ]
    for req in required:
        if not getattr(settings, req):
            logger.warning(f"⚠️ Missing {req} - some features will be unavailable")