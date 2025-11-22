# 📚 BHIV HR Platform - Complete API Documentation

**Updated**: November 21, 2025  
**API Version**: v4.2.0  
**Total Endpoints**: 89 (74 Gateway + 6 Agent + 9 LangGraph)  
**Status**: ✅ All Endpoints Operational (99.9% Uptime)

---

## 🌐 API Overview

### **Base URLs**
- **Production Gateway**: https://bhiv-hr-gateway-ltg0.onrender.com
- **Production Agent**: https://bhiv-hr-agent-nhgg.onrender.com
- **Production LangGraph**: https://bhiv-hr-langgraph.onrender.com
- **Local Gateway**: http://localhost:8000
- **Local Agent**: http://localhost:9000
- **Local LangGraph**: http://localhost:9001

### **Authentication Types**

#### **1. API Key Authentication (Primary)**
```bash
Authorization: Bearer <YOUR_API_KEY>
```
**Required for**: All Gateway endpoints, Agent endpoints, LangGraph endpoints  
**Demo API Key**: `bhiv_demo_api_key_2025`

#### **2. Client JWT Authentication**
```bash
Authorization: Bearer <client_jwt_token>
```
**Required for**: Client portal operations, job management  
**Demo Credentials**: `client_id: TECH001`, `password: demo123`

#### **3. Candidate JWT Authentication**
```bash
Authorization: Bearer <candidate_jwt_token>
```
**Required for**: Candidate profile operations, job applications  
**Demo Credentials**: `email: demo@candidate.com`, `password: demo123`

### **Authentication Flow**

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant A as Agent
    
    C->>G: POST /v1/client/login {client_id, password}
    G-->>C: JWT Token + Permissions
    C->>G: API Request with Bearer JWT
    G->>A: Forward with API Key
    A-->>G: AI Response
    G-->>C: Final Response
```

### **Common Authentication Issues**

| Error | Status | Solution | Example |
|-------|--------|----------|----------|
| `Not authenticated` | 403 | Use Bearer token format | `Authorization: Bearer <token>` |
| `Invalid API key` | 401 | Check API key value | Use `bhiv_demo_api_key_2025` |
| `Authentication required` | 401 | Include Authorization header | Add `-H "Authorization: Bearer <token>"` |
| `Token expired` | 401 | Refresh JWT token | Re-login to get new token |
| `Insufficient permissions` | 403 | Check user role/permissions | Verify client/candidate access |

### **Standard Response Format**
```json
{
  "status": "success|error",
  "data": {...},
  "message": "Human readable message",
  "timestamp": "2025-11-21T10:30:00Z",
  "request_id": "req_12345",
  "version": "v4.2.0"
}
```

### **Error Response Format**
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": "Email format is invalid",
    "field": "email"
  },
  "timestamp": "2025-11-21T10:30:00Z",
  "request_id": "req_12345"
}
```

---

## 🚀 Gateway Service API (74 Endpoints)

**Base URL**: https://bhiv-hr-gateway-ltg0.onrender.com  
**Authentication**: API Key (Bearer Token)  
**Rate Limit**: 60-500 requests/minute (dynamic)  
**Response Format**: JSON

### **Core API Endpoints (3)**

#### **GET /** - Service Information
**Description**: Get basic service information and available endpoints  
**Authentication**: None required  
**Rate Limit**: 100 requests/minute

```bash
curl -X GET https://bhiv-hr-gateway-ltg0.onrender.com/
```

**Response Schema**:
```json
{
  "message": "string",
  "version": "string",
  "status": "string",
  "endpoints": "integer",
  "documentation": "string",
  "monitoring": "string",
  "live_demo": "string"
}
```

**Example Response**:
```json
{
  "message": "BHIV HR Platform API Gateway",
  "version": "4.2.0",
  "status": "healthy",
  "endpoints": 74,
  "documentation": "/docs",
  "monitoring": "/metrics",
  "live_demo": "https://bhiv-hr-portal-u670.onrender.com"
}
```

#### **GET /health** - Health Check
**Description**: Basic health check endpoint for monitoring  
**Authentication**: None required  
**Rate Limit**: 200 requests/minute

```bash
curl -X GET https://bhiv-hr-gateway-ltg0.onrender.com/health
```

**Response Schema**:
```json
{
  "status": "healthy|unhealthy",
  "service": "string",
  "version": "string",
  "timestamp": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "status": "healthy",
  "service": "BHIV HR Gateway",
  "version": "4.2.0",
  "timestamp": "2025-11-21T10:30:00Z"
}
```

#### **GET /test-candidates** - Database Connectivity Test
**Description**: Test database connection and return sample data  
**Authentication**: API Key required  
**Rate Limit**: 30 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/test-candidates
```

**Headers**:
- `Authorization`: Bearer token (required)

**Response Schema**:
```json
{
  "database_status": "connected|disconnected",
  "total_candidates": "integer",
  "test_timestamp": "string (ISO 8601)",
  "sample_data": "array"
}
```

**Example Response**:
```json
{
  "database_status": "connected",
  "total_candidates": 10,
  "test_timestamp": "2025-11-21T10:30:00Z",
  "sample_data": [
    {"id": 1, "name": "John Smith"},
    {"id": 2, "name": "Jane Doe"}
  ]
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid API key
- `500 Internal Server Error`: Database connection failed

---

### **Monitoring Endpoints (3)**

#### **GET /metrics** - Prometheus Metrics
**Description**: Get system metrics in Prometheus format for monitoring  
**Authentication**: None required  
**Rate Limit**: 50 requests/minute  
**Content-Type**: text/plain

```bash
curl -X GET https://bhiv-hr-gateway-ltg0.onrender.com/metrics
```

**Response Format**: Prometheus metrics format
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/v1/candidates"} 1234
http_requests_total{method="POST",endpoint="/v1/jobs"} 567

# HELP response_time_seconds Response time in seconds
# TYPE response_time_seconds histogram
response_time_seconds_bucket{le="0.1"} 890
response_time_seconds_bucket{le="0.5"} 1200
```

#### **GET /health/detailed** - Detailed Health Check
**Description**: Comprehensive health check with service dependencies  
**Authentication**: API Key required  
**Rate Limit**: 20 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/health/detailed
```

**Headers**:
- `Authorization`: Bearer token (required)

**Response Schema**:
```json
{
  "status": "healthy|degraded|unhealthy",
  "services": {
    "database": "connected|disconnected",
    "ai_engine": "operational|down",
    "authentication": "active|inactive"
  },
  "performance": {
    "response_time": "string",
    "memory_usage": "string",
    "cpu_usage": "string",
    "uptime": "string"
  },
  "timestamp": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "status": "healthy",
  "services": {
    "database": "connected",
    "ai_engine": "operational",
    "authentication": "active"
  },
  "performance": {
    "response_time": "45ms",
    "memory_usage": "312MB",
    "cpu_usage": "23%",
    "uptime": "72h 15m"
  },
  "timestamp": "2025-11-21T10:30:00Z"
}
```

#### **GET /metrics/dashboard** - Metrics Dashboard
**Description**: Get formatted metrics for dashboard display  
**Authentication**: API Key required  
**Rate Limit**: 30 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/metrics/dashboard
```

**Response Schema**:
```json
{
  "system_metrics": {
    "total_requests": "integer",
    "active_users": "integer",
    "avg_response_time": "number",
    "error_rate": "number"
  },
  "business_metrics": {
    "total_candidates": "integer",
    "active_jobs": "integer",
    "matches_today": "integer",
    "applications_today": "integer"
  },
  "timestamp": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "system_metrics": {
    "total_requests": 15420,
    "active_users": 45,
    "avg_response_time": 0.087,
    "error_rate": 0.02
  },
  "business_metrics": {
    "total_candidates": 10,
    "active_jobs": 19,
    "matches_today": 156,
    "applications_today": 23
  },
  "timestamp": "2025-11-21T10:30:00Z"
}
```

---

### **Analytics Endpoints (3)**

#### **GET /v1/candidates/stats** - Candidate Statistics
**Description**: Get comprehensive candidate and job statistics  
**Authentication**: API Key required  
**Rate Limit**: 40 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/stats
```

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `period` (optional): `day|week|month|year` - Statistics period (default: `month`)
- `department` (optional): Filter by department

**Response Schema**:
```json
{
  "total_candidates": "integer",
  "active_jobs": "integer",
  "recent_matches": "integer",
  "pending_interviews": "integer",
  "applications_today": "integer",
  "hired_this_month": "integer",
  "statistics_generated_at": "string (ISO 8601)",
  "period": "string"
}
```

**Example Response**:
```json
{
  "total_candidates": 10,
  "active_jobs": 19,
  "recent_matches": 156,
  "pending_interviews": 8,
  "applications_today": 23,
  "hired_this_month": 5,
  "statistics_generated_at": "2025-11-21T10:30:00Z",
  "period": "month"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid API key
- `422 Unprocessable Entity`: Invalid period parameter

#### **GET /v1/database/schema** - Database Schema Verification
**Description**: Get current database schema information and table structure  
**Authentication**: API Key required  
**Rate Limit**: 10 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/schema
```

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `detailed` (optional): `true|false` - Include table details (default: `false`)

**Response Schema**:
```json
{
  "schema_version": "string",
  "total_tables": "integer",
  "tables": "array of strings",
  "phase3_enabled": "boolean",
  "indexes_count": "integer",
  "checked_at": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "schema_version": "4.2.0",
  "total_tables": 13,
  "tables": [
    "candidates", "jobs", "feedback", "interviews", "offers", 
    "users", "clients", "audit_logs", "rate_limits", 
    "csp_violations", "matching_cache", "company_scoring_preferences", 
    "job_applications"
  ],
  "phase3_enabled": true,
  "indexes_count": 75,
  "checked_at": "2025-11-21T10:30:00Z"
}
```

#### **GET /v1/reports/job/{job_id}/export.csv** - Job Report Export
**Description**: Export job candidates and statistics as CSV file  
**Authentication**: API Key required  
**Rate Limit**: 5 requests/minute  
**Content-Type**: text/csv

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/reports/job/1/export.csv
```

**Path Parameters**:
- `job_id` (required): Job ID to export (integer)

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `include_scores` (optional): `true|false` - Include AI matching scores (default: `true`)
- `format` (optional): `csv|xlsx` - Export format (default: `csv`)

**Response**: CSV file with headers:
```csv
candidate_id,name,email,phone,location,experience_years,technical_skills,match_score,application_date
1,"John Smith","john@example.com","+1-555-0101","Mumbai",5,"Python, Django, PostgreSQL",92.5,"2025-11-21T10:30:00Z"
2,"Jane Doe","jane@example.com","+1-555-0102","San Francisco",3,"React, JavaScript, Node.js",87.3,"2025-11-21T09:15:00Z"
```

**Error Responses**:
- `404 Not Found`: Job ID does not exist
- `401 Unauthorized`: Missing or invalid API key

---

### **Job Management Endpoints (2)**

#### **GET /v1/jobs** - List All Jobs
**Description**: Retrieve all jobs with pagination and filtering options  
**Authentication**: API Key required  
**Rate Limit**: 100 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs?limit=10&offset=0&department=Engineering"
```

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `limit` (optional): Number of jobs to return (1-100, default: 50)
- `offset` (optional): Number of jobs to skip (default: 0)
- `department` (optional): Filter by department
- `location` (optional): Filter by location
- `experience_level` (optional): Filter by experience level (`entry|mid|senior|lead`)
- `status` (optional): Filter by status (`active|closed|draft`)
- `sort_by` (optional): Sort field (`created_at|title|department`, default: `created_at`)
- `sort_order` (optional): Sort order (`asc|desc`, default: `desc`)

**Response Schema**:
```json
{
  "jobs": [
    {
      "id": "integer",
      "title": "string",
      "department": "string",
      "location": "string",
      "experience_level": "entry|mid|senior|lead",
      "requirements": "string",
      "description": "string",
      "salary_range": "string",
      "status": "active|closed|draft",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)",
      "applications_count": "integer"
    }
  ],
  "total": "integer",
  "count": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

**Example Response**:
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "department": "Engineering",
      "location": "Remote",
      "experience_level": "senior",
      "requirements": "Python, Django, PostgreSQL, REST APIs, 5+ years experience",
      "description": "We are looking for a senior Python developer to join our team...",
      "salary_range": "$120,000 - $150,000",
      "status": "active",
      "created_at": "2025-11-21T10:30:00Z",
      "updated_at": "2025-11-21T10:30:00Z",
      "applications_count": 15
    }
  ],
  "total": 19,
  "count": 1,
  "limit": 10,
  "offset": 0
}
```

#### **POST /v1/jobs** - Create New Job
**Description**: Create a new job posting with full details  
**Authentication**: API Key or Client JWT required  
**Rate Limit**: 20 requests/minute

```bash
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "department": "Engineering",
    "location": "San Francisco, CA",
    "experience_level": "mid",
    "requirements": "Python, React, 3+ years experience, Bachelor degree",
    "description": "Join our engineering team to build scalable web applications...",
    "salary_range": "$90,000 - $120,000",
    "employment_type": "full-time",
    "remote_allowed": true
  }' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs
```

**Headers**:
- `Authorization`: Bearer token (required)
- `Content-Type`: application/json (required)

**Request Schema**:
```json
{
  "title": "string (required, 3-200 chars)",
  "department": "string (required)",
  "location": "string (required)",
  "experience_level": "entry|mid|senior|lead (required)",
  "requirements": "string (required, max 2000 chars)",
  "description": "string (required, max 5000 chars)",
  "salary_range": "string (optional)",
  "employment_type": "full-time|part-time|contract|internship (optional)",
  "remote_allowed": "boolean (optional)",
  "benefits": "string (optional)",
  "application_deadline": "string (ISO 8601, optional)"
}
```

**Response Schema**:
```json
{
  "status": "success",
  "message": "string",
  "job_id": "integer",
  "job": {
    "id": "integer",
    "title": "string",
    "department": "string",
    "status": "active",
    "created_at": "string (ISO 8601)"
  }
}
```

**Example Response**:
```json
{
  "status": "success",
  "message": "Job created successfully",
  "job_id": 20,
  "job": {
    "id": 20,
    "title": "Software Engineer",
    "department": "Engineering",
    "status": "active",
    "created_at": "2025-11-21T10:30:00Z"
  }
}
```

**Validation Rules**:
- `title`: 3-200 characters, alphanumeric and spaces
- `department`: Must be from predefined list (Engineering, Marketing, Sales, HR, Finance, Operations)
- `experience_level`: Must be one of: entry, mid, senior, lead
- `requirements`: Maximum 2000 characters
- `description`: Maximum 5000 characters
- `salary_range`: Optional, format: "$X - $Y" or "$X+"

**Error Responses**:
- `400 Bad Request`: Invalid JSON format
- `401 Unauthorized`: Missing or invalid API key
- `422 Unprocessable Entity`: Validation errors (missing required fields, invalid values)
- `429 Too Many Requests`: Rate limit exceeded

---

### **Candidate Management Endpoints (5)**

#### **GET /v1/candidates** - List Candidates with Pagination
**Description**: Retrieve all candidates with advanced pagination and filtering  
**Authentication**: API Key required  
**Rate Limit**: 100 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates?limit=10&offset=0&skills=Python&location=Mumbai"
```

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `limit` (optional): Number of candidates to return (1-100, default: 50)
- `offset` (optional): Number of candidates to skip (default: 0)
- `skills` (optional): Filter by technical skills (comma-separated)
- `location` (optional): Filter by location
- `experience_min` (optional): Minimum years of experience (integer)
- `experience_max` (optional): Maximum years of experience (integer)
- `education_level` (optional): Filter by education (`High School|Bachelors|Masters|PhD`)
- `seniority_level` (optional): Filter by seniority level
- `status` (optional): Filter by status (`applied|interviewed|hired|rejected`)
- `sort_by` (optional): Sort field (`name|experience_years|created_at`, default: `created_at`)
- `sort_order` (optional): Sort order (`asc|desc`, default: `desc`)

**Response Schema**:
```json
{
  "candidates": [
    {
      "id": "integer",
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "experience_years": "integer",
      "technical_skills": "string",
      "seniority_level": "string",
      "education_level": "string",
      "status": "string",
      "resume_path": "string",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)"
    }
  ],
  "total": "integer",
  "count": "integer",
  "limit": "integer",
  "offset": "integer",
  "filters_applied": "object"
}
```

**Example Response**:
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1-555-0101",
      "location": "Mumbai",
      "experience_years": 5,
      "technical_skills": "Python, Django, PostgreSQL, REST APIs",
      "seniority_level": "Software Developer",
      "education_level": "Masters",
      "status": "applied",
      "resume_path": "/resumes/john_smith.pdf",
      "created_at": "2025-11-21T10:30:00Z",
      "updated_at": "2025-11-21T10:30:00Z"
    }
  ],
  "total": 10,
  "count": 1,
  "limit": 10,
  "offset": 0,
  "filters_applied": {
    "skills": "Python",
    "location": "Mumbai"
  }
}
```

#### **GET /v1/candidates/{id}** - Get Specific Candidate
**Description**: Retrieve detailed information for a specific candidate  
**Authentication**: API Key required  
**Rate Limit**: 200 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/1
```

**Path Parameters**:
- `id` (required): Candidate ID (integer)

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `include_applications` (optional): `true|false` - Include job applications (default: `false`)
- `include_interviews` (optional): `true|false` - Include interview history (default: `false`)
- `include_feedback` (optional): `true|false` - Include feedback records (default: `false`)

**Response Schema**:
```json
{
  "candidate": {
    "id": "integer",
    "name": "string",
    "email": "string",
    "phone": "string",
    "location": "string",
    "experience_years": "integer",
    "technical_skills": "string",
    "seniority_level": "string",
    "education_level": "string",
    "status": "string",
    "resume_path": "string",
    "linkedin_url": "string",
    "github_url": "string",
    "portfolio_url": "string",
    "created_at": "string (ISO 8601)",
    "updated_at": "string (ISO 8601)",
    "applications": "array (optional)",
    "interviews": "array (optional)",
    "feedback": "array (optional)"
  }
}
```

**Example Response**:
```json
{
  "candidate": {
    "id": 1,
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+1-555-0101",
    "location": "Mumbai",
    "experience_years": 5,
    "technical_skills": "Python, Django, PostgreSQL, REST APIs, Docker, AWS",
    "seniority_level": "Software Developer",
    "education_level": "Masters",
    "status": "applied",
    "resume_path": "/resumes/john_smith.pdf",
    "linkedin_url": "https://linkedin.com/in/johnsmith",
    "github_url": "https://github.com/johnsmith",
    "portfolio_url": "https://johnsmith.dev",
    "created_at": "2025-11-21T10:30:00Z",
    "updated_at": "2025-11-21T10:30:00Z"
  }
}
```

**Error Responses**:
- `404 Not Found`: Candidate ID does not exist
- `401 Unauthorized`: Missing or invalid API key

#### **GET /v1/candidates/search** - Advanced Search with Filters
**Description**: Advanced candidate search with multiple filter options and AI-powered matching  
**Authentication**: API Key required  
**Rate Limit**: 50 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/search?skills=Python,Django&location=Mumbai&experience_min=3&experience_max=8&education_level=Masters"
```

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `skills` (optional): Comma-separated list of technical skills
- `location` (optional): Location filter (supports partial matching)
- `experience_min` (optional): Minimum years of experience (integer, 0-50)
- `experience_max` (optional): Maximum years of experience (integer, 0-50)
- `education_level` (optional): Education level (`High School|Bachelors|Masters|PhD`)
- `seniority_level` (optional): Seniority level filter
- `status` (optional): Candidate status (`applied|interviewed|hired|rejected`)
- `limit` (optional): Number of results (1-100, default: 20)
- `offset` (optional): Results offset (default: 0)
- `ai_match` (optional): `true|false` - Use AI semantic matching (default: `false`)
- `match_threshold` (optional): AI match threshold (0.0-1.0, default: 0.7)

**Response Schema**:
```json
{
  "candidates": [
    {
      "id": "integer",
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "technical_skills": "string",
      "experience_years": "integer",
      "seniority_level": "string",
      "education_level": "string",
      "status": "string",
      "match_score": "number (if ai_match=true)",
      "match_reasoning": "string (if ai_match=true)"
    }
  ],
  "filters_applied": "object",
  "total_matches": "integer",
  "count": "integer",
  "ai_matching_enabled": "boolean",
  "search_timestamp": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "candidates": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1-555-0101",
      "location": "Mumbai",
      "technical_skills": "Python, Django, PostgreSQL, REST APIs",
      "experience_years": 5,
      "seniority_level": "Software Developer",
      "education_level": "Masters",
      "status": "applied",
      "match_score": 0.92,
      "match_reasoning": "Strong match: Python (0.95), Django (0.89), Experience: 5y matches requirement"
    }
  ],
  "filters_applied": {
    "skills": ["Python", "Django"],
    "location": "Mumbai",
    "experience_min": 3,
    "experience_max": 8,
    "education_level": "Masters"
  },
  "total_matches": 15,
  "count": 1,
  "ai_matching_enabled": true,
  "search_timestamp": "2025-11-21T10:30:00Z"
}
```

#### **POST /v1/candidates/bulk** - Bulk Upload with Validation
**Description**: Upload multiple candidates at once with comprehensive validation  
**Authentication**: API Key required  
**Rate Limit**: 5 requests/minute  
**Max Candidates**: 50 per request

```bash
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": [
      {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "+1-555-0102",
        "location": "San Francisco, CA",
        "experience_years": 3,
        "technical_skills": "React, JavaScript, Node.js, TypeScript",
        "seniority_level": "Mid-level Developer",
        "education_level": "Bachelors",
        "linkedin_url": "https://linkedin.com/in/janedoe",
        "github_url": "https://github.com/janedoe"
      },
      {
        "name": "Mike Johnson",
        "email": "mike@example.com",
        "phone": "+1-555-0103",
        "location": "New York, NY",
        "experience_years": 7,
        "technical_skills": "Java, Spring Boot, Microservices, AWS",
        "seniority_level": "Senior Developer",
        "education_level": "Masters"
      }
    ],
    "validate_emails": true,
    "skip_duplicates": true
  }' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/bulk
```

**Headers**:
- `Authorization`: Bearer token (required)
- `Content-Type`: application/json (required)

**Request Schema**:
```json
{
  "candidates": [
    {
      "name": "string (required, 2-100 chars)",
      "email": "string (required, valid email)",
      "phone": "string (optional, valid phone)",
      "location": "string (required)",
      "experience_years": "integer (required, 0-50)",
      "technical_skills": "string (required)",
      "seniority_level": "string (optional)",
      "education_level": "string (optional)",
      "linkedin_url": "string (optional, valid URL)",
      "github_url": "string (optional, valid URL)",
      "portfolio_url": "string (optional, valid URL)"
    }
  ],
  "validate_emails": "boolean (optional, default: true)",
  "skip_duplicates": "boolean (optional, default: false)",
  "send_notifications": "boolean (optional, default: false)"
}
```

**Response Schema**:
```json
{
  "status": "success|partial|error",
  "message": "string",
  "candidates_received": "integer",
  "candidates_inserted": "integer",
  "candidates_skipped": "integer",
  "errors": [
    {
      "index": "integer",
      "field": "string",
      "message": "string",
      "candidate_data": "object"
    }
  ],
  "total_errors": "integer",
  "processing_time": "string",
  "inserted_ids": "array of integers"
}
```

**Example Response**:
```json
{
  "status": "success",
  "message": "Bulk upload completed successfully",
  "candidates_received": 2,
  "candidates_inserted": 2,
  "candidates_skipped": 0,
  "errors": [],
  "total_errors": 0,
  "processing_time": "0.245s",
  "inserted_ids": [11, 12]
}
```

**Validation Rules**:
- `name`: 2-100 characters, letters and spaces only
- `email`: Valid email format, unique in database
- `phone`: Valid international phone format (optional)
- `experience_years`: Integer between 0-50
- `technical_skills`: Non-empty string, comma-separated recommended
- URLs: Valid HTTP/HTTPS format if provided

**Error Responses**:
- `400 Bad Request`: Invalid JSON or request format
- `413 Payload Too Large`: More than 50 candidates in request
- `422 Unprocessable Entity`: Validation errors in candidate data

#### **GET /v1/candidates/job/{job_id}** - Candidates by Job
**Description**: Get all candidates who applied for a specific job  
**Authentication**: API Key required  
**Rate Limit**: 100 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/job/1?include_scores=true&status=applied"
```

**Path Parameters**:
- `job_id` (required): Job ID (integer)

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `include_scores` (optional): `true|false` - Include AI matching scores (default: `false`)
- `status` (optional): Filter by application status (`applied|reviewed|interviewed|hired|rejected`)
- `limit` (optional): Number of candidates (1-100, default: 50)
- `offset` (optional): Results offset (default: 0)
- `sort_by` (optional): Sort field (`match_score|application_date|name`, default: `application_date`)
- `sort_order` (optional): Sort order (`asc|desc`, default: `desc`)

**Response Schema**:
```json
{
  "job_id": "integer",
  "job_title": "string",
  "candidates": [
    {
      "id": "integer",
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "experience_years": "integer",
      "technical_skills": "string",
      "seniority_level": "string",
      "education_level": "string",
      "application_date": "string (ISO 8601)",
      "application_status": "string",
      "match_score": "number (if include_scores=true)",
      "match_reasoning": "string (if include_scores=true)"
    }
  ],
  "total_applications": "integer",
  "count": "integer",
  "filters_applied": "object"
}
```

**Example Response**:
```json
{
  "job_id": 1,
  "job_title": "Senior Python Developer",
  "candidates": [
    {
      "id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1-555-0101",
      "location": "Mumbai",
      "experience_years": 5,
      "technical_skills": "Python, Django, PostgreSQL, REST APIs",
      "seniority_level": "Software Developer",
      "education_level": "Masters",
      "application_date": "2025-11-21T10:30:00Z",
      "application_status": "applied",
      "match_score": 92.5,
      "match_reasoning": "Strong technical match: Python (0.95), Django (0.89), 5y experience aligns with senior role"
    }
  ],
  "total_applications": 15,
  "count": 1,
  "filters_applied": {
    "status": "applied",
    "include_scores": true
  }
}
```

**Error Responses**:
- `404 Not Found`: Job ID does not exist
- `401 Unauthorized`: Missing or invalid API key

---

### **AI Matching Endpoints (2)**

#### **GET /v1/match/{job_id}/top** - AI-Powered Semantic Matching
**Description**: Get top candidate matches for a job using Phase 3 AI semantic matching  
**Authentication**: API Key required  
**Rate Limit**: 20 requests/minute  
**Processing Time**: <0.02 seconds

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/match/1/top?limit=5&threshold=0.7&include_reasoning=true"
```

**Path Parameters**:
- `job_id` (required): Job ID to match candidates against (integer)

**Headers**:
- `Authorization`: Bearer token (required)

**Query Parameters**:
- `limit` (optional): Number of top matches to return (1-50, default: 10)
- `threshold` (optional): Minimum match score threshold (0.0-1.0, default: 0.6)
- `include_reasoning` (optional): `true|false` - Include AI reasoning (default: `true`)
- `algorithm` (optional): `semantic|hybrid|traditional` - Matching algorithm (default: `semantic`)
- `boost_location` (optional): `true|false` - Boost local candidates (default: `false`)
- `boost_experience` (optional): `true|false` - Boost experience match (default: `true`)

**Response Schema**:
```json
{
  "matches": [
    {
      "candidate_id": "integer",
      "name": "string",
      "email": "string",
      "phone": "string",
      "location": "string",
      "score": "number (0-100)",
      "confidence": "number (0-1)",
      "skills_match": "array of strings",
      "skills_score": "number (0-1)",
      "experience_match": "string",
      "experience_score": "number (0-1)",
      "location_match": "boolean",
      "location_score": "number (0-1)",
      "education_match": "string",
      "reasoning": "string",
      "recommendation_strength": "Excellent|Strong|Good|Fair",
      "semantic_similarity": "number (0-1)"
    }
  ],
  "job_id": "integer",
  "job_title": "string",
  "limit": "integer",
  "threshold": "number",
  "total_candidates_analyzed": "integer",
  "matches_found": "integer",
  "algorithm_version": "string",
  "processing_time": "string",
  "ai_analysis": "string",
  "agent_status": "connected|disconnected",
  "timestamp": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "matches": [
    {
      "candidate_id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "phone": "+1-555-0101",
      "location": "Mumbai",
      "score": 92.5,
      "confidence": 0.94,
      "skills_match": ["Python", "Django", "PostgreSQL", "REST APIs"],
      "skills_score": 0.89,
      "experience_match": "5y - Exceeds minimum requirement",
      "experience_score": 0.95,
      "location_match": true,
      "location_score": 1.0,
      "education_match": "Masters - Meets requirement",
      "reasoning": "Exceptional match: Strong semantic similarity (0.89) in Python/Django stack. 5 years experience exceeds 3+ requirement. Masters degree aligns with senior role. Location preference match.",
      "recommendation_strength": "Excellent",
      "semantic_similarity": 0.89
    }
  ],
  "job_id": 1,
  "job_title": "Senior Python Developer",
  "limit": 5,
  "threshold": 0.7,
  "total_candidates_analyzed": 10,
  "matches_found": 1,
  "algorithm_version": "3.0.0-phase3-production",
  "processing_time": "0.015s",
  "ai_analysis": "Phase 3 semantic matching with sentence transformers",
  "agent_status": "connected",
  "timestamp": "2025-11-21T10:30:00Z"
}
```

**Match Score Breakdown**:
- **90-100**: Excellent match - Highly recommended
- **80-89**: Strong match - Recommended
- **70-79**: Good match - Consider for interview
- **60-69**: Fair match - Review carefully
- **<60**: Poor match - Not recommended

**Error Responses**:
- `404 Not Found`: Job ID does not exist
- `401 Unauthorized`: Missing or invalid API key
- `503 Service Unavailable`: AI Agent service unavailable

#### **POST /v1/match/batch** - Batch Matching for Multiple Jobs
**Description**: Process AI matching for multiple jobs simultaneously with optimized batch processing  
**Authentication**: API Key required  
**Rate Limit**: 5 requests/minute  
**Max Jobs**: 20 per request  
**Processing**: 50 candidates per chunk

```bash
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{
    "job_ids": [1, 2, 3],
    "limit_per_job": 5,
    "threshold": 0.7,
    "include_reasoning": true,
    "algorithm": "semantic"
  }' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/match/batch
```

**Headers**:
- `Authorization`: Bearer token (required)
- `Content-Type`: application/json (required)

**Request Schema**:
```json
{
  "job_ids": "array of integers (required, 1-20 jobs)",
  "limit_per_job": "integer (optional, 1-20, default: 5)",
  "threshold": "number (optional, 0.0-1.0, default: 0.6)",
  "include_reasoning": "boolean (optional, default: true)",
  "algorithm": "semantic|hybrid|traditional (optional, default: semantic)",
  "boost_location": "boolean (optional, default: false)",
  "parallel_processing": "boolean (optional, default: true)"
}
```

**Response Schema**:
```json
{
  "batch_results": {
    "[job_id]": {
      "job_id": "integer",
      "job_title": "string",
      "matches": [
        {
          "candidate_id": "integer",
          "name": "string",
          "email": "string",
          "score": "number (0-100)",
          "confidence": "number (0-1)",
          "skills_match": "array",
          "reasoning": "string",
          "recommendation_strength": "string"
        }
      ],
      "matches_found": "integer",
      "candidates_analyzed": "integer",
      "processing_time": "string",
      "algorithm": "string"
    }
  },
  "summary": {
    "total_jobs_processed": "integer",
    "total_jobs_requested": "integer",
    "total_matches_found": "integer",
    "total_candidates_analyzed": "integer",
    "average_processing_time": "string",
    "failed_jobs": "array"
  },
  "algorithm_version": "string",
  "batch_processing_time": "string",
  "status": "success|partial|error",
  "timestamp": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "batch_results": {
    "1": {
      "job_id": 1,
      "job_title": "Senior Python Developer",
      "matches": [
        {
          "candidate_id": 1,
          "name": "John Smith",
          "email": "john@example.com",
          "score": 92.5,
          "confidence": 0.94,
          "skills_match": ["Python", "Django", "PostgreSQL"],
          "reasoning": "Exceptional semantic match for Python development role",
          "recommendation_strength": "Excellent"
        }
      ],
      "matches_found": 1,
      "candidates_analyzed": 10,
      "processing_time": "0.023s",
      "algorithm": "semantic-batch"
    },
    "2": {
      "job_id": 2,
      "job_title": "Frontend Developer",
      "matches": [
        {
          "candidate_id": 2,
          "name": "Jane Doe",
          "email": "jane@example.com",
          "score": 87.3,
          "confidence": 0.91,
          "skills_match": ["React", "JavaScript", "TypeScript"],
          "reasoning": "Strong frontend skills alignment with modern stack",
          "recommendation_strength": "Strong"
        }
      ],
      "matches_found": 1,
      "candidates_analyzed": 10,
      "processing_time": "0.019s",
      "algorithm": "semantic-batch"
    }
  },
  "summary": {
    "total_jobs_processed": 2,
    "total_jobs_requested": 3,
    "total_matches_found": 2,
    "total_candidates_analyzed": 20,
    "average_processing_time": "0.021s",
    "failed_jobs": [3]
  },
  "algorithm_version": "3.0.0-phase3-production-batch",
  "batch_processing_time": "0.156s",
  "status": "partial",
  "timestamp": "2025-11-21T10:30:00Z"
}
```

**Performance Optimization**:
- **Parallel Processing**: Jobs processed simultaneously
- **Chunked Analysis**: 50 candidates per processing chunk
- **Caching**: Results cached for 15 minutes
- **Load Balancing**: Distributed across AI agents

**Error Responses**:
- `400 Bad Request`: Invalid job IDs or request format
- `413 Payload Too Large`: More than 20 jobs requested
- `401 Unauthorized`: Missing or invalid API key
- `503 Service Unavailable`: AI Agent service unavailable

---

### **Assessment Workflow Endpoints (6)**

#### **POST /v1/feedback** - Values Assessment (5-Point BHIV Values)
**Description**: Submit values-based feedback for candidates using BHIV core values  
**Authentication**: API Key required  
**Rate Limit**: 30 requests/minute

```bash
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "integrity": 5,
    "honesty": 4,
    "discipline": 4,
    "hard_work": 5,
    "gratitude": 4,
    "comments": "Excellent candidate with strong values alignment",
    "interviewer_name": "John Manager"
  }' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/feedback
```

**Headers**:
- `Authorization`: Bearer token (required)
- `Content-Type`: application/json (required)

**Request Schema**:
```json
{
  "candidate_id": "integer (required)",
  "job_id": "integer (required)",
  "integrity": "integer (required, 1-5)",
  "honesty": "integer (required, 1-5)",
  "discipline": "integer (required, 1-5)",
  "hard_work": "integer (required, 1-5)",
  "gratitude": "integer (required, 1-5)",
  "comments": "string (optional, max 1000 chars)",
  "interviewer_name": "string (optional)",
  "interview_type": "technical|behavioral|cultural|final (optional)"
}
```

**Response Schema**:
```json
{
  "status": "success",
  "message": "string",
  "feedback_id": "integer",
  "candidate_id": "integer",
  "job_id": "integer",
  "values_scores": {
    "integrity": "integer",
    "honesty": "integer",
    "discipline": "integer",
    "hard_work": "integer",
    "gratitude": "integer"
  },
  "average_score": "number",
  "submitted_at": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "status": "success",
  "message": "Feedback submitted successfully",
  "feedback_id": 1,
  "candidate_id": 1,
  "job_id": 1,
  "values_scores": {
    "integrity": 5,
    "honesty": 4,
    "discipline": 4,
    "hard_work": 5,
    "gratitude": 4
  },
  "average_score": 4.4,
  "submitted_at": "2025-11-21T10:30:00Z"
}
```

#### **GET /v1/feedback** - Get All Feedback Records
**Description**: Retrieve all feedback records with filtering options  
**Authentication**: API Key required  
**Rate Limit**: 50 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/feedback?candidate_id=1&job_id=1"
```

**Query Parameters**:
- `candidate_id` (optional): Filter by candidate ID
- `job_id` (optional): Filter by job ID
- `interviewer_name` (optional): Filter by interviewer
- `limit` (optional): Number of records (1-100, default: 50)
- `offset` (optional): Records offset (default: 0)

**Response Schema**:
```json
{
  "feedback_records": [
    {
      "id": "integer",
      "candidate_id": "integer",
      "candidate_name": "string",
      "job_id": "integer",
      "job_title": "string",
      "values_scores": "object",
      "average_score": "number",
      "comments": "string",
      "interviewer_name": "string",
      "submitted_at": "string (ISO 8601)"
    }
  ],
  "total": "integer",
  "count": "integer"
}
```

#### **POST /v1/interviews** - Schedule Interview
**Description**: Schedule interviews with candidates for specific jobs  
**Authentication**: API Key required  
**Rate Limit**: 20 requests/minute

```bash
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "interview_date": "2025-12-01T10:00:00Z",
    "interviewer": "John Manager",
    "interview_type": "technical",
    "duration_minutes": 60,
    "location": "Conference Room A",
    "notes": "Technical interview scheduled"
  }' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/interviews
```

**Request Schema**:
```json
{
  "candidate_id": "integer (required)",
  "job_id": "integer (required)",
  "interview_date": "string (required, ISO 8601)",
  "interviewer": "string (required)",
  "interview_type": "technical|behavioral|cultural|final (optional)",
  "duration_minutes": "integer (optional, default: 60)",
  "location": "string (optional)",
  "meeting_link": "string (optional, valid URL)",
  "notes": "string (optional, max 500 chars)"
}
```

**Response Schema**:
```json
{
  "status": "success",
  "message": "string",
  "interview_id": "integer",
  "candidate_id": "integer",
  "job_id": "integer",
  "interview_date": "string (ISO 8601)",
  "status": "scheduled",
  "created_at": "string (ISO 8601)"
}
```

**Example Response**:
```json
{
  "status": "success",
  "message": "Interview scheduled successfully",
  "interview_id": 1,
  "candidate_id": 1,
  "job_id": 1,
  "interview_date": "2025-12-01T10:00:00Z",
  "status": "scheduled",
  "created_at": "2025-11-21T10:30:00Z"
}
```

#### **GET /v1/interviews** - Get All Interviews
**Description**: Retrieve all scheduled interviews with filtering options  
**Authentication**: API Key required  
**Rate Limit**: 50 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/interviews?status=scheduled&date_from=2025-11-21"
```

**Query Parameters**:
- `candidate_id` (optional): Filter by candidate ID
- `job_id` (optional): Filter by job ID
- `interviewer` (optional): Filter by interviewer name
- `status` (optional): Filter by status (`scheduled|completed|cancelled|rescheduled`)
- `date_from` (optional): Filter interviews from date (ISO 8601)
- `date_to` (optional): Filter interviews to date (ISO 8601)
- `limit` (optional): Number of records (1-100, default: 50)

**Response Schema**:
```json
{
  "interviews": [
    {
      "id": "integer",
      "candidate_id": "integer",
      "candidate_name": "string",
      "job_id": "integer",
      "job_title": "string",
      "interview_date": "string (ISO 8601)",
      "interviewer": "string",
      "interview_type": "string",
      "duration_minutes": "integer",
      "location": "string",
      "status": "string",
      "notes": "string"
    }
  ],
  "total": "integer",
  "count": "integer"
}
```

#### **POST /v1/offers** - Job Offers Management
**Description**: Create job offers for candidates  
**Authentication**: API Key required  
**Rate Limit**: 10 requests/minute

```bash
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "salary": 120000.00,
    "currency": "USD",
    "start_date": "2025-12-15",
    "employment_type": "full-time",
    "benefits": "Health insurance, 401k, PTO",
    "terms": "Full-time position with benefits",
    "expiry_date": "2025-12-01"
  }' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/offers
```

**Request Schema**:
```json
{
  "candidate_id": "integer (required)",
  "job_id": "integer (required)",
  "salary": "number (required)",
  "currency": "string (optional, default: USD)",
  "start_date": "string (required, ISO 8601 date)",
  "employment_type": "full-time|part-time|contract|internship (optional)",
  "benefits": "string (optional)",
  "terms": "string (optional, max 2000 chars)",
  "expiry_date": "string (optional, ISO 8601 date)",
  "remote_allowed": "boolean (optional)"
}
```

**Response Schema**:
```json
{
  "status": "success",
  "message": "string",
  "offer_id": "integer",
  "candidate_id": "integer",
  "job_id": "integer",
  "salary": "number",
  "status": "pending",
  "created_at": "string (ISO 8601)"
}
```

#### **GET /v1/offers** - Get All Job Offers
**Description**: Retrieve all job offers with filtering options  
**Authentication**: API Key required  
**Rate Limit**: 50 requests/minute

```bash
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/offers?status=pending&candidate_id=1"
```

**Query Parameters**:
- `candidate_id` (optional): Filter by candidate ID
- `job_id` (optional): Filter by job ID
- `status` (optional): Filter by status (`pending|accepted|rejected|expired`)
- `salary_min` (optional): Minimum salary filter
- `salary_max` (optional): Maximum salary filter
- `limit` (optional): Number of records (1-100, default: 50)

**Response Schema**:
```json
{
  "offers": [
    {
      "id": "integer",
      "candidate_id": "integer",
      "candidate_name": "string",
      "job_id": "integer",
      "job_title": "string",
      "salary": "number",
      "currency": "string",
      "start_date": "string",
      "employment_type": "string",
      "status": "string",
      "created_at": "string (ISO 8601)",
      "expiry_date": "string"
    }
  ],
  "total": "integer",
  "count": "integer"
}
```

---

### **Security Testing Endpoints (7)**

#### **GET /v1/security/rate-limit-status** - Check Rate Limit Status
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/rate-limit-status
```
**Response:**
```json
{
  "rate_limit_enabled": true,
  "requests_per_minute": 60,
  "current_requests": 15,
  "remaining_requests": 45,
  "reset_time": "2025-01-XX T XX:XX:XX Z",
  "status": "active"
}
```

#### **POST /v1/security/test-input-validation** - Test Input Validation
```bash
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{"input_data": "<script>alert(\"test\")</script>"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/test-input-validation
```
**Response:**
```json
{
  "input": "<script>alert(\"test\")</script>",
  "validation_result": "BLOCKED",
  "threats_detected": ["XSS attempt detected"],
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

#### **POST /v1/security/test-email-validation** - Test Email Validation
```bash
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/test-email-validation
```

#### **POST /v1/security/test-phone-validation** - Test Phone Validation
```bash
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{"phone": "+1-555-123-4567"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/test-phone-validation
```

#### **GET /v1/security/security-headers-test** - Test Security Headers
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/security-headers-test
```

#### **GET /v1/security/blocked-ips** - View Blocked IPs
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/blocked-ips
```

#### **GET /v1/security/penetration-test-endpoints** - Penetration Testing Endpoints
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/penetration-test-endpoints
```

---

### **2FA Authentication Endpoints (8)**

#### **POST /v1/2fa/setup** - Setup 2FA for Client
```bash
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "client_001"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/2fa/setup
```
**Response:**
```json
{
  "message": "2FA setup initiated",
  "user_id": "client_001",
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "manual_entry_key": "JBSWY3DPEHPK3PXP",
  "instructions": "Scan QR code with Google Authenticator, Microsoft Authenticator, or Authy"
}
```

#### **POST /v1/2fa/verify-setup** - Verify 2FA Setup
```bash
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "client_001", "totp_code": "123456"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/2fa/verify-setup
```

#### **POST /v1/2fa/login-with-2fa** - Login with 2FA
```bash
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "client_001", "totp_code": "123456"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/2fa/login-with-2fa
```

#### **GET /v1/2fa/status/{client_id}** - Get 2FA Status
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/2fa/status/client_001
```

#### **POST /v1/2fa/disable** - Disable 2FA
#### **POST /v1/2fa/regenerate-backup-codes** - Regenerate Backup Codes
#### **GET /v1/2fa/test-token/{client_id}/{token}** - Test 2FA Token
#### **GET /v1/2fa/demo-setup** - Demo 2FA Setup

---

### **Client Portal Endpoints (1)**

#### **POST /v1/client/login** - Client Authentication with JWT
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"client_id": "TECH001", "password": "demo123"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login
```
**Response:**
```json
{
  "success": true,
  "message": "Authentication successful",
  "client_id": "TECH001",
  "company_name": "Tech Innovations Inc",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "permissions": ["view_jobs", "create_jobs", "view_candidates", "schedule_interviews"]
}
```

---

### **Candidate Portal Endpoints (5)**

#### **POST /v1/candidate/register** - Candidate Registration
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith",
       "email": "jane@example.com",
       "password": "securepassword123",
       "phone": "+1-555-0123",
       "location": "San Francisco",
       "experience_years": 3,
       "technical_skills": "React, JavaScript, Node.js",
       "education_level": "Bachelors",
       "seniority_level": "Mid-level"
     }' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/register
```
**Response:**
```json
{
  "success": true,
  "message": "Registration successful",
  "candidate_id": 32
}
```

#### **POST /v1/candidate/login** - Candidate Login with JWT
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "jane@example.com", "password": "securepassword123"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/login
```
**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "candidate": {
    "id": 32,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+1-555-0123",
    "location": "San Francisco",
    "experience_years": 3,
    "technical_skills": "React, JavaScript, Node.js",
    "seniority_level": "Mid-level",
    "education_level": "Bachelors",
    "status": "applied"
  }
}
```

#### **PUT /v1/candidate/profile/{id}** - Update Candidate Profile
```bash
curl -X PUT -H "Authorization: Bearer <candidate_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Jane Smith Updated",
       "technical_skills": "React, JavaScript, Node.js, TypeScript",
       "experience_years": 4
     }' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/profile/32
```

#### **POST /v1/candidate/apply** - Job Application Submission
```bash
curl -X POST -H "Authorization: Bearer <candidate_jwt_token>" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 32,
       "job_id": 1,
       "cover_letter": "I am very interested in this position..."
     }' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/apply
```

#### **GET /v1/candidate/applications/{id}** - Get Candidate Applications
```bash
curl -H "Authorization: Bearer <candidate_jwt_token>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/applications/32
```

---

## 🤖 Agent Service API (6 Endpoints)

### **Base URL**
- **Production**: https://bhiv-hr-agent-nhgg.onrender.com
- **Local**: http://localhost:9000

### **Core Endpoints (2)**

#### **GET /** - Service Information
```bash
curl https://bhiv-hr-agent-nhgg.onrender.com/
```
**Response:**
```json
{
  "service": "BHIV AI Agent",
  "version": "3.0.0",
  "endpoints": 6,
  "available_endpoints": {
    "root": "GET / - Service information",
    "health": "GET /health - Service health check",
    "test_db": "GET /test-db - Database connectivity test",
    "match": "POST /match - AI-powered candidate matching",
    "batch_match": "POST /batch-match - Batch AI matching for multiple jobs",
    "analyze": "GET /analyze/{candidate_id} - Detailed candidate analysis"
  }
}
```

#### **GET /health** - Health Check
```bash
curl https://bhiv-hr-agent-nhgg.onrender.com/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "BHIV AI Agent",
  "version": "3.0.0",
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

---

### **AI Processing Endpoints (3)**

#### **POST /match** - Phase 3 AI Semantic Matching
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"job_id": 1}' \
     https://bhiv-hr-agent-nhgg.onrender.com/match
```
**Response:**
```json
{
  "job_id": 1,
  "top_candidates": [
    {
      "candidate_id": 1,
      "name": "John Smith",
      "email": "john@example.com",
      "score": 92.5,
      "skills_match": ["Python", "Django", "PostgreSQL"],
      "experience_match": "5y - Phase 3 matched",
      "location_match": true,
      "reasoning": "Semantic match: 0.85; Skills: Python, Django; Experience: 5y"
    }
  ],
  "total_candidates": 10,
  "processing_time": 0.015,
  "algorithm_version": "3.0.0-phase3-production",
  "status": "success"
}
```

#### **POST /batch-match** - Batch Processing for Multiple Jobs
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"job_ids": [1, 2, 3]}' \
     https://bhiv-hr-agent-nhgg.onrender.com/batch-match
```
**Response:**
```json
{
  "batch_results": {
    "1": {
      "job_id": 1,
      "matches": [
        {
          "candidate_id": 1,
          "name": "John Smith",
          "score": 92.5,
          "reasoning": "Batch AI matching - Job 1"
        }
      ],
      "algorithm": "batch-production"
    }
  },
  "total_jobs_processed": 3,
  "total_candidates_analyzed": 31,
  "algorithm_version": "3.0.0-phase3-production-batch",
  "status": "success"
}
```

#### **GET /analyze/{candidate_id}** - Detailed Candidate Analysis
```bash
curl https://bhiv-hr-agent-nhgg.onrender.com/analyze/1
```
**Response:**
```json
{
  "candidate_id": 1,
  "name": "John Smith",
  "email": "john@example.com",
  "experience_years": 5,
  "seniority_level": "Software Developer",
  "education_level": "Masters",
  "location": "Mumbai",
  "skills_analysis": {
    "Programming": ["python", "java", "javascript"],
    "Web Development": ["django", "react"],
    "Database": ["postgresql", "mysql"]
  },
  "semantic_skills": ["Python", "Django", "PostgreSQL", "REST APIs"],
  "total_skills": 15,
  "ai_analysis_enabled": true,
  "analysis_timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

---

### **Diagnostics Endpoints (1)**

#### **GET /test-db** - Database Connectivity Test
```bash
curl https://bhiv-hr-agent-nhgg.onrender.com/test-db
```
**Response:**
```json
{
  "status": "success",
  "candidates_count": 10,
  "samples": [
    {"id": 1, "name": "John Smith"},
    {"id": 2, "name": "Jane Doe"},
    {"id": 3, "name": "Mike Johnson"}
  ]
}
```

---

## 🔄 LangGraph Service API (9 Endpoints)

### **Base URL**
- **Production**: https://bhiv-hr-langgraph.onrender.com
- **Local**: http://localhost:9001

### **Core Endpoints (2)**

#### **GET /** - Service Information
```bash
curl https://bhiv-hr-langgraph.onrender.com/
```
**Response:**
```json
{
  "service": "BHIV LangGraph Workflows",
  "version": "4.2.0",
  "endpoints": 9,
  "status": "operational",
  "workflows_available": ["application", "shortlist", "interview"]
}
```

#### **GET /health** - Health Check
```bash
curl https://bhiv-hr-langgraph.onrender.com/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "BHIV LangGraph",
  "version": "4.2.0",
  "timestamp": "2025-11-15T XX:XX:XXZ"
}
```

---

### **Workflow Management Endpoints (6)**

#### **POST /workflows/application/start** - Start Application Workflow
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"candidate_id": 1, "job_id": 1}' \
     https://bhiv-hr-langgraph.onrender.com/workflows/application/start
```
**Response:**
```json
{
  "workflow_id": "wf_app_001",
  "status": "started",
  "candidate_id": 1,
  "job_id": 1,
  "steps": ["notification_sent", "hr_notified", "status_updated"],
  "created_at": "2025-11-21T10:30:00Z"
}
```

#### **POST /workflows/shortlist/start** - Start Shortlist Workflow
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"candidate_id": 1, "job_id": 1, "shortlist_reason": "Strong technical match"}' \
     https://bhiv-hr-langgraph.onrender.com/workflows/shortlist/start
```
**Response:**
```json
{
  "workflow_id": "wf_short_001",
  "status": "started",
  "candidate_id": 1,
  "job_id": 1,
  "steps": ["candidate_shortlisted", "interview_scheduled", "notifications_sent"],
  "created_at": "2025-11-21T10:30:00Z"
}
```

#### **POST /workflows/interview/start** - Start Interview Workflow
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"candidate_id": 1, "job_id": 1, "interview_type": "technical"}' \
     https://bhiv-hr-langgraph.onrender.com/workflows/interview/start
```
**Response:**
```json
{
  "workflow_id": "wf_int_001",
  "status": "started",
  "candidate_id": 1,
  "job_id": 1,
  "steps": ["interview_scheduled", "reminders_sent", "feedback_collected"],
  "created_at": "2025-11-21T10:30:00Z"
}
```

#### **GET /workflows/{id}/status** - Get Workflow Status
```bash
curl https://bhiv-hr-langgraph.onrender.com/workflows/wf_app_001/status
```
**Response:**
```json
{
  "workflow_id": "wf_app_001",
  "status": "completed",
  "progress": "100%",
  "steps_completed": 3,
  "total_steps": 3,
  "last_updated": "2025-11-15T XX:XX:XXZ"
}
```

#### **GET /workflows** - List All Workflows
```bash
curl https://bhiv-hr-langgraph.onrender.com/workflows
```
**Response:**
```json
{
  "workflows": [
    {
      "id": "wf_app_001",
      "type": "application",
      "status": "completed",
      "candidate_id": 1,
      "job_id": 1
    }
  ],
  "total": 1
}
```

#### **POST /tools/send-notification** - Send Multi-Channel Notification
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{
       "recipient": "candidate@example.com",
       "message": "Application received",
       "channels": ["email", "sms"]
     }' \
     https://bhiv-hr-langgraph.onrender.com/tools/send-notification
```
**Response:**
```json
{
  "notification_id": "notif_001",
  "status": "sent",
  "channels_used": ["email", "sms"],
  "sent_at": "2025-11-15T XX:XX:XXZ"
}
```

---

### **Integration Endpoints (1)**

#### **GET /test-integration** - Test Gateway Integration
```bash
curl https://bhiv-hr-langgraph.onrender.com/test-integration
```
**Response:**
```json
{
  "integration_status": "connected",
  "gateway_reachable": true,
  "database_accessible": true,
  "test_timestamp": "2025-11-15T XX:XX:XXZ"
}
```

---

## 🔒 Authentication Guide

### **API Key Authentication**
```bash
# Primary authentication method
Authorization: Bearer <YOUR_API_KEY>
```

### **Client JWT Authentication**
```bash
# Step 1: Login to get JWT token
curl -X POST -H "Content-Type: application/json" \
     -d '{"client_id": "TECH001", "password": "demo123"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login

# Step 2: Use JWT token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### **Candidate JWT Authentication**
```bash
# Step 1: Register or login to get JWT token
curl -X POST -H "Content-Type: application/json" \
     -d '{"email": "candidate@example.com", "password": "password123"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/login

# Step 2: Use candidate JWT token
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📊 Rate Limiting

### **Rate Limits by Endpoint**
```
Default Tier:
- /v1/jobs: 100 requests/minute
- /v1/candidates/search: 50 requests/minute
- /v1/match: 20 requests/minute
- /v1/candidates/bulk: 5 requests/minute
- Default: 60 requests/minute

Premium Tier:
- /v1/jobs: 500 requests/minute
- /v1/candidates/search: 200 requests/minute
- /v1/match: 100 requests/minute
- /v1/candidates/bulk: 25 requests/minute
- Default: 300 requests/minute
```

### **Dynamic Rate Limiting**
Rate limits adjust based on system CPU usage:
- **High Load (>80% CPU)**: Reduce limits by 50%
- **Low Load (<30% CPU)**: Increase limits by 50%
- **Normal Load**: Standard limits apply

---

## 🚨 Error Handling

### **Standard Error Response**
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": "Email format is invalid"
  },
  "timestamp": "2025-01-XX T XX:XX:XX Z"
}
```

### **Common HTTP Status Codes**
- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Too Many Requests
- **500**: Internal Server Error

---

## 📈 Performance Metrics

### **Response Times**
- **Gateway API**: <100ms average
- **Agent API**: <50ms average
- **AI Matching**: <0.02 seconds
- **Database Queries**: <50ms

### **Throughput**
- **Gateway**: 500+ requests/minute
- **Agent**: 200+ requests/minute
- **Concurrent Users**: 10+ supported
- **Batch Processing**: 50 candidates/chunk

---

## 🔧 SDK & Integration

### **cURL Examples**
All examples provided above use cURL for easy testing and integration.

### **Python Integration Example**
```python
import requests

# API Configuration
BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com"
API_KEY = "<YOUR_API_KEY>"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Get all jobs
response = requests.get(f"{BASE_URL}/v1/jobs", headers=HEADERS)
jobs = response.json()

# AI matching
match_response = requests.get(f"{BASE_URL}/v1/match/1/top", headers=HEADERS)
matches = match_response.json()
```

### **JavaScript Integration Example**
```javascript
const BASE_URL = "https://bhiv-hr-gateway-ltg0.onrender.com";
const API_KEY = "<YOUR_API_KEY>";

const headers = {
  "Authorization": `Bearer ${API_KEY}`,
  "Content-Type": "application/json"
};

// Get candidates
fetch(`${BASE_URL}/v1/candidates`, { headers })
  .then(response => response.json())
  .then(data => console.log(data));

// AI matching
fetch(`${BASE_URL}/v1/match/1/top`, { headers })
  .then(response => response.json())
  .then(matches => console.log(matches));
```

---

## 📚 Interactive Documentation

### **Swagger UI**
- **Gateway**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
- **Agent**: https://bhiv-hr-agent-nhgg.onrender.com/docs

### **ReDoc**
- **Gateway**: https://bhiv-hr-gateway-ltg0.onrender.com/redoc
- **Agent**: https://bhiv-hr-agent-nhgg.onrender.com/redoc

---

**BHIV HR Platform API Documentation** - Complete API reference with 89 endpoints, triple authentication, and comprehensive examples.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: November 21, 2025 | **API Version**: v4.2.0 | **Status**: ✅ All Operational

---

## 📋 Complete API Endpoint Summary

### **Gateway Service (74 Endpoints)**

| Category | Endpoints | Authentication | Rate Limit |
|----------|-----------|----------------|-------------|
| **Core** | 3 | None/API Key | 30-200/min |
| **Monitoring** | 3 | None/API Key | 20-50/min |
| **Analytics** | 3 | API Key | 5-40/min |
| **Job Management** | 2 | API Key/Client JWT | 20-100/min |
| **Candidate Management** | 5 | API Key | 5-200/min |
| **AI Matching** | 2 | API Key | 5-20/min |
| **Assessment Workflow** | 6 | API Key | 10-50/min |
| **Security Testing** | 7 | API Key | 10-30/min |
| **2FA Authentication** | 8 | API Key | 5-20/min |
| **Client Portal** | 1 | None | 10/min |
| **Candidate Portal** | 5 | None/Candidate JWT | 5-50/min |
| **Additional Endpoints** | 49 | Various | Various |

### **Agent Service (6 Endpoints)**

| Endpoint | Method | Authentication | Rate Limit |
|----------|--------|----------------|-------------|
| `/` | GET | None | 100/min |
| `/health` | GET | None | 200/min |
| `/test-db` | GET | None | 50/min |
| `/match` | POST | None | 20/min |
| `/batch-match` | POST | None | 5/min |
| `/analyze/{id}` | GET | None | 30/min |

### **LangGraph Service (9 Endpoints)**

| Endpoint | Method | Authentication | Rate Limit |
|----------|--------|----------------|-------------|
| `/` | GET | None | 100/min |
| `/health` | GET | None | 200/min |
| `/workflows/application/start` | POST | None | 10/min |
| `/workflows/{id}/status` | GET | None | 50/min |
| `/workflows` | GET | None | 30/min |
| `/tools/send-notification` | POST | None | 20/min |
| `/test-integration` | GET | None | 10/min |

---

## 🔐 Authentication Examples

### **1. API Key Authentication**
```bash
# Standard API call
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/stats

# With query parameters
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates?limit=10&skills=Python"
```

### **2. Client JWT Authentication**
```bash
# Step 1: Login to get JWT
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"client_id": "TECH001", "password": "demo123"}' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login

# Step 2: Use JWT token
curl -X POST \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"title": "New Job", "department": "Engineering"}' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs
```

### **3. Candidate JWT Authentication**
```bash
# Step 1: Register or login
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "candidate@example.com", "password": "password123"}' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/login

# Step 2: Use candidate JWT
curl -X PUT \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"technical_skills": "Python, Django, React"}' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/profile/1
```

---

## 📊 Rate Limiting Details

### **Dynamic Rate Limiting**
The system implements intelligent rate limiting based on:
- **CPU Usage**: Adjusts limits based on system load
- **User Tier**: Different limits for different user types
- **Endpoint Complexity**: Higher limits for simple endpoints

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
X-RateLimit-Retry-After: 15
```

### **Rate Limit Tiers**

#### **Free Tier (Default)**
- General endpoints: 60 requests/minute
- Search endpoints: 30 requests/minute
- AI matching: 10 requests/minute
- Bulk operations: 3 requests/minute

#### **Premium Tier**
- General endpoints: 300 requests/minute
- Search endpoints: 150 requests/minute
- AI matching: 50 requests/minute
- Bulk operations: 15 requests/minute

#### **Enterprise Tier**
- General endpoints: 1000 requests/minute
- Search endpoints: 500 requests/minute
- AI matching: 200 requests/minute
- Bulk operations: 50 requests/minute

---

## 🚨 Error Handling Guide

### **Standard Error Codes**

| Code | Status | Description | Action |
|------|--------|-------------|---------|
| 400 | Bad Request | Invalid request format | Check request syntax |
| 401 | Unauthorized | Missing/invalid auth | Verify API key/JWT |
| 403 | Forbidden | Insufficient permissions | Check user role |
| 404 | Not Found | Resource doesn't exist | Verify resource ID |
| 422 | Unprocessable Entity | Validation errors | Fix input data |
| 429 | Too Many Requests | Rate limit exceeded | Wait and retry |
| 500 | Internal Server Error | Server error | Contact support |
| 503 | Service Unavailable | Service down | Try again later |

### **Error Response Examples**

#### **Validation Error (422)**
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": "Email format is invalid",
    "field": "email",
    "value": "invalid-email"
  },
  "timestamp": "2025-11-21T10:30:00Z",
  "request_id": "req_12345"
}
```

#### **Authentication Error (401)**
```json
{
  "status": "error",
  "error": {
    "code": "AUTHENTICATION_ERROR",
    "message": "Invalid API key",
    "details": "The provided API key is not valid or has expired"
  },
  "timestamp": "2025-11-21T10:30:00Z",
  "request_id": "req_12346"
}
```

#### **Rate Limit Error (429)**
```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "details": "Rate limit of 60 requests per minute exceeded",
    "retry_after": 15
  },
  "timestamp": "2025-11-21T10:30:00Z",
  "request_id": "req_12347"
}
```

---

## 🔧 SDK Examples

### **Python SDK Example**
```python
import requests
import json
from datetime import datetime

class BHIVClient:
    def __init__(self, api_key, base_url="https://bhiv-hr-gateway-ltg0.onrender.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_candidates(self, limit=10, skills=None):
        """Get candidates with optional filtering"""
        params = {"limit": limit}
        if skills:
            params["skills"] = skills
        
        response = requests.get(
            f"{self.base_url}/v1/candidates",
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def create_job(self, job_data):
        """Create a new job posting"""
        response = requests.post(
            f"{self.base_url}/v1/jobs",
            headers=self.headers,
            json=job_data
        )
        return response.json()
    
    def ai_match(self, job_id, limit=5, threshold=0.7):
        """Get AI-powered candidate matches"""
        params = {"limit": limit, "threshold": threshold}
        response = requests.get(
            f"{self.base_url}/v1/match/{job_id}/top",
            headers=self.headers,
            params=params
        )
        return response.json()

# Usage example
client = BHIVClient("bhiv_demo_api_key_2025")

# Get candidates
candidates = client.get_candidates(limit=5, skills="Python")
print(f"Found {len(candidates['candidates'])} candidates")

# Create job
job_data = {
    "title": "Senior Python Developer",
    "department": "Engineering",
    "location": "Remote",
    "experience_level": "senior",
    "requirements": "Python, Django, 5+ years",
    "description": "Join our team..."
}
job = client.create_job(job_data)
print(f"Created job with ID: {job['job_id']}")

# Get AI matches
matches = client.ai_match(job['job_id'], limit=3)
print(f"Found {len(matches['matches'])} matches")
```

### **JavaScript SDK Example**
```javascript
class BHIVClient {
    constructor(apiKey, baseUrl = "https://bhiv-hr-gateway-ltg0.onrender.com") {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.headers = {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json"
        };
    }

    async getCandidates(options = {}) {
        const { limit = 10, skills, location } = options;
        const params = new URLSearchParams({ limit });
        if (skills) params.append("skills", skills);
        if (location) params.append("location", location);

        const response = await fetch(`${this.baseUrl}/v1/candidates?${params}`, {
            headers: this.headers
        });
        return response.json();
    }

    async createJob(jobData) {
        const response = await fetch(`${this.baseUrl}/v1/jobs`, {
            method: "POST",
            headers: this.headers,
            body: JSON.stringify(jobData)
        });
        return response.json();
    }

    async aiMatch(jobId, options = {}) {
        const { limit = 5, threshold = 0.7 } = options;
        const params = new URLSearchParams({ limit, threshold });

        const response = await fetch(`${this.baseUrl}/v1/match/${jobId}/top?${params}`, {
            headers: this.headers
        });
        return response.json();
    }

    async bulkUploadCandidates(candidates) {
        const response = await fetch(`${this.baseUrl}/v1/candidates/bulk`, {
            method: "POST",
            headers: this.headers,
            body: JSON.stringify({ candidates })
        });
        return response.json();
    }
}

// Usage example
const client = new BHIVClient("bhiv_demo_api_key_2025");

// Get candidates with skills filter
client.getCandidates({ skills: "Python,Django", limit: 5 })
    .then(data => console.log(`Found ${data.candidates.length} candidates`));

// Create new job
const jobData = {
    title: "Frontend Developer",
    department: "Engineering",
    location: "San Francisco",
    experience_level: "mid",
    requirements: "React, TypeScript, 3+ years",
    description: "Build amazing user interfaces..."
};

client.createJob(jobData)
    .then(job => {
        console.log(`Created job: ${job.job_id}`);
        return client.aiMatch(job.job_id, { limit: 3 });
    })
    .then(matches => console.log(`Found ${matches.matches.length} matches`));
```

### **cURL Script Examples**

#### **Complete Job Posting Workflow**
```bash
#!/bin/bash

API_KEY="bhiv_demo_api_key_2025"
BASE_URL="https://bhiv-hr-gateway-ltg0.onrender.com"

# 1. Create a new job
echo "Creating new job..."
JOB_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Full Stack Developer",
    "department": "Engineering",
    "location": "Remote",
    "experience_level": "mid",
    "requirements": "Python, React, 3+ years experience",
    "description": "Join our growing engineering team..."
  }' \
  "$BASE_URL/v1/jobs")

JOB_ID=$(echo $JOB_RESPONSE | jq -r '.job_id')
echo "Created job with ID: $JOB_ID"

# 2. Get AI-powered matches
echo "Finding candidate matches..."
MATCHES=$(curl -s -X GET \
  -H "Authorization: Bearer $API_KEY" \
  "$BASE_URL/v1/match/$JOB_ID/top?limit=5&threshold=0.7")

echo "Top matches:"
echo $MATCHES | jq '.matches[] | {name: .name, score: .score, reasoning: .reasoning}'

# 3. Get job statistics
echo "Getting job statistics..."
STATS=$(curl -s -X GET \
  -H "Authorization: Bearer $API_KEY" \
  "$BASE_URL/v1/candidates/stats")

echo "Platform statistics:"
echo $STATS | jq '{total_candidates, active_jobs, recent_matches}'
```

#### **Candidate Management Workflow**
```bash
#!/bin/bash

API_KEY="bhiv_demo_api_key_2025"
BASE_URL="https://bhiv-hr-gateway-ltg0.onrender.com"

# 1. Search for candidates
echo "Searching for Python developers..."
SEARCH_RESULTS=$(curl -s -X GET \
  -H "Authorization: Bearer $API_KEY" \
  "$BASE_URL/v1/candidates/search?skills=Python&experience_min=3&limit=5")

echo "Found candidates:"
echo $SEARCH_RESULTS | jq '.candidates[] | {name: .name, skills: .technical_skills, experience: .experience_years}'

# 2. Get detailed candidate info
CANDIDATE_ID=$(echo $SEARCH_RESULTS | jq -r '.candidates[0].id')
echo "Getting details for candidate $CANDIDATE_ID..."

CANDIDATE_DETAILS=$(curl -s -X GET \
  -H "Authorization: Bearer $API_KEY" \
  "$BASE_URL/v1/candidates/$CANDIDATE_ID?include_applications=true")

echo "Candidate details:"
echo $CANDIDATE_DETAILS | jq '.candidate | {name, email, location, technical_skills}'

# 3. Bulk upload new candidates
echo "Uploading new candidates..."
BULK_UPLOAD=$(curl -s -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "candidates": [
      {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "+1-555-0104",
        "location": "Seattle, WA",
        "experience_years": 4,
        "technical_skills": "Python, Flask, PostgreSQL, Docker",
        "seniority_level": "Mid-level Developer",
        "education_level": "Bachelors"
      }
    ]
  }' \
  "$BASE_URL/v1/candidates/bulk")

echo "Bulk upload result:"
echo $BULK_UPLOAD | jq '{status, candidates_inserted, total_errors}'
```

---

## 📈 Performance Benchmarks

### **Response Time Benchmarks**
- **Simple GET requests**: <50ms average
- **Complex searches**: <200ms average
- **AI matching (single job)**: <20ms average
- **Batch AI matching**: <500ms for 10 jobs
- **Bulk candidate upload**: <1s for 50 candidates

### **Throughput Benchmarks**
- **Concurrent users**: 100+ supported
- **Requests per second**: 500+ (Gateway)
- **AI matches per minute**: 1000+
- **Database queries per second**: 2000+

### **Scalability Metrics**
- **Database connections**: 100 concurrent
- **Memory usage**: <512MB per service
- **CPU usage**: <30% under normal load
- **Storage**: Unlimited (PostgreSQL)

---

## 🔍 Testing & Validation

### **API Testing Checklist**

#### **Authentication Testing**
```bash
# Test invalid API key
curl -X GET \
  -H "Authorization: Bearer invalid_key" \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/stats
# Expected: 401 Unauthorized

# Test missing authorization header
curl -X GET \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/stats
# Expected: 401 Unauthorized

# Test valid API key
curl -X GET \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/stats
# Expected: 200 OK with statistics
```

#### **Input Validation Testing**
```bash
# Test invalid email format
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{"candidates": [{"name": "Test", "email": "invalid-email"}]}' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/bulk
# Expected: 422 Unprocessable Entity

# Test missing required fields
curl -X POST \
  -H "Authorization: Bearer bhiv_demo_api_key_2025" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Job"}' \
  https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs
# Expected: 422 Unprocessable Entity
```

#### **Rate Limiting Testing**
```bash
# Test rate limiting (run multiple times quickly)
for i in {1..70}; do
  curl -X GET \
    -H "Authorization: Bearer bhiv_demo_api_key_2025" \
    https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates/stats &
done
wait
# Expected: Some requests return 429 Too Many Requests
```

---

## 📚 Additional Resources

### **Interactive Documentation**
- **Swagger UI**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
- **ReDoc**: https://bhiv-hr-gateway-ltg0.onrender.com/redoc
- **Agent API Docs**: https://bhiv-hr-agent-nhgg.onrender.com/docs

### **Live Demo Portals**
- **HR Portal**: https://bhiv-hr-portal-u670.onrender.com/
- **Client Portal**: https://bhiv-hr-client-portal-3iod.onrender.com/
- **Candidate Portal**: https://bhiv-hr-candidate-portal-abe6.onrender.com/

### **Monitoring & Metrics**
- **Prometheus Metrics**: https://bhiv-hr-gateway-ltg0.onrender.com/metrics
- **Health Dashboard**: https://bhiv-hr-gateway-ltg0.onrender.com/health/detailed

### **Support & Contact**
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Documentation**: Complete guides in `/docs` directory
- **API Status**: https://bhiv-hr-gateway-ltg0.onrender.com/health

---

**BHIV HR Platform API Documentation v4.2.0** - Complete reference with 89 endpoints, comprehensive examples, and production-ready implementation.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: November 21, 2025 | **Total Endpoints**: 89 | **Status**: ✅ All Operational | **Uptime**: 99.9%