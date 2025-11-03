# BHIV HR Platform - Testing Suite

This directory contains comprehensive testing tools and reports for the BHIV HR Platform.

## 📁 Directory Structure

### `/api/` - API Endpoint Testing
Contains comprehensive test scripts for all API endpoints across the platform:

- **`test_2fa_endpoints.py`** - Two-Factor Authentication endpoints (16 endpoints)
- **`test_agent_ai_endpoints.py`** - AI Agent Service advanced features (4 endpoints)
- **`test_agent_service_endpoints.py`** - AI Agent Service core API (2 endpoints)
- **`test_analytics_client_endpoints.py`** - Analytics & Client Portal API (5 endpoints)
- **`test_assessment_workflow_endpoints.py`** - Assessment & Workflow endpoints (6 endpoints)
- **`test_candidate_portal_endpoints.py`** - Candidate Portal endpoints (5 endpoints)
- **`test_core_api_endpoints.py`** - Core API endpoints (3 endpoints)
- **`test_csp_endpoints.py`** - CSP Management endpoints (8 endpoints)
- **`test_main_endpoints.py`** - Main business endpoints (9 endpoints)
- **`test_monitoring_endpoints.py`** - Monitoring endpoints (3 endpoints)
- **`test_password_endpoints.py`** - Password Management endpoints (12 endpoints)
- **`test_security_endpoints.py`** - Security Testing endpoints (12 endpoints)
- **`comprehensive_endpoint_testing.py`** - Legacy comprehensive testing
- **`test_endpoints.py`** - Core endpoint tests

### `/integration/` - Integration Testing
- **`test_candidate_portal.py`** - Candidate portal integration tests
- **`test_client_portal.py`** - Client portal integration tests

### `/security/` - Security Testing
- **`test_security.py`** - Security validation tests

### `/reports/` - Test Reports
Contains detailed markdown reports for all endpoint testing:

- **`2fa_endpoints_test_report.md`** - 2FA testing results
- **`agent_ai_endpoints_test_report.md`** - AI Agent advanced features results
- **`agent_service_endpoints_test_report.md`** - AI Agent core API results
- **`analytics_client_endpoints_test_report.md`** - Analytics & Client Portal results
- **`assessment_workflow_endpoints_test_report.md`** - Assessment & Workflow results
- **`candidate_portal_endpoints_test_report.md`** - Candidate Portal results
- **`core_api_endpoints_test_report.md`** - Core API results
- **`csp_endpoints_test_report.md`** - CSP Management results
- **`main_endpoints_test_report.md`** - Main business endpoints results
- **`monitoring_endpoints_test_report.md`** - Monitoring endpoints results
- **`password_endpoints_test_report.md`** - Password Management results
- **`security_endpoints_test_report.md`** - Security Testing results

## 🚀 Running Tests

### Individual Endpoint Category Testing
```bash
# Test specific endpoint category
cd tests/api
python test_monitoring_endpoints.py
python test_security_endpoints.py
python test_2fa_endpoints.py
```

### Comprehensive Testing
```bash
# Run all endpoint tests
cd tests/api
python comprehensive_endpoint_testing.py

# Run integration tests
cd tests/integration
python test_client_portal.py
python test_candidate_portal.py
```

## 📊 Test Results Summary

**Total Endpoints Tested:** 83+
**Overall Success Rate:** 73%
**Categories Covered:** 12

### Success Rates by Category:
- **Monitoring:** 100% (3/3)
- **Core API:** 100% (3/3)
- **Analytics:** 100% (3/3)
- **Password Management:** 83% (10/12)
- **Candidate Portal:** 80% (4/5)
- **CSP Management:** 75% (6/8)
- **Security Testing:** 67% (8/12)
- **Assessment & Workflow:** 67% (4/6)
- **Main Business:** 89% (8/9)
- **2FA System:** 31% (5/16)
- **AI Agent Service:** 50% (2/4)

## 🔧 Issues Identified

### Critical Issues (Schema Validation - Status 422):
1. **2FA Endpoints** - 11/16 POST endpoints failing
2. **Client Portal** - Registration and login blocked
3. **Password Management** - Change password endpoints failing
4. **Assessment** - Feedback and offers creation failing

### Service Issues:
1. **AI Agent Direct Access** - Timeouts (works via gateway)
2. **Security Batch Testing** - Schema validation errors

## 📝 Usage Instructions

1. **Individual Testing**: Run specific test scripts for targeted endpoint validation
2. **Report Analysis**: Check `/reports/` for detailed test results and recommendations
3. **Issue Tracking**: Use reports to identify and prioritize fixes
4. **Performance Monitoring**: Track response times and success rates

## 🔗 Related Documentation

- **API Documentation**: `/docs/api/API_DOCUMENTATION.md`
- **Testing Strategy**: `/docs/testing/TESTING_STRATEGY.md`
- **Deployment Guide**: `/docs/deployment/RENDER_DEPLOYMENT_GUIDE.md`