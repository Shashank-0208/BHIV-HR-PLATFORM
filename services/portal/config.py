"""
BHIV HR Platform - HR Portal Configuration
Version: 3.1.0 with Phase 3 Features
Updated: October 23, 2025
Status: Production Ready - Fixed Database Connection

Configuration for HR Portal Streamlit application:
- API Gateway connection settings (FIXED)
- HTTP client with connection pooling
- Timeout and retry configurations
- Production-ready defaults
"""

import httpx
import os
import logging

# Version Information
__version__ = "3.1.0"
__updated__ = "2025-10-23"
__status__ = "Production Ready - Database Fixed"

# Environment Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Service URLs - Required
GATEWAY_URL = os.getenv("GATEWAY_URL")
if not GATEWAY_URL:
    raise ValueError("GATEWAY_URL environment variable is required")

AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL")
if not AGENT_SERVICE_URL:
    raise ValueError("AGENT_SERVICE_URL environment variable is required")

# Authentication - Required
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
if not API_KEY_SECRET:
    raise ValueError("API_KEY_SECRET environment variable is required")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable is required")

CANDIDATE_JWT_SECRET = os.getenv("CANDIDATE_JWT_SECRET")
if not CANDIDATE_JWT_SECRET:
    raise ValueError("CANDIDATE_JWT_SECRET environment variable is required")

# API Configuration
API_BASE = GATEWAY_URL
API_KEY = API_KEY_SECRET

# HTTP Client Configuration with proper timeouts
timeout_config = httpx.Timeout(
    connect=15.0,  # Connection timeout
    read=60.0,     # Read timeout for long operations
    write=30.0,    # Write timeout
    pool=10.0      # Pool timeout
)

limits = httpx.Limits(
    max_keepalive_connections=10,
    max_connections=20,
    keepalive_expiry=30.0
)

headers = {"Authorization": f"Bearer {API_KEY}"}

# Global HTTP client with connection pooling
http_client = httpx.Client(
    timeout=timeout_config,
    limits=limits,
    headers=headers,
    follow_redirects=True
)

# Logging Configuration
def setup_logging():
    """Setup logging based on environment configuration"""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    
    if ENVIRONMENT == "production":
        logging.getLogger("streamlit").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)

# Portal Configuration
PORTAL_CONFIG = {
    "title": "BHIV HR Platform - Dashboard",
    "version": __version__,
    "api_endpoints": 55,
    "features": [
        "Candidate Management",
        "Job Posting", 
        "AI Matching",
        "Values Assessment",
        "Interview Scheduling",
        "Offer Management"
    ],
    "status": __status__,
    "updated": __updated__,
    "database_status": "Connected",
    "gateway_url": API_BASE
}
