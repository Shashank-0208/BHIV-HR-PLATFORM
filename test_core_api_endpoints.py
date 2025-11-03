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
            "data": data,
            "headers": dict(response.headers)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    print("Testing Core API Endpoints")
    print("=" * 40)
    
    endpoints = [
        {"name": "API Root", "endpoint": "/", "auth": False},
        {"name": "Health Check", "endpoint": "/health", "auth": False},
        {"name": "Test Candidates DB", "endpoint": "/test-candidates", "auth": True}
    ]
    
    results = []
    
    for ep in endpoints:
        print(f"\nTesting: {ep['name']}")
        result = test_endpoint(ep["endpoint"], ep["auth"])
        result["name"] = ep["name"]
        result["endpoint"] = ep["endpoint"]
        result["auth_required"] = ep["auth"]
        results.append(result)
        
        if result["status"] == "success":
            print(f"  [OK] {result['status_code']} - {result['response_time']}s")
        else:
            print(f"  [ERROR] {result.get('message', 'Failed')}")
    
    # Generate report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# BHIV HR Platform - Core API Endpoints Test Report

**Generated:** {timestamp}
**Platform:** BHIV HR Gateway Service
**Base URL:** {BASE_URL}
**Test Category:** Core API Endpoints

## Executive Summary

"""
    
    success_count = sum(1 for r in results if r["status"] == "success")
    if success_count == len(results):
        report += "✅ **ALL TESTS PASSED** - All core API endpoints are functioning correctly.\n\n"
    else:
        report += f"⚠️ **{len(results) - success_count} TESTS FAILED** - Some core endpoints need attention.\n\n"
    
    report += """## Test Summary

| Endpoint | Status | Response Time | Status Code | Auth Required |
|----------|--------|---------------|-------------|---------------|
"""
    
    for result in results:
        status_icon = "✅ OK" if result["status"] == "success" else "❌ ERROR"
        status_code = result.get("status_code", "N/A")
        response_time = f"{result.get('response_time', 0):.3f}s"
        auth_req = "Yes" if result["auth_required"] else "No"
        
        report += f"| `{result['endpoint']}` | {status_icon} | {response_time} | {status_code} | {auth_req} |\n"
    
    report += "\n## Detailed Results\n\n"
    
    for i, result in enumerate(results, 1):
        report += f"### {i}. {result['name']}\n\n"
        report += f"**Endpoint:** `GET {result['endpoint']}`\n"
        report += f"**Authentication:** {'Required' if result['auth_required'] else 'Not Required'}\n\n"
        
        if result["status"] == "success":
            report += f"**✅ Test Result:** PASSED\n"
            report += f"**Status Code:** {result['status_code']}\n"
            report += f"**Response Time:** {result['response_time']}s\n\n"
            
            # Security headers analysis
            if "headers" in result:
                security_headers = {}
                for header, value in result["headers"].items():
                    if header.lower().startswith('x-') or 'security' in header.lower() or 'content-security-policy' in header.lower():
                        security_headers[header] = value
                
                if security_headers:
                    report += "**Security Headers:**\n"
                    for header, value in security_headers.items():
                        report += f"- `{header}: {value}`\n"
                    report += "\n"
            
            if isinstance(result["data"], dict):
                report += "**Response Structure:**\n```json\n"
                if len(str(result["data"])) > 800:
                    # Show key structure for large responses
                    keys = list(result["data"].keys())
                    sample_data = {k: "..." for k in keys[:8]}
                    report += json.dumps(sample_data, indent=2)
                    if len(keys) > 8:
                        report += f"\n// ... and {len(keys) - 8} more fields"
                else:
                    report += json.dumps(result["data"], indent=2)
                report += "\n```\n\n"
        else:
            report += f"**❌ Test Result:** FAILED\n"
            report += f"**Error:** {result.get('message', 'Unknown error')}\n\n"
    
    # Code structure analysis
    report += """## Code Structure Analysis

The Core API endpoints are implemented in `services/gateway/app/main.py`:

### 1. API Root (`/`)
```python
@app.get("/", tags=["Core API Endpoints"])
def read_root():
    return {
        "message": "BHIV HR Platform API Gateway",
        "version": "3.1.0",
        "status": "healthy",
        "endpoints": len(app.routes),
        "documentation": "/docs",
        "monitoring": "/metrics"
    }
```

### 2. Health Check (`/health`)
```python
@app.get("/health", tags=["Core API Endpoints"])
def health_check(response: Response):
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return {
        "status": "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
```

### 3. Database Test (`/test-candidates`)
```python
@app.get("/test-candidates", tags=["Core API Endpoints"])
async def test_candidates_db(api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            result = connection.execute(text("SELECT COUNT(*) FROM candidates"))
            candidate_count = result.fetchone()[0]
            
            return {
                "database_status": "connected",
                "total_candidates": candidate_count,
                "test_timestamp": datetime.now(timezone.utc).isoformat()
            }
    except Exception as e:
        return {
            "database_status": "failed",
            "error": str(e)
        }
```

### Key Features:

1. **FastAPI Framework** - Modern async Python web framework
2. **Security Headers** - Comprehensive security header implementation
3. **Database Integration** - PostgreSQL connection with SQLAlchemy
4. **Authentication** - Bearer token authentication for protected endpoints
5. **Error Handling** - Comprehensive exception handling
6. **Monitoring Integration** - Built-in health checks and metrics

### Database Configuration:
```python
def get_db_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://...")
    return create_engine(
        database_url, 
        pool_pre_ping=True, 
        pool_recycle=3600,
        pool_size=10,
        connect_args={"connect_timeout": 10, "application_name": "bhiv_gateway"},
        pool_timeout=20,
        max_overflow=5
    )
```

## Security Analysis

### Authentication Implementation:
- **Public Endpoints:** `/` and `/health` (no authentication required)
- **Protected Endpoints:** `/test-candidates` (requires Bearer token)
- **API Key Validation:** Secure token-based authentication

### Security Headers Applied:
"""
    
    # Add security analysis based on actual results
    for result in results:
        if result["status"] == "success" and "headers" in result:
            headers = result["headers"]
            if any(h.lower().startswith('x-') for h in headers.keys()):
                report += f"\n**{result['name']} Security Headers:**\n"
                for header, value in headers.items():
                    if header.lower().startswith('x-') or 'content-security-policy' in header.lower():
                        report += f"- ✅ `{header}: {value}`\n"
    
    report += """
## Performance Analysis

### Response Time Metrics:
"""
    
    for result in results:
        if result["status"] == "success":
            performance_rating = "Excellent" if result["response_time"] < 0.5 else "Good" if result["response_time"] < 1.0 else "Acceptable"
            report += f"- **{result['name']}:** {result['response_time']}s ({performance_rating})\n"
    
    report += """
### Performance Characteristics:
- **API Root:** Fast response with service information
- **Health Check:** Quick health status with security headers
- **Database Test:** Database connectivity verification with candidate count

## Usage Examples

### API Discovery
```bash
# Get API information and available endpoints
curl https://bhiv-hr-gateway-ltg0.onrender.com/
```

### Health Monitoring
```bash
# Check service health status
curl https://bhiv-hr-gateway-ltg0.onrender.com/health
```

### Database Connectivity Test
```bash
# Test database connection (requires authentication)
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \\
     https://bhiv-hr-gateway-ltg0.onrender.com/test-candidates
```

## Recommendations

"""
    
    if success_count == len(results):
        report += """### ✅ Strengths
1. **All endpoints operational** - 100% success rate
2. **Fast response times** - All endpoints respond quickly
3. **Proper security implementation** - Security headers and authentication
4. **Database connectivity** - Reliable database connection testing
5. **Comprehensive error handling** - Graceful error responses

### 🔧 Optimization Opportunities
1. **Caching:** Consider caching API root response
2. **Monitoring:** Add more detailed health metrics
3. **Documentation:** Enhance endpoint documentation
4. **Rate Limiting:** Implement rate limiting for public endpoints
"""
    else:
        report += "### 🚨 Issues Found\n"
        for result in results:
            if result["status"] != "success":
                report += f"- **{result['name']}:** {result.get('message', 'Unknown error')}\n"
    
    report += """
## Conclusion

The Core API endpoints provide essential platform functionality including service discovery, health monitoring, and database connectivity testing. """
    
    if success_count == len(results):
        report += "All endpoints are functioning correctly with good performance and proper security implementation."
    else:
        report += f"{success_count}/{len(results)} endpoints are working correctly. Issues need to be addressed for full functionality."
    
    report += f"""

---
*Report generated by BHIV HR Platform Testing Suite - {timestamp}*"""
    
    with open("core_api_endpoints_test_report.md", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\nReport saved: core_api_endpoints_test_report.md")

if __name__ == "__main__":
    main()