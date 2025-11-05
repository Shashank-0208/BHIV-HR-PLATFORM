import os
import logging
from typing import Optional

class Config:
    """Configuration for Candidate Portal"""
    
    def __init__(self):
        # Environment Configuration
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # Gateway API Configuration - Required
        self.GATEWAY_URL = os.getenv("GATEWAY_URL")
        if not self.GATEWAY_URL:
            raise ValueError("GATEWAY_URL environment variable is required")
        
        # API Authentication - Required
        self.API_KEY = os.getenv("API_KEY")
        if not self.API_KEY:
            raise ValueError("API_KEY environment variable is required")
        
        # JWT Configuration for candidate authentication - Required
        self.JWT_SECRET = os.getenv("JWT_SECRET")
        if not self.JWT_SECRET:
            raise ValueError("JWT_SECRET environment variable is required")
            
        self.CANDIDATE_JWT_SECRET = os.getenv("CANDIDATE_JWT_SECRET")
        if not self.CANDIDATE_JWT_SECRET:
            raise ValueError("CANDIDATE_JWT_SECRET environment variable is required")
        
        # Database Configuration - Required
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")
        
        # Portal Configuration
        self.PORTAL_PORT = int(os.getenv("CANDIDATE_PORTAL_PORT", "8503"))
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        
        # File Upload Configuration
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]
        
        # Session Configuration
        self.SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
        
        # Setup logging
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging based on environment configuration"""
        log_level = getattr(logging, self.LOG_LEVEL.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        
        if self.ENVIRONMENT == "production":
            logging.getLogger("streamlit").setLevel(logging.WARNING)
            logging.getLogger("requests").setLevel(logging.WARNING)
        
    def get_headers(self, token: Optional[str] = None) -> dict:
        """Get API headers with authentication"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token or self.API_KEY}"
        }
        return headers
