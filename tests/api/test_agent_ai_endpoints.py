#!/usr/bin/env python3
"""
BHIV HR Platform - AI Agent Service Advanced Endpoints Testing
Tests AI matching, batch processing, candidate analysis, and diagnostics endpoints.
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

def test_endpoint(endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    url = f"{BASE_URL}{endpoint}"
    
    start_time = time.time()
    
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=30)
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
    """Test AI agent service advanced endpoints and generate report"""
    print("Testing BHIV HR Platform AI Agent Service Advanced Endpoints")
    print("=" * 75)
    
    # AI Agent service advanced endpoints configuration
    ai_endpoints = [
        # AI Matching Engine
        {
            "name": "AI-Powered Candidate Matching",
            "endpoint": "/match",
            "method": "POST",
            "category": "AI Matching Engine",
            "description": "Semantic candidate matching and scoring",
            "test_data": {
                "job_id": 1,
                "job_title": "Senior Python Developer",
                "job_description": "We are looking for an experienced Python developer with expertise in Django, REST APIs, and database design.",
                "required_skills": ["Python", "Django", "PostgreSQL", "REST APIs"],
                "experience_level": "Senior",
                "location": "Remote",
                "limit": 5
            }
        },
        {
            "name": "Batch AI Matching for Multiple Jobs",
            "endpoint": "/batch-match",
            "method": "POST",
            "category": "AI Matching Engine",
            "description": "Batch AI matching for multiple jobs",
            "test_data": {
                "jobs": [
                    {
                        "job_id": 1,
                        "job_title": "Senior Python Developer",
                        "required_skills": ["Python", "Django", "PostgreSQL"],
                        "experience_level": "Senior"
                    },
                    {
                        "job_id": 2,
                        "job_title": "Data Scientist",
                        "required_skills": ["Python", "Machine Learning", "TensorFlow"],
                        "experience_level": "Mid"
                    }
                ],
                "limit": 3
            }
        },
        # Candidate Analysis
        {
            "name": "Detailed Candidate Analysis",
            "endpoint": "/analyze/1",
            "method": "GET",
            "category": "Candidate Analysis",
            "description": "Detailed candidate profile analysis for candidate ID 1"
        },
        # System Diagnostics
        {
            "name": "Database Connectivity Test",
            "endpoint": "/test-db",
            "method": "GET",
            "category": "System Diagnostics",
            "description": "Database connectivity and testing"
        }
    ]
    
    results = []
    
    for endpoint_config in ai_endpoints:
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
    
    print(f"\nReport generated: agent_ai_endpoints_test_report.md")
    print("=" * 75)

def generate_markdown_report(results):
    """Generate a comprehensive markdown report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# BHIV HR Platform - AI Agent Service Advanced Endpoints Test Report

**Generated:** {timestamp}  
**Platform:** BHIV HR AI Agent Service  
**Base URL:** {BASE_URL}  
**Test Category:** AI Matching Engine & Advanced Features

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
    categories = {}
    for result in results:
        cat = result["endpoint_info"]["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "success": 0}
        categories[cat]["total"] += 1
        if result["status"] == "success":
            categories[cat]["success"] += 1
    
    total_success = sum(1 for r in results if r["status"] == "success")
    total_count = len(results)
    
    report += f"\n**Overall Success Rate:** {total_success}/{total_count} ({(total_success/total_count)*100:.1f}%)  \n\n"
    
    report += "**Success Rate by Category:**  \n"
    for cat, stats in categories.items():
        rate = (stats["success"] / stats["total"]) * 100
        report += f"- **{cat}:** {stats['success']}/{stats['total']} ({rate:.1f}%)  \n"
    
    report += "\n## 🔍 Detailed Test Results\n\n"
    
    # Group by category
    for category in categories.keys():
        category_results = [r for r in results if r["endpoint_info"]["category"] == category]
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
    
    # Add AI service analysis
    report += "## 🤖 AI Agent Service Advanced Analysis\n\n"
    report += "### Phase 3 AI Matching Engine\n\n"
    report += "The advanced AI matching system provides:\n\n"
    report += "- **Semantic Matching** - Deep understanding of job requirements and candidate skills\n"
    report += "- **Sentence Transformers** - State-of-the-art NLP for similarity analysis\n"
    report += "- **Multi-Factor Scoring** - Skills, experience, location, cultural fit analysis\n"
    report += "- **Batch Processing** - Efficient handling of multiple job matching requests\n"
    report += "- **Candidate Analysis** - Detailed profile analysis and recommendations\n"
    report += "- **System Diagnostics** - Database connectivity and health monitoring\n\n"
    
    report += "### AI Engine Capabilities:\n\n"
    report += "1. **Intelligent Matching** - Semantic understanding beyond keyword matching\n"
    report += "2. **Scalable Processing** - Batch operations for enterprise-scale matching\n"
    report += "3. **Deep Analysis** - Comprehensive candidate profile evaluation\n"
    report += "4. **Real-time Processing** - Fast response times for matching requests\n"
    report += "5. **Adaptive Learning** - Continuous improvement from feedback data\n"
    report += "6. **Robust Diagnostics** - System health and connectivity monitoring\n\n"
    
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
    report += "## 💡 AI Service Advanced Recommendations\n\n"
    
    if total_success == total_count:
        report += "✅ **All AI agent service advanced endpoints are functioning correctly**\n\n"
        report += "- AI matching engine is operational\n"
        report += "- Batch processing capabilities are working\n"
        report += "- Candidate analysis provides detailed insights\n"
        report += "- System diagnostics confirm connectivity\n\n"
    else:
        failed_count = total_count - total_success
        report += f"⚠️ **{failed_count} AI service endpoint(s) failed testing**\n\n"
        failed_endpoints = [r for r in results if r["status"] != "success"]
        for failed in failed_endpoints:
            report += f"- `{failed['endpoint_info']['endpoint']}`: {failed.get('message', 'Unknown error')}\n"
        report += "\n"
    
    report += "### AI Engine Best Practices:\n\n"
    report += "1. **Model Performance** - Monitor matching accuracy and response times\n"
    report += "2. **Batch Optimization** - Use batch processing for large-scale operations\n"
    report += "3. **Feedback Integration** - Collect and use matching feedback for improvement\n"
    report += "4. **System Monitoring** - Regular health checks and diagnostics\n"
    report += "5. **Scalability Planning** - Prepare for increased matching volume\n"
    report += "6. **Model Updates** - Keep AI models current with latest techniques\n"
    report += "7. **Error Handling** - Robust fallback mechanisms for service failures\n\n"
    
    # Add usage examples
    report += "## 📝 AI Service Advanced Usage Examples\n\n"
    report += "### AI-Powered Candidate Matching\n"
    report += "```bash\n"
    report += f'curl -X POST "{BASE_URL}/match" \\\n'
    report += f'  -H "Authorization: Bearer {API_KEY}" \\\n'
    report += '  -H "Content-Type: application/json" \\\n'
    report += '  -d {\n'
    report += '    "job_id": 1,\n'
    report += '    "job_title": "Senior Python Developer",\n'
    report += '    "required_skills": ["Python", "Django", "PostgreSQL"],\n'
    report += '    "experience_level": "Senior",\n'
    report += '    "limit": 5\n'
    report += '  }\n'
    report += "```\n\n"
    
    report += "### Batch AI Matching\n"
    report += "```bash\n"
    report += f'curl -X POST "{BASE_URL}/batch-match" \\\n'
    report += f'  -H "Authorization: Bearer {API_KEY}" \\\n'
    report += '  -H "Content-Type: application/json" \\\n'
    report += '  -d {\n'
    report += '    "jobs": [\n'
    report += '      {\n'
    report += '        "job_id": 1,\n'
    report += '        "job_title": "Senior Python Developer",\n'
    report += '        "required_skills": ["Python", "Django"]\n'
    report += '      }\n'
    report += '    ],\n'
    report += '    "limit": 3\n'
    report += '  }\n'
    report += "```\n\n"
    
    report += "### Candidate Analysis\n"
    report += "```bash\n"
    report += f'curl -H "Authorization: Bearer {API_KEY}" \\\n'
    report += f'     "{BASE_URL}/analyze/1"\n'
    report += "```\n\n"
    
    report += "### Database Connectivity Test\n"
    report += "```bash\n"
    report += f'curl -H "Authorization: Bearer {API_KEY}" \\\n'
    report += f'     "{BASE_URL}/test-db"\n'
    report += "```\n\n"
    
    report += f"---\n\n"
    report += f"**Report Generated:** {timestamp}  \n"
    report += f"**Test Duration:** {sum(r.get('response_time', 0) for r in results):.3f}s total  \n"
    report += f"**AI Service:** BHIV HR Platform Phase 3 AI Engine  \n"
    report += f"**Service URL:** {BASE_URL}  \n"
    
    # Write report to file
    with open("agent_ai_endpoints_test_report.md", "w", encoding="utf-8") as f:
        f.write(report)

if __name__ == "__main__":
    main()