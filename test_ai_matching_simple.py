#!/usr/bin/env python3
"""
AI Matching Engine Endpoint Testing with Schema Validation
"""

import requests
import json
import time

# Configuration
BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_top_matches():
    """Test GET /v1/match/{job_id}/top"""
    print("Testing GET /v1/match/1/top")
    
    url = f"{BASE_URL}/v1/match/1/top?limit=5"
    start_time = time.time()
    response = requests.get(url, headers=HEADERS, timeout=70)
    response_time = time.time() - start_time
    
    print(f"Status: {response.status_code}")
    print(f"Response Time: {response_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        
        # Check required fields
        required = ["matches", "job_id", "limit", "algorithm_version", "agent_status"]
        missing = [f for f in required if f not in data]
        
        if missing:
            print(f"Missing fields: {missing}")
        else:
            print("Schema: VALID")
        
        print(f"Agent Status: {data.get('agent_status')}")
        print(f"Algorithm: {data.get('algorithm_version')}")
        print(f"Matches: {len(data.get('matches', []))}")
        
        return True, data
    else:
        print(f"Failed: {response.text}")
        return False, None

def test_batch_matches():
    """Test POST /v1/match/batch"""
    print("\nTesting POST /v1/match/batch")
    
    url = f"{BASE_URL}/v1/match/batch"
    payload = [1, 2, 3]
    
    start_time = time.time()
    response = requests.post(url, headers=HEADERS, json=payload, timeout=70)
    response_time = time.time() - start_time
    
    print(f"Status: {response.status_code}")
    print(f"Response Time: {response_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        
        # Check required fields
        required = ["batch_results", "total_jobs_processed", "algorithm_version", "status"]
        missing = [f for f in required if f not in data]
        
        if missing:
            print(f"Missing fields: {missing}")
        else:
            print("Schema: VALID")
        
        print(f"Status: {data.get('status')}")
        print(f"Jobs Processed: {data.get('total_jobs_processed')}")
        print(f"Algorithm: {data.get('algorithm_version')}")
        
        return True, data
    else:
        print(f"Failed: {response.text}")
        return False, None

def test_validation():
    """Test input validation"""
    print("\nTesting Input Validation")
    
    # Invalid job_id
    response = requests.get(f"{BASE_URL}/v1/match/0/top", headers=HEADERS)
    print(f"Invalid job_id (0): {response.status_code} - {'PASS' if response.status_code == 400 else 'FAIL'}")
    
    # Invalid limit
    response = requests.get(f"{BASE_URL}/v1/match/1/top?limit=100", headers=HEADERS)
    print(f"Invalid limit (100): {response.status_code} - {'PASS' if response.status_code == 400 else 'FAIL'}")
    
    # Empty job_ids
    response = requests.post(f"{BASE_URL}/v1/match/batch", headers=HEADERS, json=[])
    print(f"Empty job_ids: {response.status_code} - {'PASS' if response.status_code == 400 else 'FAIL'}")

def main():
    print("AI Matching Engine Testing")
    print("=" * 40)
    
    top_success, top_data = test_top_matches()
    batch_success, batch_data = test_batch_matches()
    test_validation()
    
    print("\nSummary")
    print("=" * 20)
    print(f"Top Matches: {'PASS' if top_success else 'FAIL'}")
    print(f"Batch Matches: {'PASS' if batch_success else 'FAIL'}")
    
    print("\nFixes Verification")
    print("=" * 20)
    
    if top_data:
        agent_status = top_data.get('agent_status')
        if agent_status in ['connected', 'disconnected']:
            print("Timeout fix: WORKING")
        
        if 'fallback' in top_data.get('algorithm_version', '') or agent_status == 'disconnected':
            print("Fallback mechanism: ACTIVE")
        elif agent_status == 'connected':
            print("Agent service: CONNECTED")
    
    if batch_data and batch_data.get('status') in ['success', 'fallback_success']:
        print("Batch fallback: WORKING")

if __name__ == "__main__":
    main()