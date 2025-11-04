import requests
import json

def test_endpoint(method, path, data=None, expected_schema=None):
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print(f"Testing: {method} {path}")
    print("=" * 50)
    
    try:
        url = f"{base_url}{path}"
        
        # Make request
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=15)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=15)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=15)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                actual_schema = list(response_data.keys()) if isinstance(response_data, dict) else []
                
                print(f"Response Schema: {actual_schema}")
                
                # Schema validation
                if expected_schema:
                    schema_valid = all(key in actual_schema for key in expected_schema)
                    missing = [k for k in expected_schema if k not in actual_schema]
                    
                    print(f"Expected Schema: {expected_schema}")
                    print(f"Schema Valid: {'YES' if schema_valid else 'NO'}")
                    if missing:
                        print(f"Missing Keys: {missing}")
                
                # Show response data
                print(f"Response Data:")
                print(json.dumps(response_data, indent=2)[:500] + ("..." if len(str(response_data)) > 500 else ""))
                
                return {"status": "SUCCESS", "data": response_data, "schema": actual_schema}
                
            except json.JSONDecodeError:
                print("Response: Invalid JSON")
                print(f"Raw Response: {response.text[:200]}")
                return {"status": "INVALID_JSON", "raw": response.text}
        else:
            print(f"Error Response: {response.text}")
            return {"status": "ERROR", "code": response.status_code, "message": response.text}
            
    except Exception as e:
        print(f"Exception: {str(e)}")
        return {"status": "EXCEPTION", "error": str(e)}

# Ready for individual endpoint testing
if __name__ == "__main__":
    print("Gateway Endpoint Tester Ready!")
    print("Usage: test_endpoint('GET', '/v1/jobs', expected_schema=['jobs'])")