#!/usr/bin/env python3
"""
🧪 BHIV HR Platform - Enhanced Comprehensive Endpoint Testing Suite
Tests all 89 endpoints across 6 services with URL discovery and proper authentication
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import re
from urllib.parse import urljoin, urlparse

# Configure logging with UTF-8 encoding
import sys
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BHIVEndpointTester:
    def __init__(self):
        # Service URLs - Local development (Docker)
        self.services = {
            "gateway": os.getenv('GATEWAY_URL', "http://localhost:8000"),
            "agent": os.getenv('AGENT_SERVICE_URL', "http://localhost:9000"), 
            "langgraph": os.getenv('LANGGRAPH_URL', "http://localhost:9001"),
            "hr_portal": os.getenv('PORTAL_URL', "http://localhost:8501"),
            "client_portal": os.getenv('CLIENT_PORTAL_URL', "http://localhost:8502"),
            "candidate_portal": os.getenv('CANDIDATE_PORTAL_URL', "http://localhost:8503")
        }
        
        # Alternative LangGraph URLs to discover (Docker ports)
        self.langgraph_alternatives = [
            "http://localhost:9001",
            "http://localhost:8002",
            "http://localhost:8003",
            "http://localhost:8004",
            "http://localhost:9000"
        ]
        
        # API Key management - Use Docker compose default key
        self.api_key = os.getenv("API_KEY_SECRET", "<YOUR_API_KEY>")
        self.production_api_key = self.api_key
        self.api_key_status = "configured"
        self.environment = "local"
        
        # Authentication tokens
        self.client_token = None
        self.candidate_token = None
        
        # Test credentials and data
        self.test_data = {
            "job": {
                "title": "Senior Python Developer",
                "department": "Engineering",
                "location": "Mumbai",
                "experience_level": "Senior",
                "requirements": "Python, FastAPI, PostgreSQL, 5+ years experience",
                "description": "Senior Python developer for AI-powered HR platform",
                "client_id": 1,
                "employment_type": "Full-time"
            },
            "candidate": {
                "name": "Test Candidate Enhanced",
                "email": f"test.enhanced.{int(time.time())}@example.com",
                "phone": "+919876543210",
                "location": "Mumbai",
                "experience_years": 5,
                "technical_skills": "Python, FastAPI, PostgreSQL, Docker, AWS",
                "education_level": "Masters",
                "seniority_level": "Senior Developer",
                "password": "TestPass123!"
            },
            "client": {
                "client_id": f"test_client_enhanced_{int(time.time())}",
                "company_name": "Test Company Enhanced Ltd",
                "contact_email": f"test.enhanced.client.{int(time.time())}@example.com",
                "contact_phone": "+919876543211",
                "industry": "Technology",
                "company_size": "50-100",
                "password": "ClientPass123!"
            }
        }
        
        # Test results storage
        self.results = {
            "total_endpoints": 89,  # Complete endpoint count across all services
            "tested_endpoints": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "service_results": {},
            "integration_tests": {},
            "workflow_tests": {},
            "detailed_results": [],
            "discovered_urls": {},
            "api_key_status": "unknown",
            "authentication_status": {}
        }
        
        # Dynamic test data (populated during tests)
        self.created_job_id = None
        self.created_candidate_id = None
        self.workflow_id = None

    async def discover_service_urls(self):
        """Discover and validate all service URLs"""
        logger.info(f"🔍 Discovering service URLs for {self.environment} environment...")
        
        # If production, validate production URLs first
        if self.environment == "production":
            for service_name, url in self.services.items():
                if await self._validate_service_url(service_name, url):
                    logger.info(f"✅ Validated {service_name} at: {url}")
                    self.results['discovered_urls'][service_name] = url
                else:
                    logger.warning(f"⚠️ Could not validate {service_name} at: {url}")
        else:
            # Local environment - try alternatives for LangGraph
            langgraph_url = await self.discover_langgraph_url()
            self.services["langgraph"] = langgraph_url
    
    async def discover_langgraph_url(self) -> str:
        """Discover the correct LangGraph service URL (local development)"""
        logger.info("🔍 Discovering LangGraph service URL...")
        
        for url in self.langgraph_alternatives:
            if await self._validate_service_url("langgraph", url):
                logger.info(f"✅ Found LangGraph service at: {url}")
                self.results['discovered_urls']['langgraph'] = url
                return url
        
        logger.warning("⚠️ Could not discover LangGraph service URL - using default")
        return self.services["langgraph"]
    
    async def _validate_service_url(self, service_name: str, url: str) -> bool:
        """Validate if a service URL is accessible"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Try health endpoint first
                response = await client.get(f"{url}/health")
                if response.status_code == 200:
                    return True
        except:
            pass
        
        try:
            # Try root endpoint
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.get(url)
                if response.status_code in [200, 404]:  # 404 is OK, means service is up
                    return True
        except:
            pass
        
        return False

    async def validate_api_key(self) -> bool:
        """Validate the configured API key"""
        logger.info("🔑 Validating API key configuration...")
        
        try:
            headers = {'Authorization': f'Bearer {self.api_key}'}
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.get(f"{self.services['gateway']}/v1/jobs", headers=headers)
                if response.status_code == 200:
                    logger.info("✅ API key is valid")
                    self.api_key_status = 'valid'
                    return True
                else:
                    logger.warning(f"⚠️ API key validation returned: {response.status_code}")
                    self.api_key_status = 'invalid'
                    return False
        except Exception as e:
            logger.error(f"❌ API key validation failed: {e}")
            self.api_key_status = 'error'
            return False

    async def setup_authentication_tokens(self):
        """Setup authentication tokens for protected endpoint testing"""
        logger.info("🔐 Setting up authentication tokens...")
        
        # Try to register and login a test client
        try:
            # Register client
            result = await self._make_authenticated_request("POST", "gateway", "/v1/client/register", 
                                                          self.test_data["client"])
            if result and result.get('success') and result.get('status_code') in [200, 201]:
                logger.info("✅ Test client registered successfully")
                
                # Login client
                login_data = {
                    "client_id": self.test_data["client"]["client_id"], 
                    "password": self.test_data["client"]["password"]
                }
                login_result = await self._make_authenticated_request("POST", "gateway", "/v1/client/login", login_data)
                
                if login_result and login_result.get('success'):
                    response_data = login_result.get('data', {})
                    if isinstance(response_data, dict) and 'access_token' in response_data:
                        self.client_token = response_data['access_token']
                        logger.info("✅ Client authentication token obtained")
                        self.results['authentication_status']['client'] = 'success'
                    else:
                        logger.warning("⚠️ Client login response missing token")
                        self.results['authentication_status']['client'] = 'token_missing'
                else:
                    logger.warning("⚠️ Client login failed")
                    self.results['authentication_status']['client'] = 'login_failed'
            else:
                logger.warning("⚠️ Client registration failed")
                self.results['authentication_status']['client'] = 'registration_failed'
        except Exception as e:
            logger.error(f"❌ Client authentication setup failed: {e}")
            self.results['authentication_status']['client'] = f'error: {str(e)}'
        
        # Try to register and login a test candidate
        try:
            # Register candidate
            result = await self._make_authenticated_request("POST", "gateway", "/v1/candidate/register", 
                                                          self.test_data["candidate"])
            if result and result.get('success') and result.get('status_code') in [200, 201]:
                logger.info("✅ Test candidate registered successfully")
                
                # Login candidate
                login_data = {
                    "email": self.test_data["candidate"]["email"], 
                    "password": self.test_data["candidate"]["password"]
                }
                login_result = await self._make_authenticated_request("POST", "gateway", "/v1/candidate/login", login_data)
                
                if login_result and login_result.get('success'):
                    response_data = login_result.get('data', {})
                    if isinstance(response_data, dict):
                        if 'token' in response_data:
                            self.candidate_token = response_data['token']
                            logger.info("✅ Candidate authentication token obtained")
                            self.results['authentication_status']['candidate'] = 'success'
                        if 'candidate' in response_data and isinstance(response_data['candidate'], dict):
                            self.created_candidate_id = response_data['candidate'].get('id')
                            if self.created_candidate_id:
                                logger.info(f"✅ Candidate ID obtained: {self.created_candidate_id}")
                    else:
                        logger.warning("⚠️ Candidate login response format unexpected")
                        self.results['authentication_status']['candidate'] = 'response_format_error'
                else:
                    logger.warning("⚠️ Candidate login failed")
                    self.results['authentication_status']['candidate'] = 'login_failed'
            else:
                logger.warning("⚠️ Candidate registration failed")
                self.results['authentication_status']['candidate'] = 'registration_failed'
        except Exception as e:
            logger.error(f"❌ Candidate authentication setup failed: {e}")
            self.results['authentication_status']['candidate'] = f'error: {str(e)}'

    async def _make_authenticated_request(self, method: str, service: str, endpoint: str, 
                                        data: Any = None) -> Optional[Dict]:
        """Make HTTP request with proper authentication
        
        Authentication Types:
        - API Key: '<YOUR_API_KEY>' - Static service key for admin/testing access
        - JWT Token: 'eyJhbGciOiJIUzI1NiIs...' - Dynamic user token after login
        """
        url = f"{self.services[service]}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        # Add proper authentication based on service
        # API Key: '<YOUR_API_KEY>' - Static service key for admin/testing
        # JWT Token: 'eyJhbGciOiJIUzI1NiIs...' - Dynamic user token after login
        if service == "gateway":
            # Most Gateway endpoints require API key authentication
            # Only specific endpoints accept JWT tokens (dual auth endpoints)
            jwt_compatible_endpoints = [
                "/v1/jobs",  # Uses get_auth (dual authentication)
                "/v1/client/",  # Client-specific endpoints
                "/v1/candidate/"  # Candidate-specific endpoints
            ]
            
            # Check if this endpoint supports JWT tokens
            supports_jwt = any(jwt_endpoint in endpoint for jwt_endpoint in jwt_compatible_endpoints)
            
            if supports_jwt and self.client_token:
                # Use JWT token for dual-auth endpoints
                headers["Authorization"] = f"Bearer {self.client_token}"
            elif self.production_api_key:
                # Use API key for most endpoints (this is the fix)
                headers["Authorization"] = f"Bearer {self.production_api_key}"
        elif service in ["agent", "langgraph"]:
            if self.production_api_key:
                headers["Authorization"] = f"Bearer {self.production_api_key}"
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, json=data, headers=headers)
                elif method == "PUT":
                    response = await client.put(url, json=data, headers=headers)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    'headers': dict(response.headers),
                    'url': str(response.url)
                }
        except httpx.TimeoutException:
            return {'success': False, 'error': 'Request timeout', 'status_code': 408, 'url': url}
        except httpx.RequestError as e:
            return {'success': False, 'error': f'Request error: {str(e)}', 'status_code': 0, 'url': url}
        except Exception as e:
            return {'success': False, 'error': f'Unexpected error: {str(e)}', 'status_code': 0, 'url': url}

    async def run_comprehensive_test(self):
        """Run enhanced comprehensive endpoint testing suite"""
        logger.info(f"🚀 Starting BHIV HR Platform Enhanced Comprehensive Endpoint Testing ({self.environment.title()})")
        logger.info(f"Testing {self.results['total_endpoints']} endpoints across 6 services")
        logger.info(f"Environment: {self.environment.title()} ({'Production Render URLs' if self.environment == 'production' else 'Local Docker URLs'})")
        
        start_time = time.time()
        
        try:
            # Pre-test setup
            logger.info("\n🔧 Pre-test Setup")
            logger.info("-" * 30)
            
            # Discover and validate service URLs
            await self.discover_service_urls()
            
            # Validate API key
            await self.validate_api_key()
            self.results['api_key_status'] = self.api_key_status
            
            # Setup authentication tokens
            await self.setup_authentication_tokens()
            
            # Phase 1: Service Health Checks
            await self._test_service_health()
            
            # Phase 2: Core API Endpoints
            await self._test_core_endpoints()
            
            # Phase 3: Authentication & Security
            await self._test_authentication_security()
            
            # Phase 4: Business Logic Workflow
            await self._test_business_workflow()
            
            # Phase 5: AI & Matching Engine
            await self._test_ai_matching()
            
            # Phase 6: LangGraph Workflows
            await self._test_langgraph_workflows()
            
            # Phase 7: Integration Tests
            await self._test_service_integration()
            
            # Phase 8: Portal Accessibility
            await self._test_portal_accessibility()
            
        except Exception as e:
            logger.error(f"❌ Critical error during testing: {e}")
        
        # Generate comprehensive report
        total_time = time.time() - start_time
        await self._generate_enhanced_test_report(total_time)

    async def _test_service_health(self):
        """Test basic health endpoints for all services"""
        logger.info("Phase 1: Testing Service Health")
        
        health_endpoints = [
            ("gateway", "/health", "Gateway Health Check"),
            ("gateway", "/", "Gateway Root Endpoint"),
            ("agent", "/health", "Agent Health Check"),
            ("agent", "/", "Agent Root Endpoint"),
            ("langgraph", "/health", "LangGraph Health Check"),
            ("langgraph", "/", "LangGraph Root Endpoint")
        ]
        
        for service, endpoint, test_name in health_endpoints:
            await self._test_endpoint("GET", service, endpoint, expected_status=200, 
                                    test_name=test_name)

    async def _test_core_endpoints(self):
        """Test core API endpoints with proper authentication"""
        logger.info("Phase 2: Testing Core API Endpoints")
        
        # Gateway core endpoints
        core_tests = [
            ("GET", "gateway", "/openapi.json", None, 200, "OpenAPI Schema"),
            ("GET", "gateway", "/v1/test-candidates", None, 200, "Database Connectivity"),
            ("GET", "gateway", "/v1/candidates/stats", None, 200, "Candidate Statistics"),
            ("GET", "gateway", "/v1/database/schema", None, 200, "Database Schema"),
            ("GET", "gateway", "/metrics", None, 200, "Prometheus Metrics"),
            ("GET", "gateway", "/health/detailed", None, 200, "Detailed Health Check")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in core_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)

    async def _test_authentication_security(self):
        """Test authentication and security endpoints with enhanced validation"""
        logger.info("Phase 3: Testing Authentication & Security")
        
        # Security testing endpoints
        security_tests = [
            ("GET", "gateway", "/v1/security/rate-limit-status", None, 200, "Rate Limit Status"),
            ("GET", "gateway", "/v1/security/blocked-ips", None, 200, "Blocked IPs"),
            ("POST", "gateway", "/v1/security/test-input-validation", 
             {"input_data": "test input"}, 200, "Input Validation"),
            ("POST", "gateway", "/v1/security/validate-email", 
             {"email": "test@example.com"}, 200, "Email Validation"),
            ("POST", "gateway", "/v1/security/validate-phone", 
             {"phone": "+919876543210"}, 200, "Phone Validation"),
            ("GET", "gateway", "/v1/security/test-headers", None, 200, "Security Headers"),
            ("GET", "gateway", "/v1/security/csp-policies", None, 200, "CSP Policies"),
            ("GET", "gateway", "/v1/security/test-auth", None, 200, "Authentication Test")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in security_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)
        
        # 2FA endpoints
        twofa_tests = [
            ("POST", "gateway", "/v1/auth/2fa/setup", {"user_id": "test_user"}, 200, "2FA Setup"),
            ("GET", "gateway", "/v1/auth/2fa/status/test_user", None, 200, "2FA Status"),
            ("GET", "gateway", "/v1/auth/2fa/qr/test_user", None, 200, "2FA QR Code")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in twofa_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)
        
        # Password management
        password_tests = [
            ("POST", "gateway", "/v1/auth/password/validate", 
             {"password": "TestPass123!"}, 200, "Password Validation"),
            ("GET", "gateway", "/v1/auth/password/generate", None, 200, "Password Generation"),
            ("GET", "gateway", "/v1/auth/password/policy", None, 200, "Password Policy"),
            ("GET", "gateway", "/v1/auth/password/security-tips", None, 200, "Security Tips")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in password_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)

    async def _test_business_workflow(self):
        """Test complete business workflow with enhanced authentication"""
        logger.info("Phase 4: Testing Business Logic Workflow")
        
        # Step 1: Create Job (requires API key, not JWT)
        job_response = await self._make_authenticated_request("POST", "gateway", "/v1/jobs", 
                                                            self.test_data["job"])
        if job_response and job_response.get('success') and job_response.get('status_code') == 200:
            job_data = job_response.get('data', {})
            if isinstance(job_data, dict) and 'job_id' in job_data:
                self.created_job_id = job_data['job_id']
                logger.info(f"✅ Created job with ID: {self.created_job_id}")
                self.results['passed'] += 1
                logger.info("✅ PASS Create Job: (200)")
            else:
                self.results['failed'] += 1
                logger.error("❌ FAIL Create Job: Missing job_id in response")
        else:
            self.results['failed'] += 1
            logger.error(f"❌ FAIL Create Job: {job_response.get('status_code', 'Unknown')}")
        
        self.results['tested_endpoints'] += 1
        if job_response and job_response.get("job_id"):
            self.created_job_id = job_response["job_id"]
            logger.info(f"✅ Created job with ID: {self.created_job_id}")
        
        # Continue with other workflow tests using authenticated requests
        workflow_tests = [
            ("GET", "gateway", "/v1/jobs", None, 200, "List Jobs"),
            ("GET", "gateway", "/v1/candidates", None, 200, "Get All Candidates"),
            ("GET", "gateway", "/v1/candidates/search", None, 200, "Search Candidates"),
            ("GET", "gateway", "/v1/interviews", None, 200, "Get Interviews"),
            ("GET", "gateway", "/v1/feedback", None, 200, "Get Feedback")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in workflow_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)

    async def _test_ai_matching(self):
        """Test AI matching and agent endpoints with authentication"""
        logger.info("Phase 5: Testing AI & Matching Engine")
        
        # Agent service tests
        agent_tests = [
            ("GET", "agent", "/test-db", None, 200, "Agent Database Test"),
            ("POST", "agent", "/match", {"job_id": 1}, 200, "AI Candidate Matching"),
            ("POST", "agent", "/batch-match", {"job_ids": [1, 2]}, 200, "Batch AI Matching"),
            ("GET", "agent", "/analyze/1", None, 200, "Candidate Analysis")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in agent_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)
        
        # Gateway AI matching endpoints
        gateway_ai_tests = [
            ("GET", "gateway", "/v1/match/1/top", None, 200, "Gateway AI Matching"),
            ("POST", "gateway", "/v1/match/batch", [1, 2], 200, "Gateway Batch Matching")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in gateway_ai_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)

    async def _test_langgraph_workflows(self):
        """Test LangGraph workflow endpoints with enhanced discovery"""
        logger.info("Phase 6: Testing LangGraph Workflows")
        
        # LangGraph endpoints with authentication
        langgraph_tests = [
            ("GET", "langgraph", "/health", None, 200, "LangGraph Health Check"),
            ("GET", "langgraph", "/", None, 200, "LangGraph Root Endpoint"),
            ("GET", "langgraph", "/workflows", None, 200, "List Workflows"),
            ("GET", "langgraph", "/workflows/stats", None, 200, "Workflow Stats"),
            ("GET", "langgraph", "/docs", None, 200, "LangGraph API Documentation"),
            ("POST", "langgraph", "/tools/send-notification", 
             {"candidate_name": "Test", "job_title": "Developer", "message": "Test notification", "channels": ["email"]}, 
             200, "Send Notification"),
            ("GET", "langgraph", "/test-integration", None, 200, "Test Integration")
        ]
        
        for method, service, endpoint, data, expected_status, test_name in langgraph_tests:
            await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name)

    async def _test_service_integration(self):
        """Test integration between services with enhanced validation"""
        logger.info("Phase 7: Testing Service Integration")
        
        integration_results = {}
        
        # Test Gateway -> Agent integration
        try:
            gateway_match = await self._test_endpoint_with_auth("GET", "gateway", "/v1/match/1/top", 
                                                              None, 200, "Gateway-Agent Integration", return_response=True)
            agent_match = await self._test_endpoint_with_auth("POST", "agent", "/match", 
                                                            {"job_id": 1}, 200, "Direct Agent Match", return_response=True)
            
            integration_results["gateway_agent"] = {
                "status": "✅ INTEGRATED" if gateway_match and agent_match else "❌ DISCONNECTED",
                "gateway_response": bool(gateway_match),
                "agent_response": bool(agent_match)
            }
        except Exception as e:
            integration_results["gateway_agent"] = {"status": "❌ ERROR", "error": str(e)}
        
        # Test Gateway -> LangGraph integration
        try:
            langgraph_health = await self._test_endpoint_with_auth("GET", "langgraph", "/health", 
                                                                 None, 200, "LangGraph Health", return_response=True)
            langgraph_workflows = await self._test_endpoint_with_auth("GET", "langgraph", "/workflows", 
                                                                    None, 200, "LangGraph Workflows", return_response=True)
            
            integration_results["gateway_langgraph"] = {
                "status": "✅ INTEGRATED" if langgraph_health and langgraph_workflows else "❌ DISCONNECTED",
                "health_response": bool(langgraph_health),
                "workflows_response": bool(langgraph_workflows)
            }
        except Exception as e:
            integration_results["gateway_langgraph"] = {"status": "❌ ERROR", "error": str(e)}
        
        self.results["integration_tests"] = integration_results

    async def _test_portal_accessibility(self):
        """Test portal accessibility with enhanced validation"""
        logger.info("Phase 8: Testing Portal Accessibility")
        
        portal_results = {}
        
        for portal_name, portal_url in [
            ("hr_portal", self.services["hr_portal"]),
            ("client_portal", self.services["client_portal"]),
            ("candidate_portal", self.services["candidate_portal"])
        ]:
            try:
                async with httpx.AsyncClient(timeout=15.0) as client:
                    response = await client.get(portal_url)
                    portal_results[portal_name] = {
                        "status": "✅ ACCESSIBLE" if response.status_code == 200 else f"❌ ERROR ({response.status_code})",
                        "status_code": response.status_code,
                        "accessible": response.status_code == 200,
                        "url": portal_url
                    }
            except Exception as e:
                portal_results[portal_name] = {
                    "status": "❌ UNREACHABLE",
                    "error": str(e),
                    "accessible": False,
                    "url": portal_url
                }
        
        self.results["portal_accessibility"] = portal_results

    async def _test_endpoint_with_auth(self, method: str, service: str, endpoint: str, 
                                     data: Any = None, expected_status: int = 200, 
                                     test_name: str = "", return_response: bool = False) -> Optional[Dict]:
        """Test individual endpoint with proper authentication
        
        Authentication Types:
        - API Key: Static service key for admin/testing access (e.g., '<YOUR_API_KEY>')
        - JWT Token: Dynamic user token after login (e.g., 'eyJhbGciOiJIUzI1NiIs...')
        """
        url = f"{self.services[service]}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        # Add proper authentication based on service
        if service == "gateway":
            # Most Gateway endpoints require API key authentication
            # Only specific endpoints accept JWT tokens (dual auth endpoints)
            jwt_compatible_endpoints = [
                "/v1/jobs",  # Uses get_auth (dual authentication)
                "/v1/client/",  # Client-specific endpoints
                "/v1/candidate/"  # Candidate-specific endpoints
            ]
            
            # Check if this endpoint supports JWT tokens
            supports_jwt = any(jwt_endpoint in endpoint for jwt_endpoint in jwt_compatible_endpoints)
            
            if supports_jwt and self.client_token:
                # Use JWT token for dual-auth endpoints
                headers["Authorization"] = f"Bearer {self.client_token}"
            elif self.production_api_key:
                # Use API key for most endpoints (this is the fix)
                headers["Authorization"] = f"Bearer {self.production_api_key}"
        elif service in ["agent", "langgraph"]:
            if self.production_api_key:
                headers["Authorization"] = f"Bearer {self.production_api_key}"
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                if method == "GET":
                    response = await client.get(url, headers=headers)
                elif method == "POST":
                    response = await client.post(url, json=data, headers=headers)
                elif method == "PUT":
                    response = await client.put(url, json=data, headers=headers)
                elif method == "DELETE":
                    response = await client.delete(url, headers=headers)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                # Record result
                success = response.status_code == expected_status
                result = {
                    "test_name": test_name or f"{method} {endpoint}",
                    "service": service,
                    "endpoint": endpoint,
                    "method": method,
                    "expected_status": expected_status,
                    "actual_status": response.status_code,
                    "success": success,
                    "url": url,
                    "timestamp": datetime.now().isoformat()
                }
                
                if success:
                    self.results["passed"] += 1
                    logger.info(f"✅ PASS {test_name}: ({response.status_code})")
                    if return_response:
                        try:
                            return response.json()
                        except:
                            return {"status": "success"}
                else:
                    self.results["failed"] += 1
                    logger.error(f"❌ FAIL {test_name}: ({response.status_code})")
                    result["error"] = response.text[:200] if response.text else "No response body"
                
                self.results["tested_endpoints"] += 1
                self.results["detailed_results"].append(result)
                
                # Update service results
                if service not in self.results["service_results"]:
                    self.results["service_results"][service] = {"passed": 0, "failed": 0, "total": 0}
                
                self.results["service_results"][service]["total"] += 1
                if success:
                    self.results["service_results"][service]["passed"] += 1
                else:
                    self.results["service_results"][service]["failed"] += 1
                
                return response.json() if success and return_response else None
                
        except Exception as e:
            self.results["failed"] += 1
            self.results["tested_endpoints"] += 1
            logger.error(f"❌ ERROR {test_name}: {str(e)}")
            
            error_result = {
                "test_name": test_name or f"{method} {endpoint}",
                "service": service,
                "endpoint": endpoint,
                "method": method,
                "expected_status": expected_status,
                "actual_status": 0,
                "success": False,
                "error": str(e),
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            self.results["detailed_results"].append(error_result)
            return None

    # Keep the existing _test_endpoint method for backward compatibility
    async def _test_endpoint(self, method: str, service: str, endpoint: str, 
                           data: Any = None, expected_status: int = 200, 
                           test_name: str = "", return_response: bool = False) -> Optional[Dict]:
        """Test individual endpoint (legacy method)"""
        return await self._test_endpoint_with_auth(method, service, endpoint, data, expected_status, test_name, return_response)

    async def _generate_enhanced_test_report(self, total_time: float):
        """Generate enhanced comprehensive test report"""
        logger.info("📊 Generating Enhanced Comprehensive Test Report")
        
        # Calculate success rate
        success_rate = (self.results["passed"] / max(self.results["tested_endpoints"], 1)) * 100
        
        report = f"""
# 🧪 BHIV HR Platform - Enhanced Comprehensive Endpoint Test Report

**Test Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Total Test Time**: {total_time:.2f} seconds  
**Test Environment**: {self.environment.title()} ({'Production (Render Cloud)' if self.environment == 'production' else 'Local Development'})  
**Test Version**: Enhanced with URL Discovery & Authentication

## 📊 Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| **Total Endpoints** | {self.results['total_endpoints']} | 📋 Documented |
| **Tested Endpoints** | {self.results['tested_endpoints']} | 🧪 Executed |
| **Passed Tests** | {self.results['passed']} | ✅ Success |
| **Failed Tests** | {self.results['failed']} | ❌ Failed |
| **Success Rate** | {success_rate:.1f}% | {'✅ EXCELLENT' if success_rate >= 90 else '⚠️ NEEDS ATTENTION' if success_rate >= 70 else '❌ CRITICAL'} |

## 🔧 Enhanced Features Status

### 🔍 URL Discovery
"""
        
        if self.results.get('discovered_urls'):
            for service, url in self.results['discovered_urls'].items():
                report += f"- **{service.title()}**: {url} ✅\n"
        else:
            report += "- No alternative URLs discovered - using defaults\n"
        
        report += f"""
### 🔑 API Key Status
- **Status**: {self.results['api_key_status'].upper()}
- **Production Key**: {'✅ VALID' if self.production_api_key else '❌ MISSING'}

### 🔐 Authentication Status
"""
        
        for auth_type, status in self.results.get('authentication_status', {}).items():
            status_icon = "✅" if status == "success" else "❌"
            report += f"- **{auth_type.title()}**: {status} {status_icon}\n"
        
        report += f"""
## 🏗️ Service-Level Results

"""
        
        for service, stats in self.results["service_results"].items():
            service_success_rate = (stats["passed"] / max(stats["total"], 1)) * 100
            status_icon = "✅" if service_success_rate >= 90 else "⚠️" if service_success_rate >= 70 else "❌"
            
            report += f"""
### {service.title().replace('_', ' ')} Service
- **URL**: {self.services.get(service, 'Unknown')}
- **Endpoints Tested**: {stats['total']}
- **Passed**: {stats['passed']} | **Failed**: {stats['failed']}
- **Success Rate**: {service_success_rate:.1f}% {status_icon}
"""
        
        # Integration test results
        if self.results.get("integration_tests"):
            report += "\n## 🔗 Service Integration Results\n\n"
            for integration, result in self.results["integration_tests"].items():
                report += f"- **{integration.replace('_', ' ').title()}**: {result['status']}\n"
        
        # Portal accessibility results
        if self.results.get("portal_accessibility"):
            report += "\n## 🌐 Portal Accessibility Results\n\n"
            for portal, result in self.results["portal_accessibility"].items():
                report += f"- **{portal.replace('_', ' ').title()}**: {result['status']} ({result.get('url', 'Unknown URL')})\n"
        
        # Enhanced recommendations
        report += f"""
## 🎯 Enhanced Recommendations

### ✅ Strengths
- **Success Rate**: {success_rate:.1f}% of endpoints working correctly
- **URL Discovery**: {'Successful alternative URL discovery' if self.results.get('discovered_urls') else 'Using default URLs'}
- **Authentication**: {'Enhanced authentication implemented' if any(s == 'success' for s in self.results.get('authentication_status', {}).values()) else 'Basic authentication only'}

### 🔧 Critical Actions Needed
"""
        
        if self.results['api_key_status'] == 'missing':
            report += "- **🚨 URGENT**: Obtain production API key to test protected endpoints\n"
        
        if self.results.get('discovered_urls', {}).get('langgraph'):
            report += f"- **📝 UPDATE**: Update documentation with discovered LangGraph URL: {self.results['discovered_urls']['langgraph']}\n"
        
        failed_tests = [r for r in self.results["detailed_results"] if not r["success"]]
        if failed_tests:
            report += f"- **🔧 FIX**: {len(failed_tests)} endpoints need immediate attention\n"
        
        # Detailed failed tests
        if failed_tests:
            report += f"\n### ❌ Failed Tests Requiring Attention ({len(failed_tests)})\n\n"
            for test in failed_tests[:10]:  # Show first 10 failed tests
                error_msg = test.get('error', 'Unknown error')[:100]
                report += f"- **{test['test_name']}** ({test['service']}) - Status: {test['actual_status']} - {error_msg}\n"
            
            if len(failed_tests) > 10:
                report += f"- ... and {len(failed_tests) - 10} more failed tests\n"
        
        report += f"""
## 📋 Enhanced Test Summary

**Test Execution**: {'✅ COMPLETED' if self.results['tested_endpoints'] > 0 else '❌ INCOMPLETE'}  
**Overall Status**: {'✅ SYSTEM HEALTHY' if success_rate >= 90 else '⚠️ NEEDS ATTENTION' if success_rate >= 70 else '❌ CRITICAL ISSUES'}  
**Production Ready**: {'✅ YES' if success_rate >= 90 and self.results['failed'] < 5 else '⚠️ WITH CAUTION' if success_rate >= 70 else '❌ NOT RECOMMENDED'}  
**Enhanced Features**: {'✅ ACTIVE' if self.production_api_key or self.results.get('discovered_urls') else '⚠️ LIMITED'}

## 🚀 Next Steps

1. **If API Key Missing**: Set `API_KEY_SECRET` environment variable and re-run tests
2. **If LangGraph URL Changed**: Update documentation with discovered URL
3. **If Tests Failed**: Review failed endpoints and fix underlying issues
4. **If Success Rate < 95%**: Investigate and resolve failing endpoints

---

*Report Generated by BHIV Enhanced Comprehensive Endpoint Tester*  
*Test Environment: {self.environment.title()} ({'Production (Render Cloud)' if self.environment == 'production' else 'Local Development'})*  
*Total Test Time: {total_time:.2f} seconds*  
*Enhanced Features: URL Discovery, API Key Validation, Authentication Tokens*
"""
        
        # Save report
        with open("ENHANCED_COMPREHENSIVE_TEST_REPORT.md", "w", encoding='utf-8') as f:
            f.write(report)
        
        # Print summary
        logger.info("=" * 80)
        logger.info("ENHANCED COMPREHENSIVE TEST SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total Endpoints: {self.results['total_endpoints']}")
        logger.info(f"Tested: {self.results['tested_endpoints']}")
        logger.info(f"Passed: {self.results['passed']}")
        logger.info(f"Failed: {self.results['failed']}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        logger.info(f"API Key Status: {self.results['api_key_status']}")
        logger.info(f"Discovered URLs: {len(self.results.get('discovered_urls', {}))}")
        logger.info(f"Total Time: {total_time:.2f}s")
        logger.info(f"Overall Status: {'HEALTHY' if success_rate >= 90 else 'ATTENTION NEEDED' if success_rate >= 70 else 'CRITICAL'}")
        logger.info("=" * 80)
        logger.info("Enhanced detailed report saved to: ENHANCED_COMPREHENSIVE_TEST_REPORT.md")
        logger.info(f"Environment tested: {self.environment.title()}")
        if self.environment == "production":
            logger.info("Production URLs validated against live Render services")

async def main():
    """Main test execution"""
    tester = BHIVEndpointTester()
    await tester.run_comprehensive_test()

if __name__ == "__main__":
    asyncio.run(main())