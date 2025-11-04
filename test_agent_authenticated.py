import requests
import json

def test_agent_with_auth():
    base_url = "https://bhiv-hr-agent-nhgg.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    endpoints = [
        {"method": "GET", "path": "/", "name": "Root", "auth": False},
        {"method": "GET", "path": "/health", "name": "Health Check", "auth": False},
        {"method": "GET", "path": "/test-db", "name": "Database Test", "auth": True},
        {"method": "POST", "path": "/match", "name": "Single Match", "auth": True, "data": {"job_id": 1, "candidate_id": 7}},
        {"method": "POST", "path": "/batch-match", "name": "Batch Match", "auth": True, "data": {"job_id": 1}},
        {"method": "GET", "path": "/analyze/7", "name": "Analyze Candidate", "auth": True}
    ]
    
    print("BHIV AI Agent Service - Authenticated Testing")
    print("=" * 55)
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint['path']}"
            req_headers = headers if endpoint.get("auth", False) else {}
            
            if endpoint["method"] == "GET":
                response = requests.get(url, headers=req_headers, timeout=15)
            else:
                response = requests.post(url, json=endpoint.get("data", {}), headers=req_headers, timeout=15)
            
            status = "OK" if response.status_code == 200 else f"FAIL ({response.status_code})"
            time = f"{response.elapsed.total_seconds():.2f}s"
            auth_status = "AUTH" if endpoint.get("auth", False) else "PUBLIC"
            
            print(f"{endpoint['name']:17} | {status:10} | {time:6} | {auth_status:6} | {endpoint['method']} {endpoint['path']}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "matches" in data:
                        print(f"                     Matches found: {len(data['matches'])}")
                    elif "match_score" in data:
                        print(f"                     Match score: {data['match_score']}")
                    elif "status" in data:
                        print(f"                     Status: {data['status']}")
                    elif "message" in data:
                        print(f"                     Message: {data['message']}")
                except:
                    content = response.text[:60].replace('\n', ' ')
                    print(f"                     Response: {content}...")
            else:
                error = response.text[:60].replace('\n', ' ')
                print(f"                     Error: {error}...")
                
        except Exception as e:
            print(f"{endpoint['name']:17} | ERROR    | ERROR | ERROR  | {endpoint['method']} {endpoint['path']}")
            print(f"                     Exception: {str(e)[:50]}...")

if __name__ == "__main__":
    test_agent_with_auth()