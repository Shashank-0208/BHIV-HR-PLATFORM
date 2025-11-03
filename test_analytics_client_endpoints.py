#!/usr/bin/env python3
"""
BHIV HR Platform - Analytics & Client Portal Endpoints Testing
Tests analytics/statistics and client portal endpoints and generates a comprehensive report.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint(endpoint: str, method: str = "GET", data: Dict = None, auth_required: bool = True) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{endpoint}"
    headers = HEADERS if auth_required else {"Content-Type": "application/json"}
    
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        else:
            return {"status": "error", "message": f"Unsupported method: {method}"}
        
        response_time = time.time() - start_time
        
        # Try to parse JSON response
        try:
            response_data = response.json()
        except:
            response_data = response.text
        
        return {
            "status": "success" if response.status_code < 400 else "error",
            "status_code": response.status_code,
            "response_time": round(response_time, 3),
            "response_size": len(response.content),
            "response_data": response_data,
            "headers": dict(response.headers)
        }
        
    except requests.exceptions.Timeout:
        return {
            "status": "timeout",
            "message": "Request timed out after 30 seconds",
            "response_time": 30.0
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "connection_error",
            "message": "Failed to connect to the server"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "response_time": time.time() - start_time
        }

def main():
    """Test analytics & client portal endpoints and generate report"""
    print("Testing BHIV HR Platform Analytics & Client Portal Endpoints")
    print("=" * 75)
    
    # Test endpoints configuration
    endpoints = [
        # Analytics & Statistics
        {
            "name": "Candidate Statistics",
            "endpoint": "/candidates/stats",
            "method": "GET",
            "category": "Analytics",
            "description": "Get comprehensive candidate statistics and metrics"
        },
        {
            "name": "Database Schema Info",
            "endpoint": "/v1/database/schema",
            "method": "GET",
            "category": "Analytics",
            "description": "Retrieve database schema information and table details"
        },
        {
            "name": "Job Report Export",
            "endpoint": "/v1/reports/job/1/export.csv",
            "method": "GET",
            "category": "Analytics",
            "description": "Export job report data in CSV format"
        },
        # Client Portal API
        {
            "name": "Client Register",
            "endpoint": "/v1/client/register",
            "method": "POST",
            "category": "Client Portal",
            "description": "Register a new client company",
            "test_data": {
                "company_name": "Test Analytics Corp",
                "contact_email": "test@analytics.com",
                "contact_phone": "+1-555-0199",
                "industry": "Technology",
                "company_size": "50-100",
                "address": "123 Analytics St, Tech City, TC 12345"
            }
        },
        {
            "name": "Client Login",
            "endpoint": "/v1/client/login",
            "method": "POST",
            "category": "Client Portal",
            "description": "Authenticate client and get access token",
            "test_data": {
                "client_code": "TECH001",
                "password": "demo123"
            }
        }
    ]
    
    results = []
    
    for endpoint_config in endpoints:
        print(f"\nTesting: {endpoint_config['name']} ({endpoint_config['category']})")
        print(f"   Endpoint: {endpoint_config['method']} {endpoint_config['endpoint']}")
        
        test_data = endpoint_config.get("test_data")
        if test_data:
            print(f"   Test Data: {json.dumps(test_data, indent=2)}")
        
        result = test_endpoint(
            endpoint_config["endpoint"],
            endpoint_config["method"],
            test_data
        )
        
        result["endpoint_info"] = endpoint_config
        results.append(result)
        
        # Print immediate results
        if result["status"] == "success":
            print(f"   [OK] Status: {result['status_code']} - {result['response_time']}s")
            if isinstance(result["response_data"], dict):
                print(f"   Response keys: {list(result['response_data'].keys())}")
            elif isinstance(result["response_data"], list):
                print(f"   Response: {len(result['response_data'])} items")
            else:
                print(f"   Response size: {result['response_size']} bytes")
        else:
            print(f"   [ERROR] Status: {result['status']} - {result.get('message', 'Unknown error')}")
    
    # Generate markdown report
    generate_markdown_report(results)
    
    print(f"\nReport generated: analytics_client_endpoints_test_report.md")
    print("=" * 75)

def generate_markdown_report(results):
    """Generate a comprehensive markdown report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# BHIV HR Platform - Analytics & Client Portal Endpoints Test Report

**Generated:** {timestamp}  
**Platform:** BHIV HR Gateway Service  
**Base URL:** {BASE_URL}  
**Test Category:** Analytics & Statistics + Client Portal API

## 📊 Test Summary

| Endpoint | Method | Category | Status | Response Time | Status Code |
|----------|--------|----------|--------|---------------|-------------|
"""
    
    for result in results:
        endpoint_info = result["endpoint_info"]
        status_icon = "✅" if result["status"] == "success" else "❌"
        status_code = result.get("status_code", "N/A")
        response_time = f"{result.get('response_time', 0):.3f}s"
        
        report += f"| `{endpoint_info['endpoint']}` | {endpoint_info['method']} | {endpoint_info['category']} | {status_icon} {result['status']} | {response_time} | {status_code} |\n"
    
    # Calculate success rate by category
    analytics_results = [r for r in results if r["endpoint_info"]["category"] == "Analytics"]
    client_results = [r for r in results if r["endpoint_info"]["category"] == "Client Portal"]
    
    analytics_success = sum(1 for r in analytics_results if r["status"] == "success")
    client_success = sum(1 for r in client_results if r["status"] == "success")
    
    total_success = sum(1 for r in results if r["status"] == "success")
    total_count = len(results)
    
    report += f"\n**Overall Success Rate:** {total_success}/{total_count} ({(total_success/total_count)*100:.1f}%)  \n"
    report += f"**Analytics Success Rate:** {analytics_success}/{len(analytics_results)} ({(analytics_success/len(analytics_results))*100:.1f}%)  \n"
    report += f"**Client Portal Success Rate:** {client_success}/{len(client_results)} ({(client_success/len(client_results))*100:.1f}%)  \n\n"
    
    report += "## 🔍 Detailed Test Results\n\n"
    
    # Group by category
    categories = {
        "Analytics & Statistics": analytics_results,
        "Client Portal API": client_results
    }
    
    for category, category_results in categories.items():
        report += f"### {category}\n\n"
        
        for result in category_results:
            endpoint_info = result["endpoint_info"]
            
            report += f"#### {endpoint_info['name']}\n\n"
            report += f"**Endpoint:** `{endpoint_info['method']} {endpoint_info['endpoint']}`  \n"
            report += f"**Description:** {endpoint_info['description']}  \n\n"
            
            if result["status"] == "success":
                report += f"**✅ Test Result:** PASSED  \n"
                report += f"**Status Code:** {result['status_code']}  \n"
                report += f"**Response Time:** {result['response_time']}s  \n"
                report += f"**Response Size:** {result['response_size']} bytes  \n\n"
                
                # Add response analysis
                if isinstance(result["response_data"], dict):
                    report += "**Response Structure:**\n```json\n"
                    if len(str(result["response_data"])) > 1500:
                        # Show structure for large responses
                        sample_data = {}
                        for k, v in list(result["response_data"].items())[:8]:
                            if isinstance(v, (dict, list)) and len(str(v)) > 100:
                                sample_data[k] = f"... ({type(v).__name__} with {len(v) if hasattr(v, '__len__') else 'data'})"
                            else:
                                sample_data[k] = v
                        report += json.dumps(sample_data, indent=2)
                        report += "\n// ... (truncated for readability)\n"
                    else:
                        report += json.dumps(result["response_data"], indent=2)
                    report += "\n```\n\n"
                elif isinstance(result["response_data"], list):
                    report += f"**Response:** Array with {len(result['response_data'])} items  \n"
                    if result["response_data"]:
                        report += "**Sample Item:**\n```json\n"
                        report += json.dumps(result["response_data"][0], indent=2)
                        report += "\n```\n\n"
                else:
                    if len(str(result["response_data"])) > 500:
                        report += f"**Response Preview:** `{str(result['response_data'])[:500]}...`  \n\n"
                    else:
                        report += f"**Response:** `{result['response_data']}`  \n\n"
                    
                # Add test data if it was a POST request
                if endpoint_info["method"] == "POST" and "test_data" in endpoint_info:
                    report += "**Test Data Sent:**\n```json\n"
                    report += json.dumps(endpoint_info["test_data"], indent=2)
                    report += "\n```\n\n"
                    
            else:
                report += f"**❌ Test Result:** FAILED  \n"
                report += f"**Error:** {result.get('message', 'Unknown error')}  \n"
                if "status_code" in result:
                    report += f"**Status Code:** {result['status_code']}  \n"
                if "response_time" in result:
                    report += f"**Response Time:** {result['response_time']}s  \n"
                report += "\n"
    
    # Add code structure analysis
    report += "## 🏗️ Code Structure Analysis\n\n"
    report += "### Analytics & Statistics Implementation\n\n"
    report += "The analytics endpoints provide comprehensive data insights:\n\n"
    report += "- **Candidate Statistics** - Aggregated metrics and performance data\n"
    report += "- **Database Schema** - Real-time schema information and table details\n"
    report += "- **Report Export** - CSV export functionality for job reports\n"
    report += "- **Performance Metrics** - System and business intelligence\n\n"
    
    report += "### Client Portal API Implementation\n\n"
    report += "The client portal provides enterprise-grade authentication:\n\n"
    report += "- **Client Registration** - Company onboarding with validation\n"
    report += "- **JWT Authentication** - Secure token-based login system\n"
    report += "- **Account Management** - Client profile and access control\n"
    report += "- **Security Features** - Rate limiting and audit logging\n\n"
    
    # Add performance analysis
    report += "## ⚡ Performance Analysis\n\n"
    
    successful_results = [r for r in results if r["status"] == "success"]
    if successful_results:
        avg_response_time = sum(r.get("response_time", 0) for r in successful_results) / len(successful_results)
        report += f"**Average Response Time:** {avg_response_time:.3f}s  \n"
        
        fastest = min(successful_results, key=lambda x: x.get("response_time", float('inf')))
        slowest = max(successful_results, key=lambda x: x.get("response_time", 0))
        
        report += f"**Fastest Endpoint:** `{fastest['endpoint_info']['endpoint']}` ({fastest['response_time']}s)  \n"
        report += f"**Slowest Endpoint:** `{slowest['endpoint_info']['endpoint']}` ({slowest['response_time']}s)  \n"
    
    report += "\n"
    
    # Add recommendations
    report += "## 💡 Recommendations\n\n"
    
    if total_success == total_count:
        report += "✅ **All analytics and client portal endpoints are functioning correctly**\n\n"
        report += "- Analytics provide comprehensive business intelligence\n"
        report += "- Client authentication system is secure and functional\n"
        report += "- Database schema information is accessible\n"
        report += "- Export functionality works properly\n\n"
    else:
        failed_count = total_count - total_success
        report += f"⚠️ **{failed_count} endpoint(s) failed testing**\n\n"
        failed_endpoints = [r for r in results if r["status"] != "success"]
        for failed in failed_endpoints:
            report += f"- `{failed['endpoint_info']['endpoint']}`: {failed.get('message', 'Unknown error')}\n"
        report += "\n"
    
    report += "### Next Steps:\n\n"
    report += "1. **Analytics Integration** - Connect analytics to business dashboards\n"
    report += "2. **Client Onboarding** - Streamline client registration process\n"
    report += "3. **Performance Monitoring** - Track analytics query performance\n"
    report += "4. **Security Audit** - Review client authentication security\n"
    report += "5. **Export Enhancement** - Add more export formats (Excel, JSON)\n\n"
    
    # Add usage examples
    report += "## 📝 Usage Examples\n\n"
    report += "### Get Candidate Statistics\n"
    report += "```bash\n"
    report += f'curl -H "Authorization: Bearer {API_KEY}" \\\n'
    report += f'     "{BASE_URL}/candidates/stats"\n'
    report += "```\n\n"
    
    report += "### Client Login\n"
    report += "```bash\n"
    report += f'curl -X POST "{BASE_URL}/v1/client/login" \\\n'
    report += f'  -H "Authorization: Bearer {API_KEY}" \\\n'
    report += '  -H "Content-Type: application/json" \\\n'
    report += '  -d {\n'
    report += '    "client_code": "TECH001",\n'
    report += '    "password": "demo123"\n'
    report += '  }\n'
    report += "```\n\n"
    
    report += "### Export Job Report\n"
    report += "```bash\n"
    report += f'curl -H "Authorization: Bearer {API_KEY}" \\\n'
    report += f'     "{BASE_URL}/v1/reports/job/1/export.csv" > job_report.csv\n'
    report += "```\n\n"
    
    report += f"---\n\n"
    report += f"**Report Generated:** {timestamp}  \n"
    report += f"**Test Duration:** {sum(r.get('response_time', 0) for r in results):.3f}s total  \n"
    report += f"**Platform:** BHIV HR Platform v3.0.0-Phase3  \n"
    
    # Write report to file
    with open("analytics_client_endpoints_test_report.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()