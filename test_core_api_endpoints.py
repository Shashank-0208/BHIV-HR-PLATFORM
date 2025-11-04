import requests
import json

def test_core_api_endpoints():
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    # Expected schemas based on Gateway code analysis
    endpoints = [
        {
            "name": "Read Root",
            "method": "GET",
            "path": "/",
            "auth": False,
            "expected_schema": ["message", "version", "status", "endpoints", "documentation", "monitoring", "live_demo"]
        },
        {
            "name": "Health Check", 
            "method": "GET",
            "path": "/health",
            "auth": False,
            "expected_schema": ["status", "service", "version", "timestamp"]
        },
        {
            "name": "Test Candidates DB",
            "method": "GET", 
            "path": "/test-candidates",
            "auth": True,
            "expected_schema": ["database_status", "total_candidates", "test_timestamp"]
        }
    ]
    
    print("Core API Endpoints - Schema Validation & Testing")
    print("=" * 60)
    
    for endpoint in endpoints:
        print(f"\n{endpoint['name']} - {endpoint['method']} {endpoint['path']}")
        print("-" * 50)
        
        try:
            url = f"{base_url}{endpoint['path']}"
            req_headers = headers if endpoint.get("auth") else {}
            
            response = requests.get(url, headers=req_headers, timeout=15)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {response.elapsed.total_seconds():.2f}s")
            print(f"Auth Required: {'YES' if endpoint.get('auth') else 'NO'}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    actual_schema = list(data.keys()) if isinstance(data, dict) else []
                    expected_schema = endpoint["expected_schema"]
                    
                    # Schema validation
                    schema_valid = all(key in actual_schema for key in expected_schema)
                    missing = [k for k in expected_schema if k not in actual_schema]
                    extra = [k for k in actual_schema if k not in expected_schema]
                    
                    print(f"Expected Schema: {expected_schema}")
                    print(f"Actual Schema: {actual_schema}")
                    print(f"Schema Valid: {'YES' if schema_valid else 'NO'}")
                    
                    if missing:
                        print(f"Missing Keys: {missing}")
                    if extra:
                        print(f"Extra Keys: {extra}")
                    
                    # Show sample response data
                    print("Sample Response:")
                    sample = json.dumps(data, indent=2)[:300]
                    print(f"{sample}{'...' if len(str(data)) > 300 else ''}")
                    
                    # Validate specific data types and values
                    if endpoint["path"] == "/":
                        print(f"Service Info: {data.get('message', 'N/A')}")
                        print(f"Version: {data.get('version', 'N/A')}")
                        print(f"Endpoints Count: {data.get('endpoints', 'N/A')}")
                    
                    elif endpoint["path"] == "/health":
                        print(f"Health Status: {data.get('status', 'N/A')}")
                        print(f"Service Name: {data.get('service', 'N/A')}")
                    
                    elif endpoint["path"] == "/test-candidates":
                        print(f"DB Status: {data.get('database_status', 'N/A')}")
                        print(f"Candidates Count: {data.get('total_candidates', 'N/A')}")
                    
                except json.JSONDecodeError:
                    print("ERROR: Invalid JSON response")
                    print(f"Raw Response: {response.text[:100]}...")
                    
            else:
                print(f"FAILED - HTTP {response.status_code}")
                print(f"Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"ERROR - {str(e)}")
    
    print(f"\n{'='*60}")
    print("Core API Endpoints validation complete!")

if __name__ == "__main__":
    test_core_api_endpoints()