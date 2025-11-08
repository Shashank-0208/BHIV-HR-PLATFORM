#!/usr/bin/env python3
"""
N8N Integration Testing Script
Tests all 3 N8N workflows with production URLs
"""
import httpx
import asyncio
import json
from datetime import datetime

# Production N8N Webhook URLs
N8N_GMAIL_WEBHOOK = "https://bhivhrplatform.app.n8n.cloud/webhook/1a108336-bfad-489c-8c38-4f907045a2ed"
N8N_WHATSAPP_WEBHOOK = "https://bhivhrplatform.app.n8n.cloud/webhook/aafbb77b-2dce-41c1-8c34-33fef4cb8ead"
N8N_TELEGRAM_WEBHOOK = "https://bhivhrplatform.app.n8n.cloud/webhook/17543422-01c7-4f75-ad76-9504c5fc9499"

# Gateway webhook endpoints
GATEWAY_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"

async def test_n8n_direct():
    """Test N8N workflows directly"""
    print("🧪 Testing N8N Workflows Directly...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test Gmail workflow
        print("\n📧 Testing Gmail Workflow...")
        try:
            response = await client.post(N8N_GMAIL_WEBHOOK, json={
                "email": "test@example.com",
                "candidateName": "Test Candidate",
                "status": "Application Received",
                "message": "Thank you for your application. We will review it shortly."
            })
            print(f"Gmail Response: {response.status_code}")
        except Exception as e:
            print(f"Gmail Error: {e}")
        
        # Test WhatsApp workflow
        print("\n📱 Testing WhatsApp Workflow...")
        try:
            response = await client.post(N8N_WHATSAPP_WEBHOOK, json={
                "phone": "+1234567890",
                "candidateName": "Test Candidate",
                "status": "Interview Scheduled",
                "message": "Your interview is on Monday at 10 AM."
            })
            print(f"WhatsApp Response: {response.status_code}")
        except Exception as e:
            print(f"WhatsApp Error: {e}")
        
        # Test Telegram workflow
        print("\n🤖 Testing Telegram Workflow...")
        try:
            response = await client.post(N8N_TELEGRAM_WEBHOOK, json={
                "chatId": "123456789",
                "candidateName": "Test Candidate",
                "status": "Offer Sent",
                "message": "Congratulations on your offer!"
            })
            print(f"Telegram Response: {response.status_code}")
        except Exception as e:
            print(f"Telegram Error: {e}")

async def test_gateway_integration():
    """Test Gateway N8N integration endpoints"""
    print("\n🚀 Testing Gateway Integration...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test candidate applied webhook
        print("\n📝 Testing Candidate Applied Webhook...")
        try:
            response = await client.post(f"{GATEWAY_URL}/webhooks/candidate-applied", json={
                "email": "test@example.com",
                "name": "John Doe",
                "phone": "+1234567890",
                "job_title": "Senior Developer"
            })
            print(f"Applied Response: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Applied Error: {e}")
        
        # Test candidate shortlisted webhook
        print("\n🎯 Testing Candidate Shortlisted Webhook...")
        try:
            response = await client.post(f"{GATEWAY_URL}/webhooks/candidate-shortlisted", json={
                "email": "test@example.com",
                "name": "John Doe",
                "job_title": "Senior Developer"
            })
            print(f"Shortlisted Response: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Shortlisted Error: {e}")
        
        # Test interview scheduled webhook
        print("\n📅 Testing Interview Scheduled Webhook...")
        try:
            response = await client.post(f"{GATEWAY_URL}/webhooks/interview-scheduled", json={
                "email": "test@example.com",
                "name": "John Doe",
                "job_title": "Senior Developer",
                "date": "2025-01-10",
                "time": "10:00 AM",
                "interviewer": "Sarah Johnson"
            })
            print(f"Interview Response: {response.status_code} - {response.json()}")
        except Exception as e:
            print(f"Interview Error: {e}")

async def main():
    """Run all tests"""
    print("🔥 N8N Integration Testing Started")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 50)
    
    await test_n8n_direct()
    await test_gateway_integration()
    
    print("\n" + "=" * 50)
    print("✅ N8N Integration Testing Complete!")

if __name__ == "__main__":
    asyncio.run(main())