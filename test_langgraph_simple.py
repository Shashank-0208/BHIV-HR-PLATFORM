#!/usr/bin/env python3
"""
Simple LangGraph Service Test
"""

import requests
import os

API_KEY = "bhiv-hr-2024-secure-api-key-v2"
LANGGRAPH_URL = "https://bhiv-hr-langgraph.onrender.com"

def test_endpoint(url, headers=None):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.status_code, response.text[:100]
    except Exception as e:
        return None, str(e)

def main():
    print("Simple LangGraph Test")
    print("=" * 25)
    
    # Test without auth
    print("Testing without auth:")
    status, response = test_endpoint(f"{LANGGRAPH_URL}/health")
    print(f"  /health: {status} - {response}")
    
    # Test with auth
    print("\nTesting with auth:")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    status, response = test_endpoint(f"{LANGGRAPH_URL}/health", headers)
    print(f"  /health: {status} - {response}")
    
    # Test root
    status, response = test_endpoint(f"{LANGGRAPH_URL}/", headers)
    print(f"  /: {status} - {response}")
    
    # Test local dependencies
    print("\nTesting local dependencies:")
    try:
        import sys
        sys.path.append("services/langgraph")
        from dependencies import validate_api_key
        result = validate_api_key(API_KEY)
        print(f"  API key validation: {result}")
    except Exception as e:
        print(f"  Import error: {e}")

if __name__ == "__main__":
    main()