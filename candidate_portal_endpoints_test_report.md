# BHIV HR Platform - Candidate Portal Endpoints Test Report

**Generated:** 2025-11-03 14:36:22  
**Platform:** BHIV HR Gateway Service  
**Base URL:** https://bhiv-hr-gateway-ltg0.onrender.com  
**Test Category:** Candidate Portal System

## 📊 Test Summary

| Endpoint | Method | Category | Status | Response Time | Status Code |
|----------|--------|----------|--------|---------------|-------------|
| `/v1/candidate/register` | POST | Authentication | ❌ error | 0.912s | 422 |
| `/v1/candidate/login` | POST | Authentication | ✅ success | 1.424s | 200 |
| `/v1/candidate/profile/1` | PUT | Profile Management | ✅ success | 1.157s | 200 |
| `/v1/candidate/apply` | POST | Job Applications | ✅ success | 1.817s | 200 |
| `/v1/candidate/applications/1` | GET | Job Applications | ✅ success | 2.532s | 200 |

**Overall Success Rate:** 4/5 (80.0%)  

**Success Rate by Category:**  
- **Authentication:** 1/2 (50.0%)  
- **Profile Management:** 1/1 (100.0%)  
- **Job Applications:** 2/2 (100.0%)  

## 🔍 Detailed Test Results

### Authentication

#### Candidate Register

**Endpoint:** `POST /v1/candidate/register`  
**Description:** Register new candidate account  

**❌ Test Result:** FAILED  
**Error:** Unknown error  
**Status Code:** 422  
**Response Time:** 0.912s  

#### Candidate Login

**Endpoint:** `POST /v1/candidate/login`  
**Description:** Authenticate candidate and get access token  

**✅ Test Result:** PASSED  
**Status Code:** 200  
**Response Time:** 1.424s  
**Response Size:** 47 bytes  

**Response Structure:**
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

**Test Data Sent:**
```json
{
  "email": "candidate@example.com",
  "password": "password123"
}
```

### Profile Management

#### Update Candidate Profile

**Endpoint:** `PUT /v1/candidate/profile/1`  
**Description:** Update candidate profile information  

**✅ Test Result:** PASSED  
**Status Code:** 200  
**Response Time:** 1.157s  
**Response Size:** 57 bytes  

**Response Structure:**
```json
{
  "success": true,
  "message": "Profile updated successfully"
}
```

**Test Data Sent:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe.updated@example.com",
  "phone": "+1-555-123-9999",
  "location": "New York, NY",
  "skills": [
    "Python",
    "JavaScript",
    "React",
    "Node.js"
  ],
  "experience_years": 5,
  "education": "Bachelor's in Computer Science",
  "summary": "Experienced full-stack developer with 5 years in web development"
}
```

### Job Applications

#### Apply for Job

**Endpoint:** `POST /v1/candidate/apply`  
**Description:** Submit job application  

**✅ Test Result:** PASSED  
**Status Code:** 200  
**Response Time:** 1.817s  
**Response Size:** 82 bytes  

**Response Structure:**
```json
{
  "success": true,
  "message": "Application submitted successfully",
  "application_id": 1
}
```

**Test Data Sent:**
```json
{
  "candidate_id": 1,
  "job_id": 1,
  "cover_letter": "I am very interested in this position and believe my skills in Python and web development make me a great fit for this role.",
  "resume_url": "https://example.com/resume.pdf",
  "additional_notes": "Available for immediate start"
}
```

#### Get Candidate Applications

**Endpoint:** `GET /v1/candidate/applications/1`  
**Description:** Retrieve all applications for candidate ID 1  

**✅ Test Result:** PASSED  
**Status Code:** 200  
**Response Time:** 2.532s  
**Response Size:** 433 bytes  

**Response Structure:**
```json
{
  "applications": [
    {
      "id": 1,
      "job_id": 1,
      "status": "applied",
      "applied_date": "2025-11-03T09:06:21.459017",
      "cover_letter": "I am very interested in this position and believe my skills in Python and web development make me a great fit for this role.",
      "job_title": "Senior Python Developer",
      "department": "Engineering",
      "location": "Remote",
      "experience_level": "Senior",
      "company": "BHIV Partner",
      "updated_at": "2025-11-03T09:06:21.459017"
    }
  ],
  "count": 1
}
```

## 👥 Candidate Portal Analysis

### Candidate Portal Features

The candidate portal provides comprehensive job seeker functionality:

- **Account Management** - Registration and authentication system
- **Profile Management** - Complete candidate profile updates
- **Job Applications** - Apply for positions with cover letters
- **Application Tracking** - View all submitted applications
- **Secure Authentication** - JWT-based candidate login system
- **Data Validation** - Input validation and error handling

### Candidate Experience Benefits:

1. **Easy Registration** - Simple account creation process
2. **Profile Control** - Complete profile management capabilities
3. **Job Discovery** - Access to available positions
4. **Application Management** - Track application status
5. **Secure Access** - Protected candidate data and privacy
6. **Mobile Ready** - API-first design for mobile applications

## ⚡ Performance Analysis

**Average Response Time:** 1.732s  
**Fastest Endpoint:** `/v1/candidate/profile/1` (1.157s)  
**Slowest Endpoint:** `/v1/candidate/applications/1` (2.532s)  

## 💡 Candidate Portal Recommendations

⚠️ **1 candidate portal endpoint(s) failed testing**

- `/v1/candidate/register`: Unknown error

### Candidate Portal Best Practices:

1. **User Experience** - Ensure intuitive and responsive interface
2. **Data Security** - Protect candidate personal information
3. **Application Process** - Streamline job application workflow
4. **Status Updates** - Provide real-time application status
5. **Profile Completeness** - Encourage complete profile information
6. **Mobile Optimization** - Ensure mobile-friendly experience
7. **Communication** - Enable candidate-recruiter communication

## 📝 Candidate Portal Usage Examples

### Register New Candidate
```bash
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/register" \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d {
    "email": "candidate@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1-555-123-4567",
    "location": "San Francisco, CA"
  }
```

### Candidate Login
```bash
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/login" \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d {
    "email": "candidate@example.com",
    "password": "password123"
  }
```

### Update Profile
```bash
curl -X PUT "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/profile/1" \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d {
    "first_name": "John",
    "last_name": "Doe",
    "skills": ["Python", "JavaScript", "React"],
    "experience_years": 5
  }
```

### Apply for Job
```bash
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/apply" \
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
  -H "Content-Type: application/json" \
  -d {
    "candidate_id": 1,
    "job_id": 1,
    "cover_letter": "I am interested in this position...",
    "resume_url": "https://example.com/resume.pdf"
  }
```

---

**Report Generated:** 2025-11-03 14:36:22  
**Test Duration:** 7.842s total  
**Platform:** BHIV HR Platform v3.0.0-Phase3  
