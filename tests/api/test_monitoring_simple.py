import requests
import json
import time
from datetime import datetime

BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

def test_endpoint(endpoint, auth_required=True):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {API_KEY}"} if auth_required else {}
    
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=30)
        response_time = time.time() - start_time
        
        try:
            data = response.json()
        except:
            data = response.text
        
        return {
            "status": "success" if response.status_code < 400 else "error",
            "status_code": response.status_code,
            "response_time": round(response_time, 3),
            "data": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    print("Testing Monitoring Endpoints")
    print("=" * 40)
    
    endpoints = [
        {"name": "Prometheus Metrics", "endpoint": "/metrics", "auth": False},
        {"name": "Detailed Health", "endpoint": "/health/detailed", "auth": True},
        {"name": "Metrics Dashboard", "endpoint": "/metrics/dashboard", "auth": True}
    ]
    
    results = []
    
    for ep in endpoints:
        print(f"\nTesting: {ep['name']}")
        result = test_endpoint(ep["endpoint"], ep["auth"])
        result["name"] = ep["name"]
        result["endpoint"] = ep["endpoint"]
        results.append(result)
        
        if result["status"] == "success":
            print(f"  [OK] {result['status_code']} - {result['response_time']}s")
        else:
            print(f"  [ERROR] {result.get('message', 'Failed')}")
    
    # Generate report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# BHIV HR Platform - Monitoring Endpoints Test Report

**Generated:** {timestamp}
**Platform:** BHIV HR Gateway Service
**Base URL:** {BASE_URL}

## Test Summary

| Endpoint | Status | Response Time | Status Code |
|----------|--------|---------------|-------------|
"""
    
    for result in results:
        status_icon = "OK" if result["status"] == "success" else "ERROR"
        status_code = result.get("status_code", "N/A")
        response_time = f"{result.get('response_time', 0):.3f}s"
        
        report += f"| `{result['endpoint']}` | {status_icon} | {response_time} | {status_code} |\n"
    
    report += "\n## Detailed Results\n\n"
    
    for i, result in enumerate(results, 1):
        report += f"### {i}. {result['name']}\n\n"
        report += f"**Endpoint:** `GET {result['endpoint']}`\n\n"
        
        if result["status"] == "success":
            report += f"**Status:** PASSED\n"
            report += f"**Status Code:** {result['status_code']}\n"
            report += f"**Response Time:** {result['response_time']}s\n\n"
            
            if isinstance(result["data"], dict):
                report += "**Response Structure:**\n```json\n"
                if len(str(result["data"])) > 500:
                    keys = list(result["data"].keys())[:5]
                    report += json.dumps({k: "..." for k in keys}, indent=2)
                    report += "\n// ... (truncated)\n"
                else:
                    report += json.dumps(result["data"], indent=2)
                report += "\n```\n\n"
        else:
            report += f"**Status:** FAILED\n"
            report += f"**Error:** {result.get('message', 'Unknown error')}\n\n"
    
    report += "## Code Structure Analysis\n\n"
    report += "The monitoring endpoints are implemented in:\n\n"
    report += "- `services/gateway/app/main.py` - Main endpoint definitions\n"
    report += "- `services/gateway/app/monitoring.py` - Advanced monitoring system\n\n"
    
    report += "### Key Features:\n\n"
    report += "1. **Prometheus Integration** - Metrics export in Prometheus format\n"
    report += "2. **System Health Monitoring** - CPU, memory, disk usage tracking\n"
    report += "3. **Performance Metrics** - Response times, error rates, throughput\n"
    report += "4. **Business Metrics** - Job postings, matches, user activity\n\n"
    
    success_count = sum(1 for r in results if r["status"] == "success")
    
    if success_count == len(results):
        report += "## Status: ALL TESTS PASSED\n\n"
        report += "All monitoring endpoints are functioning correctly.\n"
    else:
        report += f"## Status: {len(results) - success_count} TESTS FAILED\n\n"
        report += "Some monitoring endpoints need attention.\n"
    
    with open("monitoring_endpoints_test_report.md", "w") as f:
        f.write(report)
    
    print(f"\nReport saved: monitoring_endpoints_test_report.md")

if __name__ == "__main__":
    main()