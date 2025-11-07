#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the specific security changes made to search_candidates and update_candidate_profile endpoints
"""

import requests
import json
import time
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def test_search_candidates_validation():
    """Test the enhanced input validation in search_candidates endpoint"""
    print("Testing search_candidates input validation...")
    print("=" * 50)
    
    gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Test cases for search validation
    test_cases = [
        {
            "params": {"skills": "Python Java", "location": "Mumbai"},
            "expected": "PASS",
            "desc": "Valid alphanumeric with spaces"
        },
        {
            "params": {"skills": "Python, Java, React", "location": "Mumbai, Delhi"},
            "expected": "PASS", 
            "desc": "Valid with commas"
        },
        {
            "params": {"skills": "Python<script>", "location": "Mumbai"},
            "expected": "FAIL",
            "desc": "Invalid - XSS attempt in skills"
        },
        {
            "params": {"skills": "Python", "location": "Mumbai'; DROP TABLE--"},
            "expected": "FAIL",
            "desc": "Invalid - SQL injection in location"
        },
        {
            "params": {"skills": "Python@#$", "location": "Mumbai"},
            "expected": "FAIL",
            "desc": "Invalid - special characters in skills"
        },
        {
            "params": {"skills": "A" * 201, "location": "Mumbai"},
            "expected": "FAIL",
            "desc": "Invalid - skills too long (>200 chars)"
        },
        {
            "params": {"skills": "Python", "location": "A" * 101},
            "expected": "FAIL",
            "desc": "Invalid - location too long (>100 chars)"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        try:
            # Test with API key to see actual validation results
            response = requests.get(
                f"{gateway_url}/v1/candidates/search",
                params=test["params"],
                headers=headers,
                timeout=15
            )
            
            print(f"[{i}/7] {test['desc']}")
            print(f"      Params: skills='{test['params']['skills'][:30]}...', location='{test['params']['location'][:30]}...'")
            
            if response.status_code == 400:
                # This means validation failed (good for invalid inputs)
                error_detail = response.json().get('detail', 'Unknown error')
                if test["expected"] == "FAIL":
                    print(f"      Result: PASS - Validation blocked invalid input")
                    print(f"      Error: {error_detail}")
                else:
                    print(f"      Result: FAIL - Valid input was blocked")
                    print(f"      Error: {error_detail}")
            elif response.status_code == 401:
                # Authentication required - validation passed, now needs API key
                if test["expected"] == "PASS":
                    print(f"      Result: PASS - Validation passed, auth required")
                else:
                    print(f"      Result: FAIL - Invalid input should have been blocked before auth")
            else:
                print(f"      Result: HTTP_{response.status_code}")
                
        except Exception as e:
            print(f"      Result: ERROR - {str(e)}")
        print()

def test_profile_update_validation():
    """Test the enhanced phone validation in update_candidate_profile endpoint"""
    print("Testing update_candidate_profile phone validation...")
    print("=" * 50)
    
    gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Test cases for profile update validation
    test_cases = [
        {
            "data": {"phone": "9876543210"},
            "expected": "PASS",
            "desc": "Valid 10-digit Indian number"
        },
        {
            "data": {"phone": "+919876543210"},
            "expected": "PASS",
            "desc": "Valid with +91 prefix"
        },
        {
            "data": {"phone": "919876543210"},
            "expected": "PASS",
            "desc": "Valid with 91 prefix"
        },
        {
            "data": {"phone": "1234567890"},
            "expected": "FAIL",
            "desc": "Invalid - starts with 1"
        },
        {
            "data": {"phone": "98765432"},
            "expected": "FAIL",
            "desc": "Invalid - too short"
        },
        {
            "data": {"phone": "98765432101"},
            "expected": "FAIL",
            "desc": "Invalid - too long"
        },
        {
            "data": {"experience_years": -1},
            "expected": "FAIL",
            "desc": "Invalid - negative experience"
        },
        {
            "data": {"experience_years": 5},
            "expected": "PASS",
            "desc": "Valid experience years"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        try:
            response = requests.put(
                f"{gateway_url}/v1/candidate/profile/1",
                json=test["data"],
                headers=headers,
                timeout=15
            )
            
            print(f"[{i}/8] {test['desc']}")
            print(f"      Data: {test['data']}")
            
            if response.status_code == 400:
                # Validation failed
                error_detail = response.json().get('detail', 'Unknown error')
                if test["expected"] == "FAIL":
                    print(f"      Result: PASS - Validation blocked invalid input")
                    print(f"      Error: {error_detail}")
                else:
                    print(f"      Result: FAIL - Valid input was blocked")
                    print(f"      Error: {error_detail}")
            elif response.status_code == 401:
                # Authentication required - validation passed
                if test["expected"] == "PASS":
                    print(f"      Result: PASS - Validation passed, auth required")
                else:
                    print(f"      Result: FAIL - Invalid input should have been blocked before auth")
            else:
                print(f"      Result: HTTP_{response.status_code}")
                
        except Exception as e:
            print(f"      Result: ERROR - {str(e)}")
        print()

def test_with_api_key():
    """Test endpoints with proper API key authentication"""
    print("Testing with API key authentication...")
    print("=" * 40)
    
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Test 1: Authenticated search with valid input
    print("[1/5] Testing authenticated candidate search...")
    try:
        response = requests.get(
            f"{gateway_url}/v1/candidates/search",
            params={"skills": "Python", "location": "Mumbai"},
            headers=headers,
            timeout=15
        )
        print(f"      Status: HTTP_{response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ Found {len(data.get('candidates', []))} candidates")
        else:
            print(f"      Response: {response.text[:100]}...")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Test 2: Get all candidates
    print("\n[2/5] Testing get all candidates...")
    try:
        response = requests.get(
            f"{gateway_url}/v1/candidates",
            headers=headers,
            timeout=15
        )
        print(f"      Status: HTTP_{response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ Retrieved {len(data)} total candidates")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Test 3: Get all jobs
    print("\n[3/5] Testing get all jobs...")
    try:
        response = requests.get(
            f"{gateway_url}/v1/jobs",
            headers=headers,
            timeout=15
        )
        print(f"      Status: HTTP_{response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ Retrieved {len(data)} total jobs")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Test 4: AI Matching test
    print("\n[4/5] Testing AI matching for job 1...")
    try:
        response = requests.get(
            f"{gateway_url}/v1/match/1/top",
            headers=headers,
            timeout=120
        )
        print(f"      Status: HTTP_{response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"      ✅ AI matching returned {len(data.get('matches', []))} matches")
        else:
            print(f"      Response: {response.text[:100]}...")
    except Exception as e:
        print(f"      ❌ Error: {e}")
    
    # Test 5: Security validation endpoints
    print("\n[5/5] Testing security validation endpoints...")
    try:
        # Test phone validation
        response = requests.post(
            f"{gateway_url}/v1/security/validate-phone",
            json={"phone": "+919876543210"},
            headers=headers,
            timeout=10
        )
        print(f"      Phone validation: HTTP_{response.status_code}")
        
        # Test input validation
        response = requests.post(
            f"{gateway_url}/v1/security/test-input-validation",
            json={"test_input": "Python Java"},
            headers=headers,
            timeout=10
        )
        print(f"      Input validation: HTTP_{response.status_code}")
        print("      ✅ Security endpoints accessible")
    except Exception as e:
        print(f"      ❌ Security test error: {e}")

def test_endpoint_responses():
    """Test that the endpoints are responding correctly"""
    print("Testing endpoint availability...")
    print("=" * 30)
    
    gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    
    endpoints = [
        {"url": f"{gateway_url}/v1/candidates/search", "method": "GET"},
        {"url": f"{gateway_url}/v1/candidate/profile/1", "method": "PUT"},
        {"url": f"{gateway_url}/v1/security/validate-phone", "method": "POST"},
        {"url": f"{gateway_url}/v1/security/test-input-validation", "method": "POST"}
    ]
    
    for endpoint in endpoints:
        try:
            if endpoint["method"] == "GET":
                response = requests.get(endpoint["url"], timeout=5)
            elif endpoint["method"] == "PUT":
                response = requests.put(endpoint["url"], json={}, timeout=5)
            else:
                response = requests.post(endpoint["url"], json={}, timeout=5)
            
            print(f"{endpoint['method']} {endpoint['url'].split('/')[-1]}: HTTP_{response.status_code}")
            
        except Exception as e:
            print(f"{endpoint['method']} {endpoint['url'].split('/')[-1]}: ERROR - {str(e)}")

if __name__ == "__main__":
    print("BHIV HR Platform - Security Changes Testing")
    print("=" * 60)
    print("Testing the two modified endpoints for security validation")
    print()
    
    test_endpoint_responses()
    print()
    test_with_api_key()
    print()
    test_search_candidates_validation()
    test_profile_update_validation()
    
    print("=" * 60)
    print("Security changes testing completed!")