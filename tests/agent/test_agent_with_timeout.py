import requests
import json

def test_agent_with_proper_timeout():
    base_url = "https://bhiv-hr-agent-nhgg.onrender.com"
    headers = {"Authorization": "Bearer <YOUR_API_KEY>"}
    
    endpoints = [
        {"method": "GET", "path": "/", "name": "Root", "timeout": 10},
        {"method": "GET", "path": "/health", "name": "Health Check", "timeout": 10},
        {"method": "GET", "path": "/test-db", "name": "Database Test", "timeout": 15, "auth": True},
        {"method": "POST", "path": "/match", "name": "Single Match", "timeout": 60, "auth": True, "data": {"job_id": 1, "candidate_ids": [7]}},
        {"method": "POST", "path": "/batch-match", "name": "Batch Match", "timeout": 30, "auth": True, "data": {"job_ids": [1]}},
        {"method": "GET", "path": "/analyze/7", "name": "Analyze Candidate", "timeout": 20, "auth": True}
    ]
    
    print("BHIV AI Agent Service - Complete Test (60s timeout for match)")
    print("=" * 65)
    
    for endpoint in endpoints:
        print(f"\nTesting {endpoint['name']}...")
        try:
            url = f"{base_url}{endpoint['path']}"
            req_headers = headers if endpoint.get("auth", False) else {}
            timeout = endpoint.get("timeout", 15)
            
            if endpoint["method"] == "GET":
                response = requests.get(url, headers=req_headers, timeout=timeout)
            else:
                response = requests.post(url, json=endpoint.get("data", {}), headers=req_headers, timeout=timeout)
            
            status = "OK" if response.status_code == 200 else f"FAIL ({response.status_code})"
            time = f"{response.elapsed.total_seconds():.1f}s"
            
            print(f"{endpoint['name']:17} | {status:10} | {time:8} | {endpoint['method']} {endpoint['path']}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "matches" in data:
                        print(f"                     Result: {len(data['matches'])} matches found")
                    elif "match_score" in data:
                        print(f"                     Result: Match score {data['match_score']}")
                    elif "status" in data:
                        print(f"                     Result: {data['status']}")
                    elif "message" in data:
                        print(f"                     Result: {data['message']}")
                except:
                    print(f"                     Result: {response.text[:50]}...")
            else:
                print(f"                     Error: {response.text[:50]}...")
                
        except requests.exceptions.Timeout:
            print(f"{endpoint['name']:17} | TIMEOUT  | >{timeout}s    | {endpoint['method']} {endpoint['path']}")
        except Exception as e:
            print(f"{endpoint['name']:17} | ERROR    | ERROR    | {endpoint['method']} {endpoint['path']}")
            print(f"                     Exception: {str(e)[:50]}...")

if __name__ == "__main__":
    test_agent_with_proper_timeout()
