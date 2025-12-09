1. **BHIV HR Platform API Gateway**
1. 
**&nbsp;4.2.0** 

**OAS 3.1**

**/openapi.json**

**Enterprise HR Platform with Advanced Security Features**







Authentication





POST

/auth/2fa/setup

Setup 2Fa







POST

/auth/2fa/verify

Verify 2Fa







POST

/auth/login

Login With 2Fa





GET

/auth/2fa/status/{user\_id}

Get 2Fa Status





AI Integration





POST

/api/v1/ai/test-communication

Test Communication System







POST

/api/v1/ai/gemini/analyze

Analyze With Gemini





LangGraph Workflows





POST

/api/v1/workflow/trigger

Trigger Workflow





GET

/api/v1/workflow/status/{workflow\_id}

Get Workflow Status





GET

/api/v1/workflow/list

List Workflows





GET

/api/v1/workflow/health

Check Langgraph Health





POST

/api/v1/webhooks/candidate-applied

Webhook Candidate Applied





POST

/api/v1/webhooks/candidate-shortlisted

Webhook Candidate Shortlisted





POST

/api/v1/webhooks/interview-scheduled

Webhook Interview Scheduled



RL + Feedback Agent





POST

/api/v1/rl/predict

Rl Predict Match







POST

/api/v1/rl/feedback

Submit Rl Feedback







GET

/api/v1/rl/analytics

Get Rl Analytics







GET

/api/v1/rl/performance

Get Rl Performance





Monitoring





GET

/metrics

Get Prometheus Metrics





GET

/health/detailed

Detailed Health Check





GET

/metrics/dashboard

Metrics Dashboard



Core API Endpoints





GET

/openapi.json

Get Openapi





GET

/docs

Get Docs





GET

/

Read Root





GET

/health

Health Check





GET

/v1/test-candidates

Test Candidates Db





Job Management





GET

/v1/jobs

List Jobs







POST

/v1/jobs

Create Job





Candidate Management





GET

/v1/candidates

Get All Candidates







GET

/v1/candidates/search

Search Candidates







GET

/v1/candidates/job/{job\_id}

Get Candidates By Job







GET

/v1/candidates/{candidate\_id}

Get Candidate By Id







POST

/v1/candidates/bulk

Bulk Upload Candidates





Analytics \& Statistics





GET

/v1/candidates/stats

Get Candidate Stats







GET

/v1/database/schema

Get Database Schema







GET

/v1/reports/job/{job\_id}/export.csv

Export Job Report





AI Matching Engine





GET

/v1/match/{job\_id}/top

Get Top Matches







POST

/v1/match/batch

Batch Match Jobs





Assessment \& Workflow





GET

/v1/feedback

Get All Feedback







POST

/v1/feedback

Submit Feedback







GET

/v1/interviews

Get Interviews







POST

/v1/interviews

Schedule Interview







GET

/v1/offers

Get All Offers







POST

/v1/offers

Create Job Offer





Client Portal API





POST

/v1/client/register

Client Register





POST

/v1/client/login

Client Login



Security Testing





GET

/v1/security/rate-limit-status

Check Rate Limit Status







GET

/v1/security/blocked-ips

View Blocked Ips







POST

/v1/security/test-input-validation

Test Input Validation







POST

/v1/security/validate-email

Validate Email







POST

/v1/security/test-email-validation

Test Email Validation







POST

/v1/security/validate-phone

Validate Phone







POST

/v1/security/test-phone-validation

Test Phone Validation







GET

/v1/security/test-headers

Test Security Headers







GET

/v1/security/security-headers-test

Test Security Headers Legacy







POST

/v1/security/penetration-test

Penetration Test







GET

/v1/security/test-auth

Test Authentication







GET

/v1/security/penetration-test-endpoints

Penetration Test Endpoints





CSP Management





POST

/v1/security/csp-report

Csp Violation Reporting







GET

/v1/security/csp-violations

View Csp Violations







GET

/v1/security/csp-policies

Current Csp Policies







POST

/v1/security/test-csp-policy

Test Csp Policy





Two-Factor Authentication





POST

/v1/auth/2fa/setup

Setup 2Fa







POST

/v1/auth/2fa/verify

Verify 2Fa







POST

/v1/auth/2fa/login

Login 2Fa







GET

/v1/auth/2fa/status/{user\_id}

Get 2Fa Status Auth







POST

/v1/auth/2fa/disable

Disable 2Fa Auth







POST

/v1/auth/2fa/backup-codes

Generate Backup Codes Auth







POST

/v1/auth/2fa/test-token

Test 2Fa Token Auth







GET

/v1/auth/2fa/qr/{user\_id}

Get Qr Code





Password Management





POST

/v1/auth/password/validate

Validate Password







GET

/v1/auth/password/generate

Generate Password







GET

/v1/auth/password/policy

Get Password Policy Auth







POST

/v1/auth/password/change

Change Password Auth







POST

/v1/auth/password/strength

Test Password Strength







GET

/v1/auth/password/security-tips

Get Security Tips





Candidate Portal





POST

/v1/candidate/register

Candidate Register





POST

/v1/candidate/login

Candidate Login





PUT

/v1/candidate/profile/{candidate\_id}

Update Candidate Profile







POST

/v1/candidate/apply

Apply For Job







GET

/v1/candidate/applications/{candidate\_id}

Get Candidate Applications,

**2. BHIV AI Matching Engine**

 **3.0.0** 

**OAS 3.1**

**/openapi.json**

**Advanced AI-Powered Semantic Candidate Matching Service**







Core API Endpoints

Service health and system information







GET

/

AI Service Information





GET

/health

Health Check



AI Matching Engine

Semantic candidate matching and scoring







POST

/match

AI-Powered Candidate Matching







POST

/batch-match

Batch AI Matching for Multiple Jobs





Candidate Analysis

Detailed candidate profile analysis







GET

/analyze/{candidate\_id}

Detailed Candidate Analysis





System Diagnostics

Database connectivity and testing







GET

/test-db

Database Connectivity Test





**3.BHIV LangGraph Orchestrator**

 **1.0.0** 

**OAS 3.1**

**/openapi.json**

**AI-driven workflow orchestration for BHIV HR Platform with API Key Authentication**







RL + Feedback Agent





POST

/rl/predict

Rl Predict Match







POST

/rl/feedback

Submit Rl Feedback







GET

/rl/analytics

Get Rl Analytics







GET

/rl/performance/{model\_version}

Get Rl Performance





GET

/rl/history/{candidate\_id}

Get Candidate Rl History





POST

/rl/retrain

Trigger Rl Retrain





GET

/rl/performance

Get Rl Performance







POST

/rl/start-monitoring

Start Rl Monitoring





Core API Endpoints





GET

/

Read Root





GET

/health

Health Check



Workflow Management





POST

/workflows/application/start

Start Application Workflow







POST

/workflows/{workflow\_id}/resume

Resume Workflow





Workflow Monitoring





GET

/workflows/{workflow\_id}/status

Get Workflow Status







GET

/workflows

List Workflows







GET

/workflows/stats

Get Workflow Stats





Communication Tools





POST

/tools/send-notification

Send Notification







POST

/test/send-email

Test Send Email







POST

/test/send-whatsapp

Test Send Whatsapp







POST

/test/send-telegram

Test Send Telegram







POST

/test/send-whatsapp-buttons

Test Send Whatsapp Buttons







POST

/test/send-automated-sequence

Test Send Automated Sequence







POST

/automation/trigger-workflow

Trigger Workflow Automation







POST

/automation/bulk-notifications

Send Bulk Notifications







POST

/webhook/whatsapp

Whatsapp Webhook





System Diagnostics





GET

/test-integration

Test Integration

