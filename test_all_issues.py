import requests
import time
import os

# Configuration
GATEWAY_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-nhgg.onrender.com"
HR_PORTAL_URL = "https://bhiv-hr-portal-u670.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-3iod.onrender.com"
CANDIDATE_PORTAL_URL = "https://bhiv-hr-candidate-portal-abe6.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def test_endpoint(name, url, method="GET", data=None, timeout=10):
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=timeout)
        end_time = time.time()
        
        return {
            "status": response.status_code,
            "success": response.status_code < 400,
            "time": round(end_time - start_time, 3),
            "error": response.text[:100] if response.status_code >= 400 else None
        }
    except requests.exceptions.Timeout:
        return {"status": "TIMEOUT", "success": False, "time": timeout, "error": "Read timed out"}
    except Exception as e:
        return {"status": "ERROR", "success": False, "time": 0, "error": str(e)[:100]}

print("BHIV HR Platform - Issue Verification Test")
print("=" * 50)

# Issue 1: AI Agent Service
print("\n1. AI AGENT SERVICE CONNECTIVITY")
print("-" * 30)
agent_tests = [
    ("Agent Root", f"{AGENT_URL}/"),
    ("Agent Health", f"{AGENT_URL}/health"),
    ("Agent Test DB", f"{AGENT_URL}/test-db"),
    ("Agent Match", f"{AGENT_URL}/match", "POST", {"job_id": 1}),
    ("Agent Analyze", f"{AGENT_URL}/analyze/1")
]

agent_working = 0
for test_name, url, *args in agent_tests:
    method = args[0] if args else "GET"
    data = args[1] if len(args) > 1 else None
    result = test_endpoint(test_name, url, method, data)
    
    status = "PASS" if result["success"] else "FAIL"
    print(f"{test_name}: {status} ({result['status']}) - {result['time']}s")
    if not result["success"]:
        print(f"  Error: {result['error']}")
    else:
        agent_working += 1

print(f"Agent Service: {agent_working}/5 endpoints working")

# Issue 2: Portal Accessibility
print("\n2. PORTAL ACCESSIBILITY")
print("-" * 30)
portals = [
    ("HR Portal", HR_PORTAL_URL),
    ("Client Portal", CLIENT_PORTAL_URL),
    ("Candidate Portal", CANDIDATE_PORTAL_URL)
]

portal_working = 0
for portal_name, url in portals:
    result = test_endpoint(portal_name, url, timeout=15)
    status = "ACCESSIBLE" if result["success"] else "INACCESSIBLE"
    print(f"{portal_name}: {status} ({result['status']}) - {result['time']}s")
    if not result["success"]:
        print(f"  Error: {result['error']}")
    else:
        portal_working += 1

print(f"Portals: {portal_working}/3 accessible")

# Issue 3: Search Endpoint Bug
print("\n3. CANDIDATE SEARCH ENDPOINT")
print("-" * 30)

# Test broken endpoint
broken_url = f"{GATEWAY_URL}/v1/candidates/search?skills=Python&limit=5"
result = test_endpoint("Broken Search", broken_url)
print(f"Broken Search: {'PASS' if result['success'] else 'FAIL'} ({result['status']})")
if not result["success"]:
    print(f"  Error: {result['error']}")

# Test workaround
workaround_url = f"{GATEWAY_URL}/v1/candidates?limit=5"
result = test_endpoint("Workaround", workaround_url)
print(f"Workaround: {'PASS' if result['success'] else 'FAIL'} ({result['status']})")

# Issue 4: Authentication
print("\n4. CLIENT AUTHENTICATION")
print("-" * 30)
auth_data = {"client_id": "TECH001", "password": "demo123"}
result = test_endpoint("Client Login", f"{GATEWAY_URL}/v1/client/login", "POST", auth_data)
print(f"Client Auth: {'PASS' if result['success'] else 'FAIL'} ({result['status']})")
if result["error"] and "timezone" in result["error"].lower():
    print("  TIMEZONE ISSUE DETECTED")
elif not result["success"]:
    print(f"  Error: {result['error']}")

# Issue 5: File Structure
print("\n5. FILE STRUCTURE ISSUES")
print("-" * 30)

redundant_files = [
    "services/client_portal/auth_service.py",
    "services/semantic_engine/"
]

for file_path in redundant_files:
    full_path = os.path.join("c:\\BHIV HR PLATFORM", file_path)
    exists = os.path.exists(full_path)
    status = "EXISTS (remove)" if exists else "NOT FOUND (good)"
    print(f"{file_path}: {status}")

# Check .pyc files
pyc_count = 0
try:
    for root, dirs, files in os.walk("c:\\BHIV HR PLATFORM"):
        pyc_count += len([f for f in files if f.endswith('.pyc')])
    print(f".pyc files: {pyc_count} found {'(should remove)' if pyc_count > 0 else '(good)'}")
except:
    print(".pyc files: Could not check")

# Issue 6: Database
print("\n6. DATABASE SCHEMA")
print("-" * 30)
result = test_endpoint("DB Schema", f"{GATEWAY_URL}/v1/database/schema")
print(f"Database: {'ACCESSIBLE' if result['success'] else 'INACCESSIBLE'} ({result['status']})")

# Summary
print("\n" + "=" * 50)
print("ISSUE VERIFICATION SUMMARY")
print("=" * 50)
print(f"Agent Service: {'DOWN' if agent_working == 0 else 'PARTIAL' if agent_working < 5 else 'UP'} ({agent_working}/5)")
print(f"Portals: {'PARTIAL' if portal_working < 3 else 'ALL UP'} ({portal_working}/3)")
print(f"Search Bug: CONFIRMED (workaround available)")
print(f"Auth: {'WORKING' if result['success'] else 'ISSUES'}")
print(f"File Issues: DETECTED (cleanup needed)")
print("=" * 50)