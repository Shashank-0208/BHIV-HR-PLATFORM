import requests

# Test Agent service directly
AGENT_URL = "https://bhiv-hr-agent-nhgg.onrender.com"
API_KEY = "<YOUR_API_KEY>"

print("Testing Agent Service Directly...")
print("=" * 40)

# Test 1: Agent Health
try:
    response = requests.get(f"{AGENT_URL}/health", timeout=10)
    print(f"Agent Health: {response.status_code}")
    if response.status_code == 200:
        print("Agent service is healthy")
    else:
        print(f"Agent health issue: {response.text[:100]}")
except Exception as e:
    print(f"Agent health error: {e}")

# Test 2: Agent Match Endpoint
try:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {"job_id": 1}
    
    response = requests.post(f"{AGENT_URL}/match", json=data, headers=headers, timeout=30)
    print(f"Agent Match: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Match successful: {len(result.get('top_candidates', []))} candidates")
    else:
        print(f"Match error: {response.text[:200]}")
        
except Exception as e:
    print(f"Agent match error: {e}")

print("\nDiagnosis:")
print("If Agent health works but match fails, it's an authentication or data issue")
print("If both fail, Agent service needs restart")
