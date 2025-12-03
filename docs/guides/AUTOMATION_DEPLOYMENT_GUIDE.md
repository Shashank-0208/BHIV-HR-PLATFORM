# 🚀 BHIV HR Platform - Automation Deployment Guide

## ✅ Automation Fixes Completed

### 🔧 Issues Fixed

1. **Correct LangGraph Endpoints** ✅
   - Fixed job posting automation: `/automation/trigger-workflow` → `/tools/send-notification`
   - Fixed candidate approval: Uses `/test/send-automated-sequence` with proper headers
   - Removed hardcoded URLs, now uses dynamic `LANGGRAPH_SERVICE_URL`

2. **Security Improvements** ✅
   - Removed exposed production credentials from `config/.env.render`
   - Created secure template: `config/render-secure.env`
   - Updated credential validation in communication manager
   - Enhanced `.gitignore` to prevent future credential exposure

3. **Dynamic Configuration** ✅
   - Client portal now imports `LANGGRAPH_SERVICE_URL` from config
   - LangGraph config uses environment variable placeholders
   - Proper error handling for missing environment variables

## 📋 Deployment Steps

### 1. Render Dashboard Configuration

**For each service, add these environment variables in Render dashboard:**

```bash
# Core Configuration
DATABASE_URL=<your_postgresql_url>
API_KEY_SECRET=<your_api_key>
JWT_SECRET_KEY=<your_jwt_secret>
CANDIDATE_JWT_SECRET_KEY=<your_candidate_jwt_secret>

# Service URLs (Production)
GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-ltg0.onrender.com
LANGGRAPH_SERVICE_URL=https://bhiv-hr-langgraph.onrender.com
AGENT_SERVICE_URL=https://bhiv-hr-agent-nhgg.onrender.com

# Email & WhatsApp Automation
TWILIO_ACCOUNT_SID=<your_twilio_sid>
TWILIO_AUTH_TOKEN=<your_twilio_token>
TWILIO_WHATSAPP_NUMBER=<your_whatsapp_number>
GMAIL_EMAIL=<your_gmail_email>
GMAIL_APP_PASSWORD=<your_gmail_app_password>

# AI Configuration
GEMINI_API_KEY=<your_gemini_key>
```

### 2. Service-Specific Configuration

**Client Portal:**
- Requires: `LANGGRAPH_SERVICE_URL` for automation
- Automation endpoints: `/tools/send-notification`, `/test/send-automated-sequence`

**LangGraph Service:**
- Requires: All communication credentials for email/WhatsApp
- Validates credentials on startup
- Falls back to mock mode if credentials missing

### 3. Automation Features

**Email Automation** ✅
- Job posting notifications to HR
- Candidate approval/rejection emails
- Interview scheduling with HTML templates
- Professional email formatting

**WhatsApp Automation** ✅
- Interactive buttons for candidate responses
- Automated sequences for different workflow stages
- Phone number normalization for Indian numbers
- Real-time status updates

## 🔍 Testing Automation

### Test Email Automation
```bash
curl -X POST "https://bhiv-hr-langgraph.onrender.com/test/send-email" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "test@example.com",
    "subject": "Test Email",
    "message": "Test message from BHIV HR"
  }'
```

### Test WhatsApp Automation
```bash
curl -X POST "https://bhiv-hr-langgraph.onrender.com/test/send-whatsapp" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+919284967526",
    "message": "Test WhatsApp from BHIV HR"
  }'
```

### Test Automated Sequence
```bash
curl -X POST "https://bhiv-hr-langgraph.onrender.com/test/send-automated-sequence" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "candidate_phone": "+919284967526",
    "job_title": "Software Engineer",
    "sequence_type": "interview_scheduled"
  }'
```

## 📊 Automation Endpoints Available

### LangGraph Service (9 endpoints total)
- `POST /tools/send-notification` - Multi-channel notifications
- `POST /test/send-automated-sequence` - Automated email/WhatsApp sequences
- `POST /test/send-email` - Email testing
- `POST /test/send-whatsapp` - WhatsApp testing
- `GET /workflows/stats` - Workflow statistics
- `POST /workflows/application/start` - Start AI workflows
- `GET /workflows/{id}/status` - Workflow status
- `GET /workflows` - List workflows
- `GET /health` - Health check

## 🔒 Security Notes

1. **Never commit credentials** to version control
2. **Use Render dashboard** environment variables only
3. **Rotate credentials** regularly
4. **Monitor automation logs** for security issues
5. **Validate all inputs** in automation endpoints

## 🎯 Automation Status

- ✅ Email automation: **OPERATIONAL**
- ✅ WhatsApp automation: **OPERATIONAL**
- ✅ Job posting notifications: **FIXED**
- ✅ Candidate approval automation: **FIXED**
- ✅ Dynamic URL configuration: **IMPLEMENTED**
- ✅ Security improvements: **COMPLETED**
- ❌ N8N workflows: **SKIPPED** (as requested)
- ❌ Telegram automation: **SKIPPED** (as requested)

## 📞 Support

For automation issues:
1. Check Render service logs
2. Verify environment variables are set
3. Test individual endpoints first
4. Check credential validity
5. Monitor communication service status

**Automation is now production-ready with proper security and dynamic configuration!** 🚀