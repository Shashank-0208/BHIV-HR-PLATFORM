#!/usr/bin/env python3
"""
BHIV HR Platform - Credential Validation Script
Tests all communication services before full deployment
"""

import os
import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_twilio():
    """Test Twilio WhatsApp service"""
    try:
        from twilio.rest import Client
        
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if not account_sid or not auth_token:
            return {"status": "❌", "service": "Twilio", "error": "Missing credentials"}
        
        client = Client(account_sid, auth_token)
        
        # Test account info (doesn't send messages)
        account = client.api.accounts(account_sid).fetch()
        
        return {
            "status": "✅", 
            "service": "Twilio WhatsApp", 
            "account": account_sid,
            "account_status": account.status
        }
    except Exception as e:
        return {"status": "❌", "service": "Twilio", "error": str(e)}

async def test_gmail():
    """Test Gmail SMTP connection"""
    try:
        import smtplib
        
        email = os.getenv('GMAIL_EMAIL')
        password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not email or not password:
            return {"status": "❌", "service": "Gmail", "error": "Missing credentials"}
        
        # Test SMTP connection (doesn't send emails)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email, password)
        
        return {
            "status": "✅", 
            "service": "Gmail SMTP", 
            "email": email,
            "connection": "Success"
        }
    except Exception as e:
        return {"status": "❌", "service": "Gmail", "error": str(e)}

async def test_telegram():
    """Test Telegram Bot"""
    try:
        from telegram import Bot
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not token:
            return {"status": "❌", "service": "Telegram", "error": "Missing token"}
        
        bot = Bot(token=token)
        
        # Test bot info (doesn't send messages)
        bot_info = await bot.get_me()
        
        return {
            "status": "✅", 
            "service": "Telegram Bot", 
            "username": f"@{bot_info.username}",
            "bot_id": bot_info.id
        }
    except Exception as e:
        return {"status": "❌", "service": "Telegram", "error": str(e)}

async def test_gemini():
    """Test Gemini AI"""
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            return {"status": "❌", "service": "Gemini", "error": "Missing API key"}
        
        genai.configure(api_key=api_key)
        
        # Test with simple prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, respond with 'OK' if you're working")
        
        return {
            "status": "✅", 
            "service": "Gemini AI", 
            "model": "gemini-pro",
            "response": response.text[:50]
        }
    except Exception as e:
        return {"status": "❌", "service": "Gemini", "error": str(e)}

async def main():
    """Run all credential tests"""
    print("BHIV HR Platform - Credential Validation")
    print("=" * 50)
    
    tests = [
        ("Twilio WhatsApp", test_twilio()),
        ("Gmail SMTP", test_gmail()),
        ("Telegram Bot", test_telegram()),
        ("Gemini AI", test_gemini())
    ]
    
    results = []
    for name, test_coro in tests:
        print(f"\nTesting {name}...")
        result = await test_coro
        results.append(result)
        
        if result["status"] == "✅":
            print(f"   [OK] {result['service']}: SUCCESS")
            for key, value in result.items():
                if key not in ["status", "service"]:
                    print(f"      {key}: {value}")
        else:
            print(f"   [FAIL] {result['service']}: FAILED")
            print(f"      Error: {result['error']}")
    
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY:")
    
    success_count = sum(1 for r in results if r["status"] == "✅")
    total_count = len(results)
    
    for result in results:
        status_text = '[OK]' if result['status'] == '✅' else '[FAIL]'
        print(f"   {status_text} {result['service']}")
    
    print(f"\nResult: {success_count}/{total_count} services validated")
    
    if success_count == total_count:
        print("[SUCCESS] ALL SERVICES READY - Proceed to Step 3 (Docker Startup)")
    else:
        print("[WARNING] Some services need attention before proceeding")
    
    return success_count == total_count

if __name__ == "__main__":
    asyncio.run(main())