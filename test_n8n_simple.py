#!/usr/bin/env python3
"""
N8N Integration Endpoints Testing Script - Simple Version
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
    print("BHIV HR Platform - N8N Integration Testing")
    print(f"Gateway URL: {GATEWAY_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    results = []
    
    # Test 1: Health Check
    results.append(test_endpoint(
        "GET", "/health", 
        description="Basic health check to verify service is running"
    ))
    
    # Test 2: Check if N8N routes are available
    results.append(test_endpoint(
        "GET", "/docs",
        description="Check FastAPI docs to see if N8N endpoints are listed"
    ))
    
    # Test 3: N8N Webhook - Candidate Applied
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
    
    # Test 4: N8N Status Check
    results.append(test_endpoint(
        "GET", "/n8n/status",
        description="Check N8N integration status and configuration"
    ))
    
    # Summary Report
    print(f"\n" + "="*80)
    print("TEST SUMMARY REPORT")
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
            print(f"  - {test['method']} {test['endpoint']}: {test.get('error', 'HTTP ' + str(test.get('status_code', 'Unknown')))}")
    
    if successful_tests:
        print(f"\nSUCCESSFUL TESTS:")
        for test in successful_tests:
            print(f"  - {test['method']} {test['endpoint']}: {test['status_code']} ({test['response_time']:.2f}s)")

if __name__ == "__main__":
    main()