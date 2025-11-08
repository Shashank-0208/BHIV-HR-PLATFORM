#!/usr/bin/env python3
"""
N8N Notification Service Testing Script
Tests the production notification service with real N8N webhooks
"""
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'services', 'gateway', 'app'))

from notification_service import NotificationService, notify_candidate_applied, notify_candidate_shortlisted, notify_interview_scheduled

async def test_notification_service():
    """Test the notification service with production N8N webhooks"""
    print("🧪 Testing N8N Notification Service...")
    print("=" * 50)
    
    service = NotificationService()
    
    # Test 1: Email notification
    print("\n📧 Testing Email Notification...")
    try:
        result = await service.send_email(
            email="test@example.com",
            candidate_name="Test Candidate",
            status="Application Received",
            message="Thank you for your application. We will review it shortly."
        )
        print(f"Email Result: {result}")
    except Exception as e:
        print(f"Email Error: {e}")
    
    # Test 2: WhatsApp notification (requires sandbox join)
    print("\n📱 Testing WhatsApp Notification...")
    try:
        result = await service.send_whatsapp(
            phone="+1234567890",  # Replace with your number after joining sandbox
            candidate_name="Test Candidate",
            status="Interview Scheduled",
            message="Your interview is scheduled for Monday at 10 AM."
        )
        print(f"WhatsApp Result: {result}")
    except Exception as e:
        print(f"WhatsApp Error: {e}")
    
    # Test 3: Telegram notification (requires chat ID)
    print("\n🤖 Testing Telegram Notification...")
    try:
        result = await service.send_telegram(
            chat_id="123456789",  # Replace with your Telegram chat ID
            candidate_name="Test Candidate",
            status="Offer Sent",
            message="Congratulations! We are pleased to offer you the position."
        )
        print(f"Telegram Result: {result}")
    except Exception as e:
        print(f"Telegram Error: {e}")
    
    # Test 4: All channels notification
    print("\n🚀 Testing All Channels Notification...")
    try:
        result = await service.send_all_channels(
            email="test@example.com",
            phone="+1234567890",  # Optional
            chat_id="123456789",  # Optional
            candidate_name="John Doe",
            status="Application Received",
            message="Thank you for applying. We will review your application shortly."
        )
        print(f"All Channels Result: {result}")
    except Exception as e:
        print(f"All Channels Error: {e}")

async def test_convenience_functions():
    """Test the convenience functions"""
    print("\n🎯 Testing Convenience Functions...")
    print("=" * 50)
    
    # Test candidate applied notification
    print("\n📝 Testing Candidate Applied...")
    try:
        result = await notify_candidate_applied(
            email="test@example.com",
            name="Jane Smith",
            job_title="Senior Developer",
            phone="+1234567890"
        )
        print(f"Applied Result: {result}")
    except Exception as e:
        print(f"Applied Error: {e}")
    
    # Test shortlisted notification
    print("\n🎯 Testing Candidate Shortlisted...")
    try:
        result = await notify_candidate_shortlisted(
            email="test@example.com",
            name="Jane Smith",
            job_title="Senior Developer"
        )
        print(f"Shortlisted Result: {result}")
    except Exception as e:
        print(f"Shortlisted Error: {e}")
    
    # Test interview scheduled notification
    print("\n📅 Testing Interview Scheduled...")
    try:
        result = await notify_interview_scheduled(
            email="test@example.com",
            name="Jane Smith",
            job_title="Senior Developer",
            date="2025-01-15",
            time="10:00 AM",
            interviewer="Sarah Johnson"
        )
        print(f"Interview Result: {result}")
    except Exception as e:
        print(f"Interview Error: {e}")

async def main():
    """Run all tests"""
    print("🔥 N8N Notification Service Testing Started")
    print(f"Timestamp: {asyncio.get_event_loop().time()}")
    
    await test_notification_service()
    await test_convenience_functions()
    
    print("\n" + "=" * 50)
    print("✅ N8N Notification Service Testing Complete!")
    print("\n📋 Setup Requirements:")
    print("1. WhatsApp: Send 'join locate-barn' to +14155238886")
    print("2. Telegram: Message @bhiv_hr_assistant_bot and get chat ID")
    print("3. Gmail: Should work automatically via N8N OAuth2")

if __name__ == "__main__":
    asyncio.run(main())