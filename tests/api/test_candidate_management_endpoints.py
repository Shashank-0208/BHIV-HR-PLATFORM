import requests
import json

def test_candidate_management_endpoints():
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer <YOUR_API_KEY>"}
    
    # Expected schemas based on Gateway code analysis
    endpoints = [
        {
            "name": "Get All Candidates",
            "method": "GET",
            "path": "/v1/candidates",
            "auth": True,
            "expected_schema": ["candidates", "total", "limit", "offset", "count"]
        },
        {
            "name": "Search Candidates",
            "method": "GET",
            "path": "/v1/candidates/search?skills=Python&location=Remote&experience_min=2",
            "auth": True,
            "expected_schema": ["candidates", "filters", "count"]
        },
        {
            "name": "Get Candidates By Job",
            "method": "GET",
            "path": "/v1/candidates/job/1",
            "auth": True,
            "expected_schema": ["candidates", "job_id", "count"]
        },
        {
            "name": "Get Candidate By ID",
            "method": "GET",
            "path": "/v1/candidates/7",
            "auth": True,
            "expected_schema": ["candidate"]
        },
        {
            "name": "Bulk Upload Candidates",
            "method": "POST",
            "path": "/v1/candidates/bulk",
            "auth": True,
            "data": {
                "candidates": [
                    {
                        "name": "Test Candidate Schema",
                        "email": "test.schema@example.com",
                        "phone": "+1-555-0123",
                        "location": "New York",
                        "experience_years": 3,
                        "technical_skills": "Python, JavaScript, SQL",
                        "seniority_level": "Mid-level",
                        "education_level": "Bachelor's"
                    }
                ]
            },
            "expected_schema": ["message", "candidates_received", "candidates_inserted", "errors", "total_errors", "status"]
        }
    ]
    
    print("Candidate Management Endpoints - Schema Validation & Testing")
    print("=" * 65)
    
    for endpoint in endpoints:
        print(f"\n{endpoint['name']} - {endpoint['method']} {endpoint['path']}")
        print("-" * 55)
        
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
                    if "candidates" in endpoint["path"] and endpoint["method"] == "GET":
                        if "search" in endpoint["path"]:
                            candidates_count = len(data.get("candidates", []))
                            filters = data.get("filters", {})
                            print(f"Search Results: {candidates_count} candidates")
                            print(f"Applied Filters: {filters}")
                        elif "/job/" in endpoint["path"]:
                            candidates_count = len(data.get("candidates", []))
                            job_id = data.get("job_id", "N/A")
                            print(f"Candidates for Job {job_id}: {candidates_count}")
                        elif endpoint["path"] == "/v1/candidates":
                            candidates_count = len(data.get("candidates", []))
                            total = data.get("total", 0)
                            print(f"Candidates Retrieved: {candidates_count}")
                            print(f"Total in DB: {total}")
                        elif "/candidates/" in endpoint["path"] and endpoint["path"].split("/")[-1].isdigit():
                            candidate = data.get("candidate", {})
                            print(f"Candidate Name: {candidate.get('name', 'N/A')}")
                            print(f"Candidate Email: {candidate.get('email', 'N/A')}")
                    
                    elif endpoint["method"] == "POST" and "bulk" in endpoint["path"]:
                        print(f"Upload Status: {data.get('message', 'N/A')}")
                        print(f"Received: {data.get('candidates_received', 0)}")
                        print(f"Inserted: {data.get('candidates_inserted', 0)}")
                        print(f"Errors: {data.get('total_errors', 0)}")
                    
                except json.JSONDecodeError:
                    print("ERROR: Invalid JSON response")
                    print(f"Raw Response: {response.text[:100]}...")
                    
            else:
                print(f"FAILED - HTTP {response.status_code}")
                print(f"Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"ERROR - {str(e)}")
    
    print(f"\n{'='*65}")
    print("Candidate Management Endpoints validation complete!")

if __name__ == "__main__":
    test_candidate_management_endpoints()
