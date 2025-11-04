import requests
import json

def test_agent_final():
    base_url = "https://bhiv-hr-agent-nhgg.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("BHIV AI Agent Service - Final Test Results")
    print("=" * 50)
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Root (/)           | {'OK' if response.status_code == 200 else 'FAIL'} | {response.elapsed.total_seconds():.2f}s")
    except Exception as e:
        print(f"Root (/)           | ERROR | {str(e)[:30]}...")
    
    # Test 2: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"Health (/health)   | {'OK' if response.status_code == 200 else 'FAIL'} | {response.elapsed.total_seconds():.2f}s")
        if response.status_code == 200:
            data = response.json()
            print(f"                   Status: {data.get('status', 'unknown')}")
    except Exception as e:
        print(f"Health (/health)   | ERROR | {str(e)[:30]}...")
    
    # Test 3: Database test (authenticated)
    try:
        response = requests.get(f"{base_url}/test-db", headers=headers, timeout=10)
        print(f"DB Test (/test-db) | {'OK' if response.status_code == 200 else 'FAIL'} | {response.elapsed.total_seconds():.2f}s")
        if response.status_code == 200:
            data = response.json()
            print(f"                   DB Status: {data.get('status', 'unknown')}")
    except Exception as e:
        print(f"DB Test (/test-db) | ERROR | {str(e)[:30]}...")
    
    # Test 4: Single match (correct format)
    try:
        match_data = {"job_id": 1, "candidate_ids": [7]}
        response = requests.post(f"{base_url}/match", json=match_data, headers=headers, timeout=15)
        print(f"Match (/match)     | {'OK' if response.status_code == 200 else f'FAIL ({response.status_code})'} | {response.elapsed.total_seconds():.2f}s")
        if response.status_code == 200:
            data = response.json()
            print(f"                   Score: {data.get('match_score', 'N/A')}")
        else:
            print(f"                   Error: {response.text[:40]}...")
    except Exception as e:
        print(f"Match (/match)     | ERROR | {str(e)[:30]}...")
    
    # Test 5: Batch match (correct format)
    try:
        batch_data = {"job_ids": [1]}
        response = requests.post(f"{base_url}/batch-match", json=batch_data, headers=headers, timeout=20)
        print(f"Batch (/batch-match) | {'OK' if response.status_code == 200 else f'FAIL ({response.status_code})'} | {response.elapsed.total_seconds():.2f}s")
        if response.status_code == 200:
            data = response.json()
            print(f"                     Matches: {len(data.get('matches', []))}")
        else:
            print(f"                     Error: {response.text[:40]}...")
    except Exception as e:
        print(f"Batch (/batch-match) | ERROR | {str(e)[:30]}...")
    
    # Test 6: Analyze candidate
    try:
        response = requests.get(f"{base_url}/analyze/7", headers=headers, timeout=15)
        print(f"Analyze (/analyze/7) | {'OK' if response.status_code == 200 else f'FAIL ({response.status_code})'} | {response.elapsed.total_seconds():.2f}s")
        if response.status_code == 200:
            data = response.json()
            print(f"                     Analysis: {str(data)[:40]}...")
    except Exception as e:
        print(f"Analyze (/analyze/7) | ERROR | {str(e)[:30]}...")

if __name__ == "__main__":
    test_agent_final()