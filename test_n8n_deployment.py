#!/usr/bin/env python3
"""
N8N Deployment Testing and Environment Variable Verification
Tests N8N integration deployment status and provides manual checking steps
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
    print(f"\n" + "="*60)
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
    print("BHIV HR Platform - N8N Deployment Testing")
    print(f"Gateway URL: {GATEWAY_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = []
    
    # Test 1: Basic Health Check
    results.append(test_endpoint(
        "GET", "/health", 
        description="Basic health check to verify Gateway service is running"
    ))
    
    # Test 2: Check API Documentation
    results.append(test_endpoint(
        "GET", "/docs",
        description="Check if N8N endpoints appear in FastAPI documentation"
    ))
    
    # Test 3: Test N8N Webhook - Candidate Applied (should work now)
    candidate_applied_data = {
        "candidate_id": 1,
        "job_id": 1,
        "candidate_name": "Test Candidate",
        "job_title": "Software Engineer",
        "email": "test@example.com",
        "phone": "+1234567890",
        "application_date": datetime.now().isoformat()
    }
    results.append(test_endpoint(
        "POST", "/webhooks/candidate-applied", 
        data=candidate_applied_data,
        description="N8N webhook for candidate application notifications"
    ))
    
    # Test 4: Test N8N Webhook - Candidate Shortlisted
    shortlisted_data = {
        "candidate_id": 1,
        "job_id": 1,
        "candidate_name": "Test Candidate",
        "job_title": "Software Engineer",
        "email": "test@example.com",
        "shortlisted_by": "HR Manager",
        "shortlisted_date": datetime.now().isoformat()
    }
    results.append(test_endpoint(
        "POST", "/webhooks/candidate-shortlisted",
        data=shortlisted_data,
        description="N8N webhook for candidate shortlisting notifications"
    ))
    
    # Test 5: Test N8N Webhook - Interview Scheduled
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "candidate_name": "Test Candidate",
        "job_title": "Software Engineer",
        "email": "test@example.com",
        "interview_date": "2024-12-01T10:00:00Z",
        "date": "2024-12-01",
        "time": "10:00 AM",
        "interviewer": "Tech Lead",
        "interview_type": "Technical"
    }
    results.append(test_endpoint(
        "POST", "/webhooks/interview-scheduled",
        data=interview_data,
        description="N8N webhook for interview scheduling notifications"
    ))
    
    # Test 6: Check if N8N routes are available (if included)
    results.append(test_endpoint(
        "GET", "/api/v1/notify/status",
        description="Check N8N notification service status (if routes included)"
    ))
    
    # Summary Report
    print(f"\n" + "="*80)
    print("N8N DEPLOYMENT TEST SUMMARY")
    print("="*80)
    
    successful_tests = [r for r in results if r.get('success', False)]
    failed_tests = [r for r in results if not r.get('success', False)]
    
    print(f"Total Tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Success Rate: {len(successful_tests)/len(results)*100:.1f}%")
    
    if failed_tests:
        print(f"\nFAILED TESTS:")
        for test in failed_tests:
            error_msg = test.get('error', f"HTTP {test.get('status_code', 'Unknown')}")
            print(f"  - {test['method']} {test['endpoint']}: {error_msg}")
    
    if successful_tests:
        print(f"\nSUCCESSFUL TESTS:")
        for test in successful_tests:
            print(f"  - {test['method']} {test['endpoint']}: {test['status_code']} ({test['response_time']:.2f}s)")
    
    # Manual Checking Guide
    print(f"\n" + "="*80)
    print("MANUAL CHECKING STEPS FOR N8N INTEGRATION")
    print("="*80)
    
    print("\n1. RENDER ENVIRONMENT VARIABLES:")
    print("   - Go to Render Dashboard > bhiv-hr-gateway service > Environment")
    print("   - Verify these environment variables are set:")
    print("     * N8N_GMAIL_WEBHOOK=https://bhivhrplatform.app.n8n.cloud/webhook/1a108336-bfad-489c-8c38-4f907045a2ed")
    print("     * N8N_WHATSAPP_WEBHOOK=https://bhivhrplatform.app.n8n.cloud/webhook/aafbb77b-2dce-41c1-8c34-33fef4cb8ead")
    print("     * N8N_TELEGRAM_WEBHOOK=https://bhivhrplatform.app.n8n.cloud/webhook/17543422-01c7-4f75-ad76-9504c5fc9499")
    
    print("\n2. RENDER DEPLOYMENT STATUS:")
    print("   - Check if Gateway service deployed successfully after adding N8N files")
    print("   - Look for any import errors in deployment logs")
    print("   - Verify notification_service.py and n8n_routes.py are included in deployment")
    
    print("\n3. N8N CLOUD WORKSPACE:")
    print("   - Login to https://bhivhrplatform.app.n8n.cloud")
    print("   - Check if all 3 workflows are active:")
    print("     * Gmail Notification Workflow")
    print("     * WhatsApp Notification Workflow") 
    print("     * Telegram Notification Workflow")
    print("   - Test each webhook URL manually")
    
    print("\n4. NOTIFICATION TESTING:")
    print("   - Gmail: Check if emails are being sent to test addresses")
    print("   - WhatsApp: Verify Twilio sandbox is configured and phone numbers are verified")
    print("   - Telegram: Confirm bot token is valid and chat IDs are correct")
    
    print("\n5. ENDPOINT VERIFICATION:")
    print("   - Visit https://bhiv-hr-gateway-ltg0.onrender.com/docs")
    print("   - Look for 'N8N Webhooks' section with 3 endpoints:")
    print("     * POST /webhooks/candidate-applied")
    print("     * POST /webhooks/candidate-shortlisted") 
    print("     * POST /webhooks/interview-scheduled")
    
    print("\n6. TROUBLESHOOTING STEPS:")
    print("   - If webhooks return 'No module named notification_service':")
    print("     * Redeploy Gateway service to include notification_service.py")
    print("     * Check file is in services/gateway/app/ directory")
    print("   - If N8N routes return 404:")
    print("     * Verify n8n_routes.py is included and imported in main.py")
    print("     * Check router is included with correct prefix")
    print("   - If notifications fail:")
    print("     * Verify N8N webhook URLs are accessible")
    print("     * Check N8N workspace execution limits")
    print("     * Validate environment variables in Render")
    
    print("\n7. NEXT STEPS:")
    print("   - Add N8N environment variables to Render")
    print("   - Redeploy Gateway service if needed")
    print("   - Test each notification channel individually")
    print("   - Monitor N8N execution logs for errors")
    print("   - Set up monitoring for notification delivery rates")

if __name__ == "__main__":
    main()