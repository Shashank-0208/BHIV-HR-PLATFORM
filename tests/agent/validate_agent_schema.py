import requests
import json

def validate_agent_schema():
    base_url = "https://bhiv-hr-agent-nhgg.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("AI Agent Service - Schema Validation")
    print("=" * 50)
    
    # 1. Get OpenAPI docs
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        print(f"OpenAPI Docs      | {'OK' if response.status_code == 200 else 'FAIL'}")
    except:
        print("OpenAPI Docs      | ERROR")
    
    # 2. Get JSON schema
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=10)
        if response.status_code == 200:
            schema = response.json()
            print(f"Schema JSON       | OK")
            print(f"Endpoints found   | {len(schema.get('paths', {}))}")
            
            # Validate each endpoint
            paths = schema.get('paths', {})
            for path, methods in paths.items():
                print(f"\n{path}:")
                for method, details in methods.items():
                    print(f"  {method.upper():6} | {details.get('summary', 'No summary')}")
                    
                    # Check request body
                    if 'requestBody' in details:
                        req_schema = details['requestBody']['content']['application/json']['schema']
                        if 'properties' in req_schema:
                            print(f"         Request: {list(req_schema['properties'].keys())}")
                    
                    # Check responses
                    responses = details.get('responses', {})
                    for code, resp in responses.items():
                        if code == '200' and 'content' in resp:
                            resp_schema = resp['content']['application/json']['schema']
                            if 'properties' in resp_schema:
                                print(f"         Response: {list(resp_schema['properties'].keys())}")
        else:
            print(f"Schema JSON       | FAIL ({response.status_code})")
    except Exception as e:
        print(f"Schema JSON       | ERROR: {str(e)[:40]}...")
    
    # 3. Test actual responses
    print(f"\n{'='*50}")
    print("Response Schema Validation:")
    
    test_cases = [
        {"method": "GET", "path": "/", "name": "Root"},
        {"method": "GET", "path": "/health", "name": "Health"},
        {"method": "GET", "path": "/test-db", "name": "DB Test", "auth": True},
        {"method": "POST", "path": "/match", "name": "Match", "auth": True, "data": {"job_id": 1, "candidate_ids": [7]}, "timeout": 60},
        {"method": "POST", "path": "/batch-match", "name": "Batch", "auth": True, "data": {"job_ids": [1]}},
        {"method": "GET", "path": "/analyze/7", "name": "Analyze", "auth": True}
    ]
    
    for test in test_cases:
        try:
            url = f"{base_url}{test['path']}"
            req_headers = headers if test.get("auth") else {}
            timeout = test.get("timeout", 15)
            
            if test["method"] == "GET":
                response = requests.get(url, headers=req_headers, timeout=timeout)
            else:
                response = requests.post(url, json=test.get("data", {}), headers=req_headers, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                keys = list(data.keys()) if isinstance(data, dict) else ["non-dict response"]
                print(f"{test['name']:8} | Schema: {keys}")
            else:
                print(f"{test['name']:8} | Error: {response.status_code}")
                
        except Exception as e:
            print(f"{test['name']:8} | Exception: {str(e)[:30]}...")

if __name__ == "__main__":
    validate_agent_schema()