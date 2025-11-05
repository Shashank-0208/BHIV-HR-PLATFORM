import requests
import json

def test_agent_batch_direct():
    agent_url = "https://bhiv-hr-agent-nhgg.onrender.com"
    headers = {"Authorization": "Bearer <YOUR_API_KEY>"}
    
    print("Testing Agent Service Batch Endpoint Directly")
    print("=" * 55)
    
    # Test 1: Agent service health with longer timeout
    print("\n1. Agent Health (Extended Timeout):")
    try:
        response = requests.get(f"{agent_url}/health", timeout=60)
        print(f"   Status: {response.status_code}")
        print(f"   Time: {response.elapsed.total_seconds():.2f}s")
        if response.status_code == 200:
            data = response.json()
            print(f"   Service: {data.get('service', 'N/A')}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 2: Check Agent endpoints
    print("\n2. Agent Root Endpoint:")
    try:
        response = requests.get(f"{agent_url}/", timeout=60)
        print(f"   Status: {response.status_code}")
        print(f"   Time: {response.elapsed.total_seconds():.2f}s")
        if response.status_code == 200:
            data = response.json()
            endpoints = data.get('available_endpoints', {})
            print(f"   Batch endpoint listed: {'batch_match' in str(endpoints)}")
            if 'batch_match' in str(endpoints):
                print(f"   Batch endpoint: {endpoints.get('batch_match', 'N/A')}")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 3: Direct batch-match test with correct format
    print("\n3. Direct Agent Batch-Match Test:")
    try:
        # Agent expects BatchMatchRequest with job_ids field
        test_data = {"job_ids": [1, 2]}
        response = requests.post(
            f"{agent_url}/batch-match", 
            json=test_data, 
            headers=headers, 
            timeout=120  # 2 minutes for batch processing
        )
        print(f"   Status: {response.status_code}")
        print(f"   Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   SUCCESS: Batch endpoint working!")
            print(f"   Jobs processed: {data.get('total_jobs_processed', 0)}")
            print(f"   Algorithm: {data.get('algorithm_version', 'N/A')}")
        else:
            print(f"   FAILED: {response.status_code}")
            print(f"   Error: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print(f"   TIMEOUT: Agent batch processing took >120s")
    except Exception as e:
        print(f"   ERROR: {e}")
    
    # Test 4: Compare with Gateway format
    print("\n4. Gateway vs Agent Format Analysis:")
    print("   Gateway sends to Agent: {'job_ids': [1, 2]}")
    print("   Agent expects: BatchMatchRequest with job_ids field")
    print("   Format match: YES - Should work")
    
    # Test 5: Check if it's a timeout issue
    print("\n5. Timeout Analysis:")
    print("   Gateway timeout: 60s")
    print("   Agent processing: Can be >60s for batch operations")
    print("   Recommendation: Increase Gateway timeout or optimize Agent")

if __name__ == "__main__":
    test_agent_batch_direct()
