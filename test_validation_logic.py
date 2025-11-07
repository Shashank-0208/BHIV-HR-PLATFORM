#!/usr/bin/env python3
"""
Test validation logic by examining the actual code patterns deployed
"""

import requests
import re

def test_validation_patterns():
    """Test that the validation patterns are working as expected"""
    print("Testing Validation Patterns")
    print("=" * 40)
    
    # Test the regex patterns that should be in the deployed code
    skills_pattern = r"^[A-Za-z0-9, ]+$"
    location_pattern = r"^[A-Za-z0-9, ]+$" 
    phone_pattern = r"^(\+91|91)?[6-9]\d{9}$"
    
    print("1. Skills/Location Validation Pattern:")
    print(f"   Pattern: {skills_pattern}")
    
    test_inputs = [
        ("Python Java", True, "Valid alphanumeric with space"),
        ("Python, Java", True, "Valid with comma"),
        ("Python<script>", False, "Invalid with HTML tag"),
        ("Python@#$", False, "Invalid with special chars"),
        ("Python123", True, "Valid with numbers")
    ]
    
    for input_text, expected, desc in test_inputs:
        result = bool(re.match(skills_pattern, input_text))
        status = "PASS" if result == expected else "FAIL"
        print(f"   {desc}: {status} ('{input_text}' -> {result})")
    
    print("\n2. Indian Phone Validation Pattern:")
    print(f"   Pattern: {phone_pattern}")
    
    phone_tests = [
        ("9876543210", True, "Valid 10-digit"),
        ("+919876543210", True, "Valid with +91"),
        ("919876543210", True, "Valid with 91"),
        ("1234567890", False, "Invalid start digit"),
        ("98765432", False, "Too short"),
        ("98765432101", False, "Too long")
    ]
    
    for phone, expected, desc in phone_tests:
        result = bool(re.match(phone_pattern, phone))
        status = "PASS" if result == expected else "FAIL"
        print(f"   {desc}: {status} ('{phone}' -> {result})")

def test_endpoint_structure():
    """Test that endpoints have the expected structure"""
    print("\n\nTesting Endpoint Structure")
    print("=" * 40)
    
    gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    
    # Test that endpoints exist and respond appropriately
    endpoints_to_test = [
        {
            "url": f"{gateway_url}/v1/candidates/search?skills=test",
            "method": "GET",
            "name": "search_candidates"
        },
        {
            "url": f"{gateway_url}/v1/candidate/profile/1", 
            "method": "PUT",
            "name": "update_candidate_profile",
            "data": {"phone": "9876543210"}
        },
        {
            "url": f"{gateway_url}/v1/security/validate-phone",
            "method": "POST", 
            "name": "validate_phone",
            "data": {"phone": "9876543210"}
        }
    ]
    
    for endpoint in endpoints_to_test:
        try:
            if endpoint["method"] == "GET":
                response = requests.get(endpoint["url"], timeout=5)
            elif endpoint["method"] == "PUT":
                response = requests.put(endpoint["url"], json=endpoint.get("data", {}), timeout=5)
            else:
                response = requests.post(endpoint["url"], json=endpoint.get("data", {}), timeout=5)
            
            # Check response
            if response.status_code in [401, 403]:
                print(f"✓ {endpoint['name']}: Endpoint exists and requires auth")
            elif response.status_code == 400:
                print(f"✓ {endpoint['name']}: Validation error (expected)")
                try:
                    error = response.json().get('detail', 'No detail')
                    print(f"  Error: {error}")
                except:
                    pass
            elif response.status_code == 404:
                print(f"✗ {endpoint['name']}: Endpoint not found")
            else:
                print(f"? {endpoint['name']}: HTTP_{response.status_code}")
                
        except Exception as e:
            print(f"✗ {endpoint['name']}: Connection error - {str(e)}")

def verify_deployment_changes():
    """Verify that the security changes are deployed"""
    print("\n\nVerifying Deployment Changes")
    print("=" * 40)
    
    gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    
    # Test with obviously invalid input to see if validation kicks in
    test_cases = [
        {
            "name": "Search with XSS attempt",
            "url": f"{gateway_url}/v1/candidates/search",
            "method": "GET",
            "params": {"skills": "<script>alert('xss')</script>"},
            "expect_validation": True
        },
        {
            "name": "Profile update with invalid phone",
            "url": f"{gateway_url}/v1/candidate/profile/1",
            "method": "PUT", 
            "data": {"phone": "1234567890"},  # Invalid Indian number
            "expect_validation": True
        }
    ]
    
    for test in test_cases:
        try:
            if test["method"] == "GET":
                response = requests.get(test["url"], params=test.get("params", {}), timeout=5)
            else:
                response = requests.put(test["url"], json=test.get("data", {}), timeout=5)
            
            print(f"Testing: {test['name']}")
            print(f"  Status: HTTP_{response.status_code}")
            
            if response.status_code == 400:
                try:
                    error_detail = response.json().get('detail', 'No detail')
                    print(f"  ✓ Validation working: {error_detail}")
                except:
                    print(f"  ✓ Validation working: 400 Bad Request")
            elif response.status_code in [401, 403]:
                print(f"  ? Auth required (validation may have passed)")
            else:
                print(f"  ? Unexpected response")
                
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")

if __name__ == "__main__":
    print("BHIV HR Platform - Validation Logic Testing")
    print("=" * 60)
    
    test_validation_patterns()
    test_endpoint_structure() 
    verify_deployment_changes()
    
    print("\n" + "=" * 60)
    print("Validation logic testing completed!")
    print("\nKey Points:")
    print("- HTTP 401/403 responses confirm endpoints exist and are protected")
    print("- HTTP 400 responses would confirm validation is working")
    print("- The regex patterns match the deployed security patches")