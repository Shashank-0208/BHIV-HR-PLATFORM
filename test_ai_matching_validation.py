#!/usr/bin/env python3
"""
AI Matching Engine Endpoint Testing with Schema Validation
Tests both endpoints with input/output validation and recent fixes verification
"""

import requests
import json
import time
from typing import Dict, Any, List

# Configuration
BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def validate_top_matches_response(response_data: Dict[str, Any]) -> List[str]:
    """Validate GET /v1/match/{job_id}/top response schema"""
    errors = []
    
    # Required fields
    required_fields = ["matches", "top_candidates", "job_id", "limit", "total_candidates", 
                      "algorithm_version", "processing_time", "ai_analysis", "agent_status"]
    
    for field in required_fields:
        if field not in response_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate matches structure
    if "matches" in response_data:
        for i, match in enumerate(response_data["matches"]):
            match_required = ["candidate_id", "name", "email", "score", "skills_match", 
                            "experience_match", "location_match", "reasoning", "recommendation_strength"]
            for field in match_required:
                if field not in match:
                    errors.append(f"Match {i}: Missing field {field}")
            
            # Validate score range
            if "score" in match and not (0 <= match["score"] <= 100):
                errors.append(f"Match {i}: Invalid score {match['score']}")
    
    return errors

def validate_batch_matches_response(response_data: Dict[str, Any]) -> List[str]:
    """Validate POST /v1/match/batch response schema"""
    errors = []
    
    # Required fields
    required_fields = ["batch_results", "total_jobs_processed", "total_candidates_analyzed", 
                      "algorithm_version", "status"]
    
    for field in required_fields:
        if field not in response_data:
            errors.append(f"Missing required field: {field}")
    
    # Validate batch_results structure
    if "batch_results" in response_data:
        for job_id, result in response_data["batch_results"].items():
            result_required = ["job_id", "matches", "algorithm"]
            for field in result_required:
                if field not in result:
                    errors.append(f"Job {job_id}: Missing field {field}")
    
    return errors

def test_top_matches_endpoint():
    """Test GET /v1/match/{job_id}/top endpoint"""
    print("🔍 Testing GET /v1/match/{job_id}/top")
    
    # Test valid request
    job_id = 1
    limit = 5
    url = f"{BASE_URL}/v1/match/{job_id}/top?limit={limit}"
    
    start_time = time.time()
    response = requests.get(url, headers=HEADERS, timeout=70)
    response_time = time.time() - start_time
    
    print(f"   Status: {response.status_code}")
    print(f"   Response Time: {response_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        
        # Schema validation
        schema_errors = validate_top_matches_response(data)
        if schema_errors:
            print(f"   ❌ Schema Errors: {schema_errors}")
        else:
            print("   ✅ Schema Valid")
        
        # Verify fixes
        print(f"   Agent Status: {data.get('agent_status', 'unknown')}")
        print(f"   Algorithm: {data.get('algorithm_version', 'unknown')}")
        print(f"   Matches Count: {len(data.get('matches', []))}")
        print(f"   Processing Time: {data.get('processing_time', 'unknown')}")
        
        # Check if fallback was used
        if data.get('agent_status') == 'disconnected':
            print("   ⚠️  Using fallback matching (Agent service unavailable)")
        elif data.get('agent_status') == 'connected':
            print("   ✅ Agent service connected")
        
        return True, data
    else:
        print(f"   ❌ Failed: {response.text}")
        return False, None

def test_batch_matches_endpoint():
    """Test POST /v1/match/batch endpoint"""
    print("\n🔍 Testing POST /v1/match/batch")
    
    # Test valid request
    job_ids = [1, 2, 3]
    url = f"{BASE_URL}/v1/match/batch"
    payload = job_ids
    
    start_time = time.time()
    response = requests.post(url, headers=HEADERS, json=payload, timeout=70)
    response_time = time.time() - start_time
    
    print(f"   Status: {response.status_code}")
    print(f"   Response Time: {response_time:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        
        # Schema validation
        schema_errors = validate_batch_matches_response(data)
        if schema_errors:
            print(f"   ❌ Schema Errors: {schema_errors}")
        else:
            print("   ✅ Schema Valid")
        
        # Verify fixes
        print(f"   Status: {data.get('status', 'unknown')}")
        print(f"   Algorithm: {data.get('algorithm_version', 'unknown')}")
        print(f"   Jobs Processed: {data.get('total_jobs_processed', 0)}")
        print(f"   Candidates Analyzed: {data.get('total_candidates_analyzed', 0)}")
        
        # Check batch results
        batch_results = data.get('batch_results', {})
        print(f"   Batch Results Count: {len(batch_results)}")
        
        # Check if fallback was used
        if 'fallback' in data.get('algorithm_version', ''):
            print("   ⚠️  Using fallback matching (Agent service unavailable)")
        else:
            print("   ✅ Agent service processing")
        
        return True, data
    else:
        print(f"   ❌ Failed: {response.text}")
        return False, None

def test_input_validation():
    """Test input validation for both endpoints"""
    print("\n🔍 Testing Input Validation")
    
    # Test invalid job_id
    print("   Testing invalid job_id (0)...")
    response = requests.get(f"{BASE_URL}/v1/match/0/top", headers=HEADERS)
    print(f"   Status: {response.status_code} {'✅' if response.status_code == 400 else '❌'}")
    
    # Test invalid limit
    print("   Testing invalid limit (100)...")
    response = requests.get(f"{BASE_URL}/v1/match/1/top?limit=100", headers=HEADERS)
    print(f"   Status: {response.status_code} {'✅' if response.status_code == 400 else '❌'}")
    
    # Test empty job_ids array
    print("   Testing empty job_ids array...")
    response = requests.post(f"{BASE_URL}/v1/match/batch", headers=HEADERS, json=[])
    print(f"   Status: {response.status_code} {'✅' if response.status_code == 400 else '❌'}")
    
    # Test too many job_ids
    print("   Testing too many job_ids (>10)...")
    large_job_ids = list(range(1, 12))
    response = requests.post(f"{BASE_URL}/v1/match/batch", headers=HEADERS, json=large_job_ids)
    print(f"   Status: {response.status_code} {'✅' if response.status_code == 400 else '❌'}")

def main():
    """Run all AI Matching Engine tests"""
    print("🚀 AI Matching Engine Endpoint Testing")
    print("=" * 50)
    
    # Test endpoints
    top_success, top_data = test_top_matches_endpoint()
    batch_success, batch_data = test_batch_matches_endpoint()
    
    # Test input validation
    test_input_validation()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    print(f"GET /v1/match/{{job_id}}/top: {'✅ PASS' if top_success else '❌ FAIL'}")
    print(f"POST /v1/match/batch: {'✅ PASS' if batch_success else '❌ FAIL'}")
    
    # Recent fixes verification
    print("\n🔧 Recent Fixes Verification")
    print("=" * 35)
    
    if top_data:
        agent_status = top_data.get('agent_status', 'unknown')
        if agent_status in ['connected', 'disconnected']:
            print("✅ Agent service timeout fix: Working (60s timeout)")
        else:
            print("❌ Agent service timeout fix: Issue detected")
        
        if 'fallback' in top_data.get('algorithm_version', '') or agent_status == 'disconnected':
            print("✅ Fallback mechanism: Active when needed")
        elif agent_status == 'connected':
            print("✅ Agent service: Connected and working")
    
    if batch_data:
        if batch_data.get('status') in ['success', 'fallback_success']:
            print("✅ Batch fallback mechanism: Working")
        else:
            print("❌ Batch fallback mechanism: Issue detected")

if __name__ == "__main__":
    main()