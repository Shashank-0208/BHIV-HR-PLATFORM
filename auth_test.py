import requests

def test_auth_formats():
    api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
    base_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
    
    # Test different auth formats
    auth_formats = [
        {"Authorization": f"Bearer {api_key}"},
        {"Authorization": f"API-Key {api_key}"},
        {"X-API-Key": api_key},
        {"api-key": api_key}
    ]
    
    endpoints = [
        "/health",
        "/v1/jobs", 
        "/v1/candidates"
    ]
    
    print("Testing Authorization Formats")
    print("=" * 50)
    
    for i, headers in enumerate(auth_formats, 1):
        print(f"\nFormat {i}: {headers}")
        
        for endpoint in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                response = requests.get(url, headers=headers, timeout=10)
                
                status = "SUCCESS" if response.status_code == 200 else f"FAILED ({response.status_code})"
                print(f"  {endpoint:15} | {status}")
                
                if response.status_code == 401:
                    print(f"    Error: {response.text[:100]}")
                elif response.status_code == 200 and endpoint != "/health":
                    print(f"    Response: {response.text[:50]}...")
                    
            except Exception as e:
                print(f"  {endpoint:15} | ERROR: {str(e)[:50]}")

if __name__ == "__main__":
    test_auth_formats()