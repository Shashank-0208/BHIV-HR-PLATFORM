import requests

# Test the specific search endpoint bug mentioned
GATEWAY_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

print("Testing Candidate Search Endpoint Bug")
print("=" * 40)

# Test the exact URL mentioned in the issue
test_url = f"{GATEWAY_URL}/v1/candidates/search?skills=Python&limit=5"
print(f"Testing: {test_url}")

try:
    response = requests.get(test_url, headers=HEADERS, timeout=10)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 422:
        print("BUG CONFIRMED: 422 Unprocessable Entity")
        print("Response:", response.text[:300])
    elif response.status_code == 200:
        print("UNEXPECTED: Search endpoint is working")
        data = response.json()
        print(f"Found {data.get('count', 0)} candidates")
    else:
        print(f"OTHER ERROR: {response.status_code}")
        print("Response:", response.text[:200])
        
except Exception as e:
    print(f"REQUEST ERROR: {e}")

# Test if the issue is route order (search vs {candidate_id})
print("\nTesting route conflict...")
try:
    # This should try to get candidate with ID "search"
    conflict_url = f"{GATEWAY_URL}/v1/candidates/search"
    response = requests.get(conflict_url, headers=HEADERS, timeout=10)
    print(f"GET /v1/candidates/search (no params): {response.status_code}")
    
    if response.status_code == 422:
        print("ROUTE CONFLICT CONFIRMED: 'search' being parsed as candidate_id")
    elif response.status_code == 200:
        print("No route conflict detected")
        
except Exception as e:
    print(f"Conflict test error: {e}")

print("\nConclusion:")
print("The search endpoint issue needs to be verified with the exact parameters.")