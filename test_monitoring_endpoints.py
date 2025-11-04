import requests
import json

def test_monitoring_endpoints():
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    headers = {"Authorization": "Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"}
    
    monitoring_endpoints = [
        {
            "name": "Prometheus Metrics",
            "method": "GET", 
            "path": "/metrics",
            "auth": False,
            "expected_format": "text/plain"
        },
        {
            "name": "Detailed Health Check", 
            "method": "GET",
            "path": "/health/detailed",
            "auth": True,
            "expected_schema": ["status", "timestamp", "system", "database", "services"]
        },
        {
            "name": "Metrics Dashboard",
            "method": "GET", 
            "path": "/metrics/dashboard",
            "auth": True,
            "expected_schema": ["system_metrics", "business_metrics", "performance_metrics"]
        }
    ]
    
    print("Gateway API - Monitoring Endpoints Testing")
    print("=" * 55)
    
    for endpoint in monitoring_endpoints:
        print(f"\n{endpoint['name']} - {endpoint['method']} {endpoint['path']}")
        print("-" * 50)
        
        try:
            url = f"{base_url}{endpoint['path']}"
            req_headers = headers if endpoint.get("auth") else {}
            
            response = requests.get(url, headers=req_headers, timeout=15)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Time: {response.elapsed.total_seconds():.2f}s")
            print(f"Content Type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code == 200:
                # Handle Prometheus metrics (text format)
                if endpoint.get("expected_format") == "text/plain":
                    lines = response.text.split('\n')[:10]  # First 10 lines
                    print(f"Metrics Format: Prometheus text")
                    print(f"Total Lines: {len(response.text.split())}")
                    print("Sample Metrics:")
                    for line in lines:
                        if line.strip() and not line.startswith('#'):
                            print(f"  {line}")
                            break
                    print("VALID - Prometheus metrics format")
                
                # Handle JSON responses
                else:
                    try:
                        data = response.json()
                        actual_schema = list(data.keys()) if isinstance(data, dict) else []
                        
                        print(f"Response Schema: {actual_schema}")
                        
                        if endpoint.get("expected_schema"):
                            expected = endpoint["expected_schema"]
                            schema_valid = all(key in actual_schema for key in expected)
                            missing = [k for k in expected if k not in actual_schema]
                            
                            print(f"Expected Schema: {expected}")
                            print(f"Schema Valid: {'YES' if schema_valid else 'NO'}")
                            if missing:
                                print(f"Missing Keys: {missing}")
                        
                        # Show sample data
                        print("Sample Response:")
                        sample = json.dumps(data, indent=2)[:300]
                        print(f"{sample}{'...' if len(str(data)) > 300 else ''}")
                        
                    except json.JSONDecodeError:
                        print("INVALID - Not valid JSON")
                        print(f"Raw Response: {response.text[:100]}...")
            else:
                print(f"FAILED - HTTP {response.status_code}")
                print(f"Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"ERROR - {str(e)}")
    
    print(f"\n{'='*55}")
    print("Monitoring endpoints testing complete!")

if __name__ == "__main__":
    test_monitoring_endpoints()