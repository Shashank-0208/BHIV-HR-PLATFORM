import requests
import json

def test_job_management_endpoints():
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    # Expected schemas based on Gateway code analysis
    endpoints = [
        {
            "name": "List Jobs",
            "method": "GET",
            "path": "/v1/jobs",
            "auth": True,
            "expected_schema": ["jobs", "count"]
        },
        {
            "name": "Create Job",
            "method": "POST", 
            "path": "/v1/jobs",
            "auth": True,
            "data": {
                "title": "Test Software Engineer",
                "department": "Engineering", 
                "location": "Remote",
                "experience_level": "Mid-level",
                "requirements": "Python, FastAPI, PostgreSQL",
                "description": "Test job posting for schema validation"
            },
            "expected_schema": ["message", "job_id", "created_at"]
        }
    ]
    
    print("Job Management Endpoints - Schema Validation & Testing")
    print("=" * 60)
    
    for endpoint in endpoints:
        print(f"\n{endpoint['name']} - {endpoint['method']} {endpoint['path']}")
        print("-" * 50)
        
        try:
            url = f"{base_url}{endpoint['path']}"
            req_headers = headers if endpoint.get("auth") else {}
            
            # Make request
            if endpoint["method"] == "GET":
                response = requests.get(url, headers=req_headers, timeout=15)
            elif endpoint["method"] == "POST":
                response = requests.post(url, json=endpoint.get("data", {}), headers=req_headers, timeout=15)
            
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
                    
                    # Validate specific data for each endpoint
                    if endpoint["path"] == "/v1/jobs" and endpoint["method"] == "GET":
                        jobs_count = len(data.get("jobs", []))
                        total_count = data.get("count", 0)
                        print(f"Jobs Retrieved: {jobs_count}")
                        print(f"Total Count: {total_count}")
                        if jobs_count > 0:
                            first_job = data["jobs"][0]
                            print(f"Sample Job: {first_job.get('title', 'N/A')} - {first_job.get('department', 'N/A')}")
                    
                    elif endpoint["path"] == "/v1/jobs" and endpoint["method"] == "POST":
                        print(f"Creation Status: {data.get('message', 'N/A')}")
                        print(f"New Job ID: {data.get('job_id', 'N/A')}")
                        print(f"Created At: {data.get('created_at', 'N/A')}")
                    
                except json.JSONDecodeError:
                    print("ERROR: Invalid JSON response")
                    print(f"Raw Response: {response.text[:100]}...")
                    
            else:
                print(f"FAILED - HTTP {response.status_code}")
                print(f"Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"ERROR - {str(e)}")
    
    print(f"\n{'='*60}")
    print("Job Management Endpoints validation complete!")

if __name__ == "__main__":
    test_job_management_endpoints()