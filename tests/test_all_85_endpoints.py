#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Endpoint Testing
Tests all 85 endpoints (79 Gateway + 6 Agent) with 120s timeout
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class EndpointTester:
    def __init__(self):
        self.gateway_url = "https://bhiv-hr-gateway-ltg0.onrender.com"
        self.agent_url = "https://bhiv-hr-agent-nhgg.onrender.com"
        self.api_key = "<YOUR_API_KEY>"
        self.timeout = 120
        self.results = {}
        
    def get_headers(self, auth_required=True):
        """Get request headers"""
        headers = {"Content-Type": "application/json"}
        if auth_required:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def test_endpoint(self, service, method, endpoint, data=None, auth_required=True):
        """Test a single endpoint"""
        url = f"{self.gateway_url if service == 'Gateway' else self.agent_url}{endpoint}"
        headers = self.get_headers(auth_required)
        
        try:
            start_time = time.time()
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=self.timeout)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=self.timeout)
            else:
                response = requests.request(method, url, headers=headers, json=data, timeout=self.timeout)
            
            response_time = time.time() - start_time
            
            return {
                "status": "PASS" if response.status_code < 500 else "FAIL",
                "status_code": response.status_code,
                "response_time": round(response_time, 3),
                "response_size": len(response.content),
                "error": None
            }
            
        except requests.exceptions.Timeout:
            return {
                "status": "TIMEOUT",
                "status_code": None,
                "response_time": self.timeout,
                "response_size": 0,
                "error": "Request timeout after 120s"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "status_code": None,
                "response_time": 0,
                "response_size": 0,
                "error": str(e)
            }
    
    def test_all_endpoints(self):
        """Test all 85 endpoints"""
        print("BHIV HR Platform - Comprehensive Endpoint Testing")
        print("=" * 60)
        print(f"Testing 85 endpoints with {self.timeout}s timeout")
        print(f"Gateway URL: {self.gateway_url}")
        print(f"Agent URL: {self.agent_url}")
        print()
        
        # Gateway Endpoints (79)
        gateway_endpoints = [
            # Core API (3)
            ("GET", "/", None, False),
            ("GET", "/health", None, False),
            ("GET", "/test-candidates", None, True),
            
            # Monitoring (3)
            ("GET", "/metrics", None, False),
            ("GET", "/health/detailed", None, False),
            ("GET", "/metrics/dashboard", None, False),
            
            # Job Management (2)
            ("POST", "/v1/jobs", {"title": "Test Job", "department": "IT", "location": "Remote", "experience_level": "Mid", "requirements": "Python", "description": "Test"}, True),
            ("GET", "/v1/jobs", None, True),
            
            # Candidate Management (5)
            ("GET", "/v1/candidates", None, True),
            ("GET", "/v1/candidates/search", None, True),
            ("GET", "/v1/candidates/job/1", None, True),
            ("GET", "/v1/candidates/1", None, True),
            ("POST", "/v1/candidates/bulk", {"candidates": [{"name": "Test", "email": "test@test.com"}]}, True),
            
            # AI Matching (2)
            ("GET", "/v1/match/1/top", None, True),
            ("POST", "/v1/match/batch", {"job_ids": [1, 2]}, True),
            
            # Assessment & Workflow (6)
            ("POST", "/v1/feedback", {"candidate_id": 1, "job_id": 1, "integrity": 5, "honesty": 5, "discipline": 5, "hard_work": 5, "gratitude": 5}, True),
            ("GET", "/v1/feedback", None, True),
            ("GET", "/v1/interviews", None, True),
            ("POST", "/v1/interviews", {"candidate_id": 1, "job_id": 1, "interview_date": "2025-12-01T10:00:00"}, True),
            ("POST", "/v1/offers", {"candidate_id": 1, "job_id": 1, "salary": 50000, "start_date": "2025-12-01", "terms": "Standard"}, True),
            ("GET", "/v1/offers", None, True),
            
            # Analytics (3)
            ("GET", "/candidates/stats", None, True),
            ("GET", "/v1/database/schema", None, True),
            ("GET", "/v1/reports/job/1/export.csv", None, True),
            
            # Client Portal (2)
            ("POST", "/v1/client/register", {"client_id": "TEST001", "company_name": "Test Co", "contact_email": "test@test.com", "password": "Test123!"}, False),
            ("POST", "/v1/client/login", {"client_id": "<DEMO_USERNAME>", "password": "<DEMO_PASSWORD>"}, False),
            
            # Candidate Portal (5)
            ("POST", "/v1/candidate/register", {"name": "Test User", "email": "testuser@test.com", "password": "Test123!"}, False),
            ("POST", "/v1/candidate/login", {"email": "testuser@test.com", "password": "Test123!"}, False),
            ("PUT", "/v1/candidate/profile/1", {"name": "Updated Name"}, True),
            ("POST", "/v1/candidate/apply", {"candidate_id": 1, "job_id": 1}, True),
            ("GET", "/v1/candidate/applications/1", None, True),
            
            # Security Testing (12)
            ("GET", "/v1/security/rate-limit-status", None, True),
            ("GET", "/v1/security/blocked-ips", None, True),
            ("POST", "/v1/security/test-input-validation", {"input_data": "test"}, True),
            ("POST", "/v1/security/validate-email", {"email": "test@test.com"}, True),
            ("POST", "/v1/security/test-email-validation", {"email": "test@test.com"}, True),
            ("POST", "/v1/security/validate-phone", {"phone": "123-456-7890"}, True),
            ("POST", "/v1/security/test-phone-validation", {"phone": "123-456-7890"}, True),
            ("GET", "/v1/security/test-headers", None, True),
            ("GET", "/v1/security/security-headers-test", None, True),
            ("POST", "/v1/security/penetration-test", {"test_type": "xss", "payload": "test"}, True),
            ("GET", "/v1/security/test-auth", None, True),
            ("GET", "/v1/security/penetration-test-endpoints", None, True),
            
            # CSP Management (8)
            ("POST", "/v1/security/csp-report", {"violated_directive": "script-src", "blocked_uri": "test", "document_uri": "test"}, True),
            ("GET", "/v1/security/csp-violations", None, True),
            ("GET", "/v1/csp/policies", None, True),
            ("GET", "/v1/csp/violations", None, True),
            ("POST", "/v1/csp/report", {"violated_directive": "script-src", "blocked_uri": "test", "document_uri": "test"}, True),
            ("GET", "/v1/csp/test", None, True),
            ("GET", "/v1/security/csp-policies", None, True),
            ("POST", "/v1/security/test-csp-policy", {"policy": "default-src 'self'"}, True),
            
            # 2FA Authentication (16)
            ("POST", "/v1/auth/2fa/setup", {"user_id": "test"}, True),
            ("POST", "/v1/auth/2fa/verify", {"user_id": "test", "totp_code": "123456"}, True),
            ("POST", "/v1/auth/2fa/login", {"user_id": "test", "totp_code": "123456"}, True),
            ("GET", "/v1/auth/2fa/status/test", None, True),
            ("POST", "/v1/auth/2fa/disable", {"user_id": "test"}, True),
            ("POST", "/v1/auth/2fa/backup-codes", {"user_id": "test"}, True),
            ("POST", "/v1/auth/2fa/test-token", {"user_id": "test", "totp_code": "123456"}, True),
            ("GET", "/v1/auth/2fa/qr/test", None, True),
            ("POST", "/v1/2fa/setup", {"user_id": "test"}, True),
            ("POST", "/v1/2fa/verify-setup", {"user_id": "test", "totp_code": "123456"}, True),
            ("POST", "/v1/2fa/login-with-2fa", {"user_id": "test", "totp_code": "123456"}, True),
            ("GET", "/v1/2fa/status/test", None, True),
            ("POST", "/v1/2fa/disable", {"user_id": "test"}, True),
            ("POST", "/v1/2fa/regenerate-backup-codes", {"user_id": "test"}, True),
            ("GET", "/v1/2fa/test-token/test/123456", None, True),
            ("GET", "/v1/2fa/demo-setup", None, True),
            
            # Password Management (12)
            ("POST", "/v1/auth/password/validate", {"password": "Test123!"}, True),
            ("GET", "/v1/auth/password/generate", None, True),
            ("GET", "/v1/auth/password/policy", None, True),
            ("POST", "/v1/auth/password/change", {"old_password": "old", "new_password": "new"}, True),
            ("POST", "/v1/auth/password/strength", {"password": "Test123!"}, True),
            ("GET", "/v1/auth/password/security-tips", None, True),
            ("POST", "/v1/password/validate", {"password": "Test123!"}, True),
            ("GET", "/v1/password/generate", None, True),
            ("GET", "/v1/password/policy", None, True),
            ("POST", "/v1/password/change", {"old_password": "old", "new_password": "new"}, True),
            ("GET", "/v1/password/strength-test", None, True),
            ("GET", "/v1/password/security-tips", None, True)
        ]
        
        # Agent Endpoints (6)
        agent_endpoints = [
            ("GET", "/", None, False),
            ("GET", "/health", None, False),
            ("GET", "/test-db", None, True),
            ("POST", "/match", {"job_id": 1}, True),
            ("POST", "/batch-match", {"job_ids": [1, 2]}, True),
            ("GET", "/analyze/1", None, True)
        ]
        
        # Test Gateway endpoints
        print("Testing Gateway Service (79 endpoints)...")
        for i, (method, endpoint, data, auth) in enumerate(gateway_endpoints, 1):
            print(f"  [{i:2d}/79] {method:4s} {endpoint[:50]:<50}", end=" ")
            result = self.test_endpoint("Gateway", method, endpoint, data, auth)
            self.results[f"Gateway_{method}_{endpoint}"] = result
            
            status_color = "PASS" if result["status"] == "PASS" else result["status"]
            print(f"{status_color:8s} {result['response_time']:6.2f}s")
        
        print(f"\nTesting Agent Service (6 endpoints)...")
        for i, (method, endpoint, data, auth) in enumerate(agent_endpoints, 1):
            print(f"  [{i:2d}/6 ] {method:4s} {endpoint[:50]:<50}", end=" ")
            result = self.test_endpoint("Agent", method, endpoint, data, auth)
            self.results[f"Agent_{method}_{endpoint}"] = result
            
            status_color = "PASS" if result["status"] == "PASS" else result["status"]
            print(f"{status_color:8s} {result['response_time']:6.2f}s")
        
        # Generate summary
        self.generate_summary()
        
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r["status"] == "PASS")
        failed = sum(1 for r in self.results.values() if r["status"] == "FAIL")
        timeout = sum(1 for r in self.results.values() if r["status"] == "TIMEOUT")
        error = sum(1 for r in self.results.values() if r["status"] == "ERROR")
        
        print(f"Total Endpoints: {total}")
        print(f"PASSED: {passed} ({passed/total*100:.1f}%)")
        print(f"FAILED: {failed} ({failed/total*100:.1f}%)")
        print(f"TIMEOUT: {timeout} ({timeout/total*100:.1f}%)")
        print(f"ERROR: {error} ({error/total*100:.1f}%)")
        
        # Response time stats
        response_times = [r["response_time"] for r in self.results.values() if r["response_time"] > 0]
        if response_times:
            print(f"\nResponse Time Stats:")
            print(f"Average: {sum(response_times)/len(response_times):.2f}s")
            print(f"Min: {min(response_times):.2f}s")
            print(f"Max: {max(response_times):.2f}s")
        
        # Failed endpoints
        failed_endpoints = [(k, v) for k, v in self.results.items() if v["status"] != "PASS"]
        if failed_endpoints:
            print(f"\nFailed Endpoints ({len(failed_endpoints)}):")
            for endpoint, result in failed_endpoints:
                print(f"  {endpoint}: {result['status']} - {result.get('error', 'HTTP ' + str(result.get('status_code', 'N/A')))}")
        
        # Save detailed results
        report = {
            "test_timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "timeout": timeout,
                "error": error,
                "success_rate": f"{passed/total*100:.1f}%"
            },
            "results": self.results
        }
        
        with open("endpoint_test_results.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"\nDetailed results saved: endpoint_test_results.json")

def main():
    tester = EndpointTester()
    tester.test_all_endpoints()

if __name__ == "__main__":
    main()
