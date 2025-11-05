import os
from typing import Optional

class Config:
    """Configuration for Candidate Portal"""
    
    def __init__(self):
        # Gateway API Configuration
        self.GATEWAY_URL = os.getenv(
            "GATEWAY_URL", 
            "https://bhiv-hr-gateway-ltg0.onrender.com"
        )
        
        # API Authentication
        self.API_KEY = os.getenv(
            "API_KEY", 
            "<YOUR_API_KEY>"
        )
        
        # JWT Configuration for candidate authentication
        self.JWT_SECRET = os.getenv(
            "JWT_SECRET", 
            "<YOUR_CANDIDATE_JWT_SECRET>"
        )
        
        # Database Configuration (if needed for direct access)
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://bhiv_user:8oaleQyxSfBJp7uqt0UJoAXnOhPj63nG@dpg-d40c0kf5r7bs73abt080-a.oregon-postgres.render.com/bhiv_hr_jcuu_w5fl"
        )
        
        # Portal Configuration
        self.PORTAL_PORT = int(os.getenv("CANDIDATE_PORTAL_PORT", "8503"))
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        
        # File Upload Configuration
        self.MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]
        
        # Session Configuration
        self.SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
        
    def get_headers(self, token: Optional[str] = None) -> dict:
        """Get API headers with authentication"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token or self.API_KEY}"
        }
        return headers
