import requests
import json

def complete_validation():
    base_url = "https://bhiv-hr-agent-nhgg.onrender.com"
    headers = {"Authorization": "Bearer <YOUR_API_KEY>"}
    
    print("AI Agent Service - Complete Validation")
    print("=" * 50)
    
    # Test all endpoints with proper data and timeouts
    tests = [
        {"name": "Root", "method": "GET", "path": "/", "timeout": 10},
        {"name": "Health", "method": "GET", "path": "/health", "timeout": 10},
        {"name": "DB Test", "method": "GET", "path": "/test-db", "timeout": 15, "auth": True},
        {"name": "Match", "method": "POST", "path": "/match", "timeout": 60, "auth": True, "data": {"job_id": 1, "candidate_ids": [7]}},
        {"name": "Batch", "method": "POST", "path": "/batch-match", "timeout": 30, "auth": True, "data": {"job_ids": [1]}},
        {"name": "Analyze", "method": "GET", "path": "/analyze/7", "timeout": 20, "auth": True}
    ]
    
    results = {}
    
    for test in tests:
        print(f"\nValidating {test['name']}...")
        try:
            url = f"{base_url}{test['path']}"
            req_headers = headers if test.get("auth") else {}
            
            if test["method"] == "GET":
                response = requests.get(url, headers=req_headers, timeout=test["timeout"])
            else:
                response = requests.post(url, json=test.get("data", {}), headers=req_headers, timeout=test["timeout"])
            
            if response.status_code == 200:
                data = response.json()
                results[test['name']] = {
                    "status": "PASS",
                    "response_time": f"{response.elapsed.total_seconds():.1f}s",
                    "schema": list(data.keys()) if isinstance(data, dict) else ["non-dict"],
                    "data_sample": str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
                }
                print(f"  PASS - {response.elapsed.total_seconds():.1f}s")
                print(f"    Schema: {list(data.keys()) if isinstance(data, dict) else ['non-dict']}")
            else:
                results[test['name']] = {
                    "status": "FAIL",
                    "error": f"HTTP {response.status_code}",
                    "message": response.text[:100]
                }
                print(f"  FAIL - HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            results[test['name']] = {"status": "TIMEOUT", "timeout": f"{test['timeout']}s"}
            print(f"  TIMEOUT - >{test['timeout']}s")
        except Exception as e:
            results[test['name']] = {"status": "ERROR", "error": str(e)[:50]}
            print(f"  ERROR - {str(e)[:50]}")
    
    # Summary
    print(f"\n{'='*50}")
    print("VALIDATION SUMMARY:")
    
    passed = sum(1 for r in results.values() if r.get("status") == "PASS")
    total = len(results)
    
    print(f"Status: {passed}/{total} endpoints validated successfully")
    
    for name, result in results.items():
        status = result.get("status", "UNKNOWN")
        if status == "PASS":
            print(f"  PASS {name}: {result.get('response_time', 'N/A')}")
        else:
            print(f"  FAIL {name}: {status}")
    
    if passed == total:
        print("\nALL ENDPOINTS VALIDATED SUCCESSFULLY!")
    else:
        print(f"\n{total-passed} endpoints need attention")
    
    return results

if __name__ == "__main__":
    complete_validation()
