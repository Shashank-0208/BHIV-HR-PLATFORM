import requests
import json

# Check clients table structure via API
def check_clients_table():
    url = "https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/schema"
    headers = {
        "Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("=== DATABASE SCHEMA INFO ===")
        print(f"Schema Version: {data.get('schema_version')}")
        print(f"Total Tables: {data.get('total_tables')}")
        print(f"Tables: {data.get('tables')}")
        print(f"Missing job_applications: {'job_applications' not in data.get('tables', [])}")
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

# Test specific table columns via direct query
def test_clients_columns():
    print("\n=== TESTING CLIENTS TABLE COLUMNS ===")
    
    # Test if missing columns exist by trying to use them
    url = "https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login"
    headers = {"Content-Type": "application/json"}
    data = {"client_id": "TECH001", "password": "demo123"}
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    if "failed_login_attempts" in str(result.get("error", "")):
        print("MISSING: failed_login_attempts column")
        return False
    elif result.get("success"):
        print("FIXED: Client login working")
        return True
    else:
        print(f"OTHER ERROR: {result.get('error', 'Unknown')}")
        return False

# Test AI matching connection
def test_ai_matching():
    print("\n=== TESTING AI MATCHING CONNECTION ===")
    
    url = "https://bhiv-hr-gateway-ltg0.onrender.com/v1/match/1/top"
    headers = {
        "Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        agent_status = data.get("agent_status")
        algorithm = data.get("algorithm_version")
        
        print(f"Agent Status: {agent_status}")
        print(f"Algorithm: {algorithm}")
        
        if agent_status == "connected":
            print("FIXED: AI Agent connected")
            return True
        else:
            print("NOT FIXED: Still using fallback")
            return False
    else:
        print(f"Error: {response.status_code}")
        return False

if __name__ == "__main__":
    print("CHECKING LIVE DATABASE DEPLOYMENT STATUS\n")
    
    # Check database schema
    schema_info = check_clients_table()
    
    # Test clients table columns
    clients_fixed = test_clients_columns()
    
    # Test AI matching
    ai_fixed = test_ai_matching()
    
    print("\n=== DEPLOYMENT STATUS SUMMARY ===")
    print(f"Database Schema: {'UPDATED' if schema_info and schema_info.get('schema_version') == '4.2.0' else 'NOT UPDATED'}")
    print(f"Client Login: {'FIXED' if clients_fixed else 'BROKEN'}")
    print(f"AI Matching: {'FIXED' if ai_fixed else 'USING FALLBACK'}")
    
    if not clients_fixed or not ai_fixed:
        print("\nMANUAL DEPLOYMENT STILL REQUIRED")
        if not clients_fixed:
            print("- Execute database schema update in Render PostgreSQL console")
        if not ai_fixed:
            print("- Redeploy Gateway service on Render dashboard")
    else:
        print("\nALL ISSUES RESOLVED!")