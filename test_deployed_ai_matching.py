import requests
import json

def test_deployed_ai_matching_endpoints():
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    # Expected schemas based on deployed Gateway code
    endpoints = [
        {
            "name": "Get Top Matches",
            "method": "GET",
            "path": "/v1/match/1/top",
            "auth": True,
            "timeout": 60,
            "expected_schema": ["matches", "top_candidates", "job_id", "limit", "total_candidates", "algorithm_version", "processing_time", "ai_analysis", "agent_status"]
        },
        {
            "name": "Batch Match Jobs",
            "method": "POST",
            "path": "/v1/match/batch",
            "auth": True,
            "timeout": 90,
            "data": [1, 2],
            "expected_schema": ["batch_results", "total_jobs_processed", "total_candidates_analyzed", "algorithm_version", "status"]
        }
    ]
    
    print("AI Matching Engine Endpoints - Post-Deployment Testing")
    print("=" * 65)
    
    for endpoint in endpoints:
        print(f"\n{endpoint['name']} - {endpoint['method']} {endpoint['path']}")
        print("-" * 55)
        
        try:
            url = f"{base_url}{endpoint['path']}"
            req_headers = headers if endpoint.get("auth") else {}
            timeout = endpoint.get("timeout", 15)
            
            print(f"Timeout: {timeout}s")
            
            # Make request
            if endpoint["method"] == "GET":
                response = requests.get(url, headers=req_headers, timeout=timeout)
            elif endpoint["method"] == "POST":
                response = requests.post(url, json=endpoint.get("data", {}), headers=req_headers, timeout=timeout)
            
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
                    
                    if schema_valid:
                        print("SUCCESS: Schema matches perfectly!")
                    
                    # Show sample response data
                    print("Sample Response:")
                    sample = json.dumps(data, indent=2)[:400]
                    print(f"{sample}{'...' if len(str(data)) > 400 else ''}")
                    
                    # Validate specific AI matching data
                    if endpoint["path"].startswith("/v1/match/") and endpoint["method"] == "GET":
                        matches = data.get("matches", [])
                        total_candidates = data.get("total_candidates", 0)
                        algorithm_version = data.get("algorithm_version", "N/A")
                        agent_status = data.get("agent_status", "N/A")
                        
                        print(f"Matches Found: {len(matches)}")
                        print(f"Total Candidates: {total_candidates}")
                        print(f"Algorithm Version: {algorithm_version}")
                        print(f"Agent Status: {agent_status}")
                        print(f"Schema Fix Applied: {'YES' if 'total_candidates' in actual_schema else 'NO'}")
                        
                        if matches and len(matches) > 0:
                            first_match = matches[0]
                            print(f"Top Match: {first_match.get('name', 'N/A')} (Score: {first_match.get('score', 'N/A')})")
                    
                    elif endpoint["method"] == "POST" and "batch" in endpoint["path"]:
                        batch_results = data.get("batch_results", [])
                        total_jobs = data.get("total_jobs_processed", 0)
                        total_candidates = data.get("total_candidates_analyzed", 0)
                        status = data.get("status", "N/A")
                        
                        print(f"Batch Results: {len(batch_results)} jobs")
                        print(f"Total Jobs Processed: {total_jobs}")
                        print(f"Total Candidates Analyzed: {total_candidates}")
                        print(f"Batch Status: {status}")
                    
                except json.JSONDecodeError:
                    print("ERROR: Invalid JSON response")
                    print(f"Raw Response: {response.text[:100]}...")
                    
            else:
                print(f"FAILED - HTTP {response.status_code}")
                print(f"Error: {response.text[:100]}...")
                
        except requests.exceptions.Timeout:
            print(f"TIMEOUT - Request exceeded {timeout}s")
        except Exception as e:
            print(f"ERROR - {str(e)}")
    
    print(f"\n{'='*65}")
    print("Post-Deployment AI Matching Engine validation complete!")

if __name__ == "__main__":
    test_deployed_ai_matching_endpoints()