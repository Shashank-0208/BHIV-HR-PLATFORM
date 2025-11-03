import requests
import json
import time

# Test configuration
BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-nhgg.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(name, url, method="GET", data=None, timeout=30):
    """Test a single endpoint with detailed error reporting"""
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"Method: {method}")
    
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=timeout)
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response_time}s")
        
        if response.status_code < 400:
            print("✅ SUCCESS")
            if response.headers.get('content-type', '').startswith('application/json'):
                result = response.json()
                if 'agent_status' in result:
                    print(f"Agent Status: {result['agent_status']}")
                if 'algorithm_version' in result:
                    print(f"Algorithm: {result['algorithm_version']}")
                return True, result
            return True, response.text[:200]
        else:
            print("❌ FAILED")
            print(f"Error: {response.text[:200]}")
            return False, response.text[:200]
            
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT")
        return False, "Request timed out"
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False, str(e)

def main():
    print("BHIV HR Platform - Comprehensive Deployment Test")
    print("Testing after Gateway service redeploy...")
    
    tests = [
        ("Health Check", f"{BASE_URL}/health"),
        ("Database Schema", f"{BASE_URL}/v1/database/schema"),
        ("Agent Service Health", f"{AGENT_URL}/health"),
        ("AI Matching (Critical Test)", f"{BASE_URL}/v1/match/1/top"),
        ("Client Login", f"{BASE_URL}/v1/client/login", "POST", {"client_id": "TECH001", "password": "demo123"}),
        ("Jobs List", f"{BASE_URL}/v1/jobs"),
        ("Candidates List", f"{BASE_URL}/v1/candidates")
    ]
    
    results = []
    for test_name, url, *args in tests:
        method = args[0] if args else "GET"
        data = args[1] if len(args) > 1 else None
        success, response = test_endpoint(test_name, url, method, data)
        results.append((test_name, success, response))
    
    # Summary
    print(f"\n{'='*60}")
    print("DEPLOYMENT TEST SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, response in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:<30} {status}")
    
    print(f"\nOverall: {successful}/{total} tests passed ({successful/total*100:.1f}%)")
    
    # Critical issue analysis
    print(f"\n{'='*60}")
    print("CRITICAL ISSUE ANALYSIS")
    print(f"{'='*60}")
    
    ai_test = next((r for name, success, r in results if "AI Matching" in name), None)
    if ai_test:
        if isinstance(ai_test, dict) and ai_test.get('agent_status') == 'connected':
            print("✅ AI Matching: Agent service connected successfully")
        elif isinstance(ai_test, dict) and ai_test.get('agent_status') == 'disconnected':
            print("❌ AI Matching: Still using database fallback")
        else:
            print("❌ AI Matching: Connection issues persist")
    
    client_test = next((success for name, success, _ in results if "Client Login" in name), None)
    if client_test:
        print("✅ Client Login: Database schema fix successful")
    else:
        print("❌ Client Login: Still has issues")
    
    if successful == total:
        print("\n🎉 ALL SYSTEMS OPERATIONAL - Deployment successful!")
    else:
        print(f"\n⚠️  {total - successful} issues remaining")

if __name__ == "__main__":
    main()