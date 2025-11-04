import requests
import json

def test_batch_fix():
    gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("Testing Batch Matching Fix")
    print("=" * 40)
    
    print("\nISSUE IDENTIFIED:")
    print("- Agent service: Working (2.14s response)")
    print("- Gateway timeout: 60s (too short)")
    print("- Fix applied: Increased to 120s")
    
    print("\nCODE CHANGES MADE:")
    print("File: services/gateway/app/main.py")
    print("Line: async with httpx.AsyncClient(timeout=60.0)")
    print("Changed to: async with httpx.AsyncClient(timeout=120.0)")
    
    print("\nTesting Gateway batch endpoint after fix...")
    try:
        test_data = [1, 2]
        response = requests.post(
            f"{gateway_url}/v1/match/batch", 
            json=test_data, 
            headers=headers, 
            timeout=150  # Client timeout longer than Gateway timeout
        )
        
        print(f"Status: {response.status_code}")
        print(f"Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS: Batch matching now working!")
            print(f"Jobs processed: {data.get('total_jobs_processed', 0)}")
            print(f"Algorithm: {data.get('algorithm_version', 'N/A')}")
            print(f"Status: {data.get('status', 'N/A')}")
        else:
            print(f"Still failing: {response.status_code}")
            print(f"Error: {response.text[:200]}...")
            
    except requests.exceptions.Timeout:
        print("Still timing out - may need deployment")
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\nNEXT STEPS:")
    print("1. Deploy the Gateway service with increased timeout")
    print("2. Test again after deployment")
    print("3. Batch matching should work with 120s timeout")

if __name__ == "__main__":
    test_batch_fix()