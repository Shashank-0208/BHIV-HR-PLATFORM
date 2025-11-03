# BHIV HR Platform - Analytics & Client Portal Endpoints Test Report

**Generated:** 2025-11-03 14:12:11  
**Platform:** BHIV HR Gateway Service  
**Base URL:** https://bhiv-hr-gateway-ltg0.onrender.com  
**Test Category:** Analytics & Statistics + Client Portal API

## 📊 Test Summary

| Endpoint | Method | Category | Status | Response Time | Status Code |
|----------|--------|----------|--------|---------------|-------------|
| `/candidates/stats` | GET | Analytics | ✅ success | 1.238s | 200 |
| `/v1/database/schema` | GET | Analytics | ✅ success | 1.195s | 200 |
| `/v1/reports/job/1/export.csv` | GET | Analytics | ✅ success | 0.581s | 200 |
| `/v1/client/register` | POST | Client Portal | ❌ error | 0.585s | 422 |
| `/v1/client/login` | POST | Client Portal | ❌ error | 0.626s | 422 |

**Overall Success Rate:** 3/5 (60.0%)  
**Analytics Success Rate:** 3/3 (100.0%)  
**Client Portal Success Rate:** 0/2 (0.0%)  

## 🔍 Detailed Test Results

### Analytics & Statistics

#### Candidate Statistics

**Endpoint:** `GET /candidates/stats`  
**Description:** Get comprehensive candidate statistics and metrics  

**✅ Test Result:** PASSED  
**Status Code:** 200  
**Response Time:** 1.238s  
**Response Size:** 142 bytes  

**Response Structure:**
```json
{
  "total_candidates": 7,
  "active_jobs": 5,
  "recent_matches": 25,
  "pending_interviews": 8,
  "statistics_generated_at": "2025-11-03T08:42:10.370098+00:00"
}
```

#### Database Schema Info

**Endpoint:** `GET /v1/database/schema`  
**Description:** Retrieve database schema information and table details  

**✅ Test Result:** PASSED  
**Status Code:** 200  
**Response Time:** 1.195s  
**Response Size:** 590 bytes  

**Response Structure:**
```json
{
  "schema_version": "4.2.0",
  "applied_at": "2025-11-03T06:06:10.519385",
  "total_tables": 16,
  "tables": [
    "audit_logs",
    "candidates",
    "clients",
    "company_scoring_preferences",
    "csp_violations",
    "feedback",
    "interviews",
    "job_applications",
    "jobs",
    "matching_cache",
    "offers",
    "pg_stat_statements",
    "pg_stat_statements_info",
    "rate_limits",
    "schema_version",
    "users"
  ],
  "phase3_enabled": true,
  "core_tables": [
    "candidates",
    "jobs",
    "feedback",
    "interviews",
    "offers",
    "users",
    "clients",
    "matching_cache",
    "audit_logs",
    "rate_limits",
    "csp_violations",
    "company_scoring_preferences"
  ],
  "checked_at": "2025-11-03T08:42:11.551555+00:00"
}
```

#### Job Report Export

**Endpoint:** `GET /v1/reports/job/1/export.csv`  
**Description:** Export job report data in CSV format  

**✅ Test Result:** PASSED  
**Status Code:** 200  
**Response Time:** 0.581s  
**Response Size:** 152 bytes  

**Response Structure:**
```json
{
  "message": "Job report export",
  "job_id": 1,
  "format": "CSV",
  "download_url": "/downloads/job_1_report.csv",
  "generated_at": "2025-11-03T08:42:12.180360+00:00"
}
```

### Client Portal API

#### Client Register

**Endpoint:** `POST /v1/client/register`  
**Description:** Register a new client company  

**❌ Test Result:** FAILED  
**Error:** Unknown error  
**Status Code:** 422  
**Response Time:** 0.585s  

#### Client Login

**Endpoint:** `POST /v1/client/login`  
**Description:** Authenticate client and get access token  

**❌ Test Result:** FAILED  
**Error:** Unknown error  
**Status Code:** 422  
**Response Time:** 0.626s  

## 🏗️ Code Structure Analysis

### Analytics & Statistics Implementation

The analytics endpoints provide comprehensive data insights:

- **Candidate Statistics** - Aggregated metrics and performance data
- **Database Schema** - Real-time schema information and table details
- **Report Export** - CSV export functionality for job reports
- **Performance Metrics** - System and business intelligence

### Client Portal API Implementation

The client portal provides enterprise-grade authentication:

- **Client Registration** - Company onboarding with validation
- **JWT Authentication** - Secure token-based login system
- **Account Management** - Client profile and access control
- **Security Features** - Rate limiting and audit logging

## ⚡ Performance Analysis

**Average Response Time:** 1.005s  
**Fastest Endpoint:** `/v1/reports/job/1/export.csv` (0.581s)  
**Slowest Endpoint:** `/candidates/stats` (1.238s)  

## 💡 Recommendations

⚠️ **2 endpoint(s) failed testing**

- `/v1/client/register`: Unknown error
- `/v1/client/login`: Unknown error

### Next Steps:

1. **Analytics Integration** - Connect analytics to business dashboards
2. **Client Onboarding** - Streamline client registration process
3. **Performance Monitoring** - Track analytics query performance
4. **Security Audit** - Review client authentication security
5. **Export Enhancement** - Add more export formats (Excel, JSON)

## 📝 Usage Examples

### Get Candidate Statistics
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-ltg0.onrender.com/candidates/stats"
```

### Client Login
```bash
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login" \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d {
    "client_code": "TECH001",
    "password": "demo123"
  }
```

### Export Job Report
```bash
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     "https://bhiv-hr-gateway-ltg0.onrender.com/v1/reports/job/1/export.csv" > job_report.csv
```

---

**Report Generated:** 2025-11-03 14:12:11  
**Test Duration:** 4.225s total  
**Platform:** BHIV HR Platform v3.0.0-Phase3  
