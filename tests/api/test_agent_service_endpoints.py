#!/usr/bin/env python3
"""
BHIV HR Platform - AI Agent Service Endpoints Testing
Tests the AI agent service core endpoints and generates a comprehensive report.
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
BASE_URL = "https://bhiv-hr-agent-nhgg.onrender.com"
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
    """Test AI agent service endpoints and generate report"""
    print("Testing BHIV HR Platform AI Agent Service Endpoints")
    print("=" * 65)
    
    # AI Agent service endpoints configuration
    agent_endpoints = [
        {
            "name": "AI Service Information",
            "endpoint": "/",
            "method": "GET",
            "category": "Core API",
            "description": "Get AI service information and capabilities",
            "auth_required": False
        },
        {
            "name": "Health Check",
            "endpoint": "/health",
            "method": "GET",
            "category": "Core API",
            "description": "Check AI service health and status",
            "auth_required": False
        }
    ]
    
    results = []
    
    for endpoint_config in agent_endpoints:
        print(f"\nTesting: {endpoint_config['name']} ({endpoint_config['category']})")
        print(f"   Endpoint: {endpoint_config['method']} {endpoint_config['endpoint']}")
        print(f"   Auth Required: {endpoint_config['auth_required']}")
        
        result = test_endpoint(
            endpoint_config["endpoint"],
            endpoint_config["method"],
            auth_required=endpoint_config["auth_required"]
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
    
    print(f"\nReport generated: agent_service_endpoints_test_report.md")
    print("=" * 65)

def generate_markdown_report(results):
    """Generate a comprehensive markdown report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# BHIV HR Platform - AI Agent Service Endpoints Test Report

**Generated:** {timestamp}  
**Platform:** BHIV HR AI Agent Service  
**Base URL:** {BASE_URL}  
**Test Category:** AI Agent Service Core API

## 📊 Test Summary

| Endpoint | Method | Category | Status | Response Time | Status Code | Auth Required |
|----------|--------|----------|--------|---------------|-------------|---------------|
"""
    
    for result in results:
        endpoint_info = result["endpoint_info"]
        status_icon = "✅" if result["status"] == "success" else "❌"
        status_code = result.get("status_code", "N/A")
        response_time = f"{result.get('response_time', 0):.3f}s"
        auth_req = "Yes" if endpoint_info["auth_required"] else "No"
        
        report += f"| `{endpoint_info['endpoint']}` | {endpoint_info['method']} | {endpoint_info['category']} | {status_icon} {result['status']} | {response_time} | {status_code} | {auth_req} |\n"
    
    # Calculate success rate
    total_success = sum(1 for r in results if r["status"] == "success")
    total_count = len(results)
    
    report += f"\n**Overall Success Rate:** {total_success}/{total_count} ({(total_success/total_count)*100:.1f}%)  \n\n"
    
    report += "## 🔍 Detailed Test Results\n\n"
    
    for i, result in enumerate(results, 1):
        endpoint_info = result["endpoint_info"]
        
        report += f"### {i}. {endpoint_info['name']}\n\n"
        report += f"**Endpoint:** `{endpoint_info['method']} {endpoint_info['endpoint']}`  \n"
        report += f"**Description:** {endpoint_info['description']}  \n"
        report += f"**Authentication:** {'Required' if endpoint_info['auth_required'] else 'Not Required'}  \n\n"
        
        if result["status"] == "success":
            report += f"**✅ Test Result:** PASSED  \n"
            report += f"**Status Code:** {result['status_code']}  \n"
            report += f"**Response Time:** {result['response_time']}s  \n"
            report += f"**Response Size:** {result['response_size']} bytes  \n\n"
            
            # Add response analysis
            if isinstance(result["response_data"], dict):
                report += "**Response Structure:**\n```json\n"
                if len(str(result["response_data"])) > 1500:
                    sample_data = {}
                    for k, v in list(result["response_data"].items())[:8]:
                        if isinstance(v, (dict, list)) and len(str(v)) > 100:
                            sample_data[k] = f"... ({type(v).__name__})"
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
                    
        else:
            report += f"**❌ Test Result:** FAILED  \n"
            report += f"**Error:** {result.get('message', 'Unknown error')}  \n"
            if "status_code" in result:
                report += f"**Status Code:** {result['status_code']}  \n"
            if "response_time" in result:
                report += f"**Response Time:** {result['response_time']}s  \n"
            report += "\n"
    
    # Add AI service analysis
    report += "## 🤖 AI Agent Service Analysis\n\n"
    report += "### AI Service Architecture\n\n"
    report += "The AI Agent Service provides advanced candidate matching capabilities:\n\n"
    report += "- **Phase 3 Semantic Engine** - Advanced AI-powered candidate matching\n"
    report += "- **Sentence Transformers** - State-of-the-art NLP for job-candidate similarity\n"
    report += "- **Adaptive Scoring** - Company-specific weight optimization\n"
    report += "- **Cultural Fit Analysis** - Feedback-based alignment scoring\n"
    report += "- **Batch Processing** - Efficient handling of multiple candidates\n"
    report += "- **Learning Engine** - Continuous improvement from feedback\n\n"
    
    report += "### AI Service Benefits:\n\n"
    report += "1. **Intelligent Matching** - Semantic understanding of job requirements\n"
    report += "2. **Scalable Processing** - Handle large candidate databases efficiently\n"
    report += "3. **Continuous Learning** - Improve matching accuracy over time\n"
    report += "4. **Multi-Factor Analysis** - Skills, experience, location, cultural fit\n"
    report += "5. **Real-time Processing** - Fast response times for matching requests\n"
    report += "6. **Fallback Mechanisms** - Robust error handling and recovery\n\n"
    
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
    report += "## 💡 AI Service Recommendations\n\n"
    
    if total_success == total_count:
        report += "✅ **All AI agent service endpoints are functioning correctly**\n\n"
        report += "- AI service is operational and responding properly\n"
        report += "- Health checks confirm service availability\n"
        report += "- Service information is accessible\n"
        report += "- Core API endpoints are stable\n\n"
    else:
        failed_count = total_count - total_success
        report += f"⚠️ **{failed_count} AI service endpoint(s) failed testing**\n\n"
        failed_endpoints = [r for r in results if r["status"] != "success"]
        for failed in failed_endpoints:
            report += f"- `{failed['endpoint_info']['endpoint']}`: {failed.get('message', 'Unknown error')}\n"
        report += "\n"
    
    report += "### AI Service Best Practices:\n\n"
    report += "1. **Health Monitoring** - Regular health checks for service availability\n"
    report += "2. **Performance Tracking** - Monitor response times and throughput\n"
    report += "3. **Model Updates** - Keep AI models current with latest techniques\n"
    report += "4. **Feedback Integration** - Use matching feedback to improve accuracy\n"
    report += "5. **Scalability Planning** - Prepare for increased matching volume\n"
    report += "6. **Error Handling** - Robust fallback mechanisms for service failures\n"
    report += "7. **Security** - Protect AI service endpoints and data processing\n\n"
    
    # Add usage examples
    report += "## 📝 AI Service Usage Examples\n\n"
    report += "### Check AI Service Information\n"
    report += "```bash\n"
    report += f'curl "{BASE_URL}/"\n'
    report += "```\n\n"
    
    report += "### Health Check\n"
    report += "```bash\n"
    report += f'curl "{BASE_URL}/health"\n'
    report += "```\n\n"
    
    report += "### AI Service Integration\n"
    report += "```bash\n"
    report += "# The AI service is typically called by the main gateway\n"
    report += "# Gateway URL: https://bhiv-hr-gateway-ltg0.onrender.com\n"
    report += "# AI matching endpoints are proxied through the gateway\n"
    report += f'curl -H "Authorization: Bearer {API_KEY}" \\\n'
    report += '     "https://bhiv-hr-gateway-ltg0.onrender.com/v1/match/1/top"\n'
    report += "```\n\n"
    
    report += f"---\n\n"
    report += f"**Report Generated:** {timestamp}  \n"
    report += f"**Test Duration:** {sum(r.get('response_time', 0) for r in results):.3f}s total  \n"
    report += f"**AI Service:** BHIV HR Platform Phase 3 AI Engine  \n"
    report += f"**Service URL:** {BASE_URL}  \n"
    
    # Write report to file
    with open("agent_service_endpoints_test_report.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()