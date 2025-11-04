import requests

def test_fixes():
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("Testing AI Matching Engine Fixes")
    print("=" * 40)
    
    # Test single match
    print("\n1. Single Match Test:")
    try:
        response = requests.get(f"{base_url}/v1/match/1/top", headers=headers, timeout=90)
        print(f"Status: {response.status_code}")
        print(f"Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            agent_status = data.get("agent_status", "unknown")
            reasoning = data.get("matches", [{}])[0].get("reasoning", "N/A")
            print(f"Agent Status: {agent_status}")
            print(f"Reasoning: {reasoning}")
            print(f"Fix Applied: {'YES' if 'skill matches' in reasoning else 'PARTIAL'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test batch match
    print("\n2. Batch Match Test:")
    try:
        response = requests.post(f"{base_url}/v1/match/batch", json=[1, 2], headers=headers, timeout=90)
        print(f"Status: {response.status_code}")
        print(f"Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status", "unknown")
            algorithm = data.get("algorithm_version", "N/A")
            print(f"Status: {status}")
            print(f"Algorithm: {algorithm}")
            print(f"Fallback Available: {'YES' if 'fallback' in algorithm else 'NO'}")
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\nFixes Summary:")
    print("1. Agent timeout: 30s -> 60s")
    print("2. Agent request format: Added candidate_ids")
    print("3. Batch fallback: Added fallback mechanism")
    print("4. Better scoring: Real skill/location matching")

if __name__ == "__main__":
    test_fixes()