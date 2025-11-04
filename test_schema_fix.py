import requests
import json

def test_schema_fix():
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    print("Testing Schema Fix - GET /v1/match/1/top")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}/v1/match/1/top", headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            actual_schema = list(data.keys())
            expected_schema = ["matches", "top_candidates", "job_id", "limit", "total_candidates", "algorithm_version", "processing_time", "ai_analysis", "agent_status"]
            
            schema_valid = all(key in actual_schema for key in expected_schema)
            missing = [k for k in expected_schema if k not in actual_schema]
            
            print(f"Expected Schema: {expected_schema}")
            print(f"Actual Schema: {actual_schema}")
            print(f"Schema Valid: {'YES' if schema_valid else 'NO'}")
            
            if missing:
                print(f"Missing Keys: {missing}")
            else:
                print("SUCCESS: All expected fields present!")
            
            # Check total_candidates specifically
            total_candidates = data.get("total_candidates")
            matches_count = len(data.get("matches", []))
            
            print(f"Total Candidates: {total_candidates}")
            print(f"Matches Count: {matches_count}")
            print(f"Values Match: {'YES' if total_candidates == matches_count else 'NO'}")
            
        else:
            print(f"FAILED - HTTP {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"ERROR - {str(e)}")

if __name__ == "__main__":
    test_schema_fix()