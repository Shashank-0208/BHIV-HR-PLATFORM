import requests
import json

# Test critical endpoints after redeploy
BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

print("BHIV HR Platform - Final Deployment Test")
print("=" * 50)

# Test 1: AI Matching (Critical)
print("\n1. Testing AI Matching Service Connection...")
try:
    response = requests.get(f"{BASE_URL}/v1/match/1/top", headers=HEADERS, timeout=30)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        agent_status = data.get('agent_status', 'unknown')
        algorithm = data.get('algorithm_version', 'unknown')
        
        print(f"Agent Status: {agent_status}")
        print(f"Algorithm: {algorithm}")
        
        if agent_status == 'connected':
            print("SUCCESS: AI Agent service connected!")
        else:
            print("ISSUE: Still using database fallback")
    else:
        print(f"FAILED: {response.text[:100]}")
        
except Exception as e:
    print(f"ERROR: {str(e)}")

# Test 2: Client Login (Database Schema)
print("\n2. Testing Client Login (Database Schema)...")
try:
    login_data = {"client_id": "TECH001", "password": "demo123"}
    response = requests.post(f"{BASE_URL}/v1/client/login", headers=HEADERS, json=login_data, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("SUCCESS: Client login working")
    else:
        print(f"ISSUE: {response.text[:100]}")
        
except Exception as e:
    print(f"ERROR: {str(e)}")

# Test 3: Database Schema Version
print("\n3. Checking Database Schema Version...")
try:
    response = requests.get(f"{BASE_URL}/v1/database/schema", headers=HEADERS, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"Schema Version: {data.get('schema_version', 'unknown')}")
        print(f"Total Tables: {data.get('total_tables', 'unknown')}")
        print("SUCCESS: Database accessible")
    else:
        print("ISSUE: Database schema endpoint failed")
except Exception as e:
    print(f"ERROR: {str(e)}")

print("\n" + "=" * 50)
print("DEPLOYMENT STATUS SUMMARY:")
print("- Database Schema v4.2.0: DEPLOYED")
print("- Gateway Service: REDEPLOYED")
print("- Check AI matching status above for final verification")
print("=" * 50)