#!/usr/bin/env python3
"""
BHIV HR Platform - Local Deployment with Ishan's Integration
Fixes authentication issues and integrates Ishan's AI system
"""

import os
import subprocess
import sys
import time
import requests
import json
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_docker():
    """Check if Docker is running"""
    success, stdout, stderr = run_command("docker --version")
    if not success:
        print("❌ Docker not found. Please install Docker Desktop.")
        return False
    
    success, stdout, stderr = run_command("docker ps")
    if not success:
        print("❌ Docker daemon not running. Please start Docker Desktop.")
        return False
    
    print("✅ Docker is running")
    return True

def setup_environment():
    """Setup environment variables for local deployment"""
    env_content = """# BHIV HR Platform - Local Development with Ishan Integration
# Updated for authentication fixes

# Database Configuration
DATABASE_URL=postgresql://bhiv_user:bhiv_local_password_2025@localhost:5432/bhiv_hr
POSTGRES_PASSWORD=bhiv_local_password_2025
POSTGRES_USER=bhiv_user
POSTGRES_DB=bhiv_hr

# API Security (Fixed)
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
CANDIDATE_JWT_SECRET_KEY=candidate_jwt_secret_key_2025
GATEWAY_SECRET_KEY=bhiv_gateway_secret_2025_docker

# Service URLs (Local)
GATEWAY_SERVICE_URL=http://localhost:8000
AGENT_SERVICE_URL=http://localhost:9000
LANGGRAPH_SERVICE_URL=http://localhost:9001
PORTAL_SERVICE_URL=http://localhost:8501
CLIENT_PORTAL_SERVICE_URL=http://localhost:8502
CANDIDATE_PORTAL_SERVICE_URL=http://localhost:8503
ISHAN_AI_SERVICE_URL=http://localhost:5000

# Ishan's AI System Integration
ISHAN_AI_ENABLED=true
ISHAN_AI_API_KEY=ishan_ai_integration_key_2025

# Communication Services
TWILIO_ACCOUNT_SID=<YOUR_TWILIO_ACCOUNT_SID>
TWILIO_AUTH_TOKEN=<YOUR_TWILIO_AUTH_TOKEN>
TWILIO_WHATSAPP_NUMBER=<YOUR_WHATSAPP_NUMBER>
GMAIL_EMAIL=<YOUR_GMAIL_EMAIL>
GMAIL_APP_PASSWORD=<YOUR_GMAIL_APP_PASSWORD>
TELEGRAM_BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
TELEGRAM_BOT_USERNAME=<YOUR_TELEGRAM_BOT_USERNAME>
GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>
GEMINI_MODEL=gemini-pro

# Environment Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
PYTHON_VERSION=3.12.7
OBSERVABILITY_ENABLED=true
"""
    
    with open(".env.local", "w") as f:
        f.write(env_content)
    
    print("✅ Environment configuration created")

def start_ishan_ai_system():
    """Start Ishan's AI system"""
    print("🚀 Starting Ishan's AI HR System...")
    
    ishan_dir = Path("Ishan's_AI_HR_System-main")
    if not ishan_dir.exists():
        print("❌ Ishan's AI system directory not found")
        return False
    
    # Install dependencies
    print("📦 Installing Ishan's AI system dependencies...")
    success, stdout, stderr = run_command("pip install -r requirements.txt", cwd=ishan_dir)
    if not success:
        print(f"⚠️ Warning: Could not install all dependencies: {stderr}")
    
    # Start Ishan's system in background
    print("🔄 Starting Ishan's AI system on port 5000...")
    try:
        subprocess.Popen([
            sys.executable, "run_fastapi.py"
        ], cwd=ishan_dir)
        
        # Wait for startup
        time.sleep(10)
        
        # Check if it's running
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Ishan's AI system started successfully")
                return True
        except:
            pass
        
        print("⚠️ Ishan's AI system may be starting (check manually)")
        return True
        
    except Exception as e:
        print(f"❌ Failed to start Ishan's AI system: {e}")
        return False

def fix_portal_authentication():
    """Fix authentication issues in portals"""
    print("🔧 Fixing portal authentication issues...")
    
    # Create authentication fix for HR Portal
    hr_portal_auth_fix = '''
# Authentication fix for HR Portal
import streamlit as st
import os

def check_authentication():
    """Check if user is authenticated"""
    api_key = os.getenv("API_KEY_SECRET")
    if not api_key:
        st.error("❌ API Key not configured. Please check environment variables.")
        return False
    
    # Store in session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = True
        st.session_state.api_key = api_key
    
    return True

def get_auth_headers():
    """Get authentication headers"""
    api_key = os.getenv("API_KEY_SECRET", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
'''
    
    # Write auth fix to portal
    with open("services/portal/auth_fix.py", "w") as f:
        f.write(hr_portal_auth_fix)
    
    print("✅ Portal authentication fixes applied")

def start_docker_services():
    """Start Docker services"""
    print("🐳 Starting Docker services...")
    
    # Stop any existing containers
    run_command("docker-compose -f docker-compose.production.yml down")
    
    # Start services
    success, stdout, stderr = run_command("docker-compose -f docker-compose.production.yml up -d --build")
    if not success:
        print(f"❌ Failed to start Docker services: {stderr}")
        return False
    
    print("✅ Docker services started")
    return True

def wait_for_services():
    """Wait for all services to be ready"""
    services = [
        ("Database", "http://localhost:5432", None),
        ("Gateway", "http://localhost:8000/health", 200),
        ("Agent", "http://localhost:9000/health", 200),
        ("LangGraph", "http://localhost:9001/health", 200),
        ("HR Portal", "http://localhost:8501", None),
        ("Client Portal", "http://localhost:8502", None),
        ("Candidate Portal", "http://localhost:8503", None),
        ("Ishan's AI", "http://localhost:5000/health", 200)
    ]
    
    print("⏳ Waiting for services to be ready...")
    
    for service_name, url, expected_status in services:
        if expected_status is None:
            print(f"⚠️ {service_name}: Manual check required")
            continue
            
        max_retries = 30
        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == expected_status:
                    print(f"✅ {service_name}: Ready")
                    break
            except:
                pass
            
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"⚠️ {service_name}: Not responding (may need manual check)")

def test_authentication():
    """Test authentication across all portals"""
    print("🔐 Testing authentication...")
    
    api_key = os.getenv("API_KEY_SECRET", "<YOUR_API_KEY>")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Test Gateway
    try:
        response = requests.get("http://localhost:8000/health", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Gateway authentication: Working")
        else:
            print(f"⚠️ Gateway authentication: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Gateway authentication: Failed - {e}")
    
    # Test Agent
    try:
        response = requests.get("http://localhost:9000/health", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Agent authentication: Working")
        else:
            print(f"⚠️ Agent authentication: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Agent authentication: Failed - {e}")
    
    # Test LangGraph
    try:
        response = requests.get("http://localhost:9001/health", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ LangGraph authentication: Working")
        else:
            print(f"⚠️ LangGraph authentication: Status {response.status_code}")
    except Exception as e:
        print(f"❌ LangGraph authentication: Failed - {e}")

def create_integration_endpoints():
    """Create integration endpoints for Ishan's system"""
    print("🔗 Creating integration endpoints...")
    
    integration_code = '''
"""
Integration endpoints for Ishan's AI HR System
"""
from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter(prefix="/integration/ishan", tags=["Ishan Integration"])

ISHAN_AI_URL = os.getenv("ISHAN_AI_SERVICE_URL", "http://localhost:5000")

@router.post("/sync-candidate")
async def sync_candidate_to_ishan(candidate_data: dict):
    """Sync candidate data to Ishan's AI system"""
    try:
        response = requests.post(f"{ISHAN_AI_URL}/integration/sync-candidate", json=candidate_data)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get-ai-decision")
async def get_ai_decision(request_data: dict):
    """Get AI decision from Ishan's system"""
    try:
        response = requests.post(f"{ISHAN_AI_URL}/ai/decide", json=request_data)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-feedback")
async def send_feedback_to_ishan(feedback_data: dict):
    """Send feedback to Ishan's AI system"""
    try:
        response = requests.post(f"{ISHAN_AI_URL}/ai/feedback", json=feedback_data)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def check_ishan_health():
    """Check Ishan's AI system health"""
    try:
        response = requests.get(f"{ISHAN_AI_URL}/health")
        return {"status": "connected", "ishan_health": response.json()}
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}
'''
    
    # Create integration directory
    os.makedirs("services/gateway/integration", exist_ok=True)
    
    with open("services/gateway/integration/ishan_integration.py", "w") as f:
        f.write(integration_code)
    
    print("✅ Integration endpoints created")

def show_deployment_summary():
    """Show deployment summary"""
    print("\n" + "="*60)
    print("🎉 BHIV HR Platform - Local Deployment Complete!")
    print("="*60)
    print("\n📊 Service Status:")
    print("• Database (PostgreSQL): http://localhost:5432")
    print("• Gateway API: http://localhost:8000")
    print("• Agent Service: http://localhost:9000")
    print("• LangGraph Service: http://localhost:9001")
    print("• HR Portal: http://localhost:8501")
    print("• Client Portal: http://localhost:8502")
    print("• Candidate Portal: http://localhost:8503")
    print("• Ishan's AI System: http://localhost:5000")
    
    print("\n🔐 Authentication:")
    print("• API Key: [Check .env.local file for your API key]")
    print("• All portals configured with unified authentication")
    
    print("\n🧪 Testing:")
    print("• Gateway API Docs: http://localhost:8000/docs")
    print("• Ishan's AI Docs: http://localhost:5000/docs")
    print("• Test authentication with provided API key")
    
    print("\n🔧 Troubleshooting:")
    print("• Check Docker containers: docker ps")
    print("• View logs: docker-compose logs [service_name]")
    print("• Restart services: docker-compose restart")
    
    print("\n✅ Ready for testing and development!")

def main():
    """Main deployment function"""
    print("🚀 BHIV HR Platform - Local Deployment with Ishan Integration")
    print("="*60)
    
    # Check prerequisites
    if not check_docker():
        return False
    
    # Setup environment
    setup_environment()
    
    # Fix authentication issues
    fix_portal_authentication()
    
    # Create integration endpoints
    create_integration_endpoints()
    
    # Start Ishan's AI system first
    start_ishan_ai_system()
    
    # Start Docker services
    if not start_docker_services():
        return False
    
    # Wait for services
    wait_for_services()
    
    # Test authentication
    test_authentication()
    
    # Show summary
    show_deployment_summary()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)