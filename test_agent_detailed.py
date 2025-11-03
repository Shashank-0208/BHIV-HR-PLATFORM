import requests
import time

AGENT_URL = "https://bhiv-hr-agent-nhgg.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

print("Detailed Agent Service Analysis")
print("=" * 35)

# Test each endpoint with different timeouts
endpoints = [
    ("Root", "/", "GET", None),
    ("Health", "/health", "GET", None),
    ("Test DB", "/test-db", "GET", None),
    ("Match", "/match", "POST", {"job_id": 1}),
    ("Analyze", "/analyze/1", "GET", None)
]

for name, path, method, data in endpoints:
    url = f"{AGENT_URL}{path}"
    print(f"\nTesting {name}: {url}")
    
    # Try with increasing timeouts
    for timeout in [5, 15, 30]:
        try:
            start_time = time.time()
            if method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=timeout)
            else:
                response = requests.post(url, headers=HEADERS, json=data, timeout=timeout)
            end_time = time.time()
            
            print(f"  Timeout {timeout}s: SUCCESS ({response.status_code}) in {end_time-start_time:.2f}s")
            if response.status_code == 200:
                break
            else:
                print(f"    Error: {response.text[:100]}")
                
        except requests.exceptions.Timeout:
            print(f"  Timeout {timeout}s: TIMEOUT")
        except Exception as e:
            print(f"  Timeout {timeout}s: ERROR - {str(e)[:100]}")
            break

print("\nAgent Service Analysis Complete")
print("If Match and Analyze consistently timeout, the service needs restart.")