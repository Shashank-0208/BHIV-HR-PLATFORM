#!/usr/bin/env python3
"""
N8N Integration Endpoints Testing Script
Tests all N8N webhook and notification endpoints on production Gateway service
"""

import requests
import json
import time
from datetime import datetime

# Production Gateway URL
GATEWAY_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "your-api-key-here"  # Replace with actual API key

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint(method, endpoint, data=None, description=""):
    """Test a single endpoint and return results"""
    url = f"{GATEWAY_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"Testing: {method} {endpoint}")
    print(f"Description: {description}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        
        try:
            response_json = response.json()
            print(f"Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response Text: {response.text[:500]}")
        
        return {
            "endpoint": endpoint,
            "method": method,
            "status_code": response.status_code,
            "response_time": response.elapsed.total_seconds(),
            "success": 200 <= response.status_code < 300
        }
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            "endpoint": endpoint,
            "method": method,
            "error": str(e),
            "success": False
        }

def main():
    print("🚀 BHIV HR Platform - N8N Integration Testing")
    print(f"Gateway URL: {GATEWAY_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = []
    
    # Test 1: Health Check
    results.append(test_endpoint(
        "GET", "/health", 
        description="Basic health check to verify service is running"
    ))
    
    # Test 2: N8N Webhook - Candidate Applied
    candidate_applied_data = {
        "candidate_id": 1,
        "job_id": 1,
        "candidate_name": "Test Candidate",
        "job_title": "Software Engineer",
        "application_date": datetime.now().isoformat()
    }
    results.append(test_endpoint(
        "POST", "/webhooks/candidate-applied", 
        data=candidate_applied_data,
        description="N8N webhook for candidate application notifications"
    ))
    
    # Test 3: N8N Webhook - Candidate Shortlisted
    shortlisted_data = {
        "candidate_id": 1,
        "job_id": 1,
        "candidate_name": "Test Candidate",
        "job_title": "Software Engineer",
        "shortlisted_by": "HR Manager",
        "shortlisted_date": datetime.now().isoformat()
    }
    results.append(test_endpoint(
        "POST", "/webhooks/candidate-shortlisted",
        data=shortlisted_data,
        description="N8N webhook for candidate shortlisting notifications"
    ))
    
    # Test 4: N8N Webhook - Interview Scheduled
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "candidate_name": "Test Candidate",
        "job_title": "Software Engineer",
        "interview_date": "2024-12-01T10:00:00Z",
        "interviewer": "Tech Lead",
        "interview_type": "Technical"
    }
    results.append(test_endpoint(
        "POST", "/webhooks/interview-scheduled",
        data=interview_data,
        description="N8N webhook for interview scheduling notifications"
    ))
    
    # Test 5: Manual N8N Notification - Gmail
    gmail_data = {
        "type": "gmail",
        "subject": "Test Email from BHIV HR Platform",
        "message": "This is a test email sent via N8N automation system.",
        "recipient": "test@example.com"
    }
    results.append(test_endpoint(
        "POST", "/n8n/send-notification",
        data=gmail_data,
        description="Manual Gmail notification via N8N"
    ))
    
    # Test 6: Manual N8N Notification - WhatsApp
    whatsapp_data = {
        "type": "whatsapp",
        "message": "Test WhatsApp message from BHIV HR Platform via N8N automation.",
        "phone": "+1234567890"
    }
    results.append(test_endpoint(
        "POST", "/n8n/send-notification",
        data=whatsapp_data,
        description="Manual WhatsApp notification via N8N"
    ))
    
    # Test 7: Manual N8N Notification - Telegram
    telegram_data = {
        "type": "telegram",
        "message": "Test Telegram message from BHIV HR Platform via N8N automation.",
        "chat_id": "123456789"
    }
    results.append(test_endpoint(
        "POST", "/n8n/send-notification",
        data=telegram_data,
        description="Manual Telegram notification via N8N"
    ))
    
    # Test 8: N8N Status Check
    results.append(test_endpoint(
        "GET", "/n8n/status",
        description="Check N8N integration status and configuration"
    ))
    
    # Test 9: N8N Workflows List
    results.append(test_endpoint(
        "GET", "/n8n/workflows",
        description="List all available N8N workflows"
    ))
    
    # Summary Report
    print(f"\n{'='*80}")
    print("📊 TEST SUMMARY REPORT")
    print(f"{'='*80}")
    
    successful_tests = [r for r in results if r.get('success', False)]
    failed_tests = [r for r in results if not r.get('success', False)]
    
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Success Rate: {len(successful_tests)/len(results)*100:.1f}%")
    
    if failed_tests:
        print(f"\n❌ FAILED TESTS:")
        for test in failed_tests:
            print(f"  - {test['method']} {test['endpoint']}: {test.get('error', 'HTTP ' + str(test.get('status_code', 'Unknown')))}")
    
    if successful_tests:
        print(f"\n✅ SUCCESSFUL TESTS:")
        for test in successful_tests:
            print(f"  - {test['method']} {test['endpoint']}: {test['status_code']} ({test['response_time']:.2f}s)")
    
    print(f"\n🔍 NEXT STEPS FOR MANUAL VERIFICATION:")
    print("1. Check N8N Cloud dashboard for workflow executions")
    print("2. Verify notifications received in Gmail, WhatsApp, Telegram")
    print("3. Check Gateway service logs for N8N webhook calls")
    print("4. Test with real candidate data in production")
    print("5. Monitor notification delivery rates and response times")

if __name__ == "__main__":
    main()