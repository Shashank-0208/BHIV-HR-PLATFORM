# BHIV HR Platform - Complete Implementation Roadmap
## 7-Day Sprint Execution Plan

**Document Version:** 1.0  
**Last Updated:** November 6, 2025  
**Total Estimated Hours:** 32 hours (parallelizable)  
**Target Completion:** November 13, 2025

---

## Executive Summary

This document provides a complete step-by-step implementation guide for completing the BHIV HR Platform 7-day sprint. It includes:

- ✅ **4 Implementation Phases** with detailed steps
- ✅ **Clean AI Assistant Prompts** ready for your AI tool
- ✅ **Manual Deployment Steps** for Render/manual setup
- ✅ **Code snippets** and configuration examples
- ✅ **Testing procedures** and verification checklist
- ✅ **Deployment order** and timeline
- ✅ **Success metrics** and monitoring

---

## Implementation Phases Overview

### Phase 1: N8N Automation Layer (Days 1-2)
**Hours:** 8 | **Deployment:** Render (Docker)
- Deploy N8N instance
- Create email workflows
- Setup WhatsApp integration (Twilio)
- Create Telegram bot
- Add webhook endpoints to Gateway
- Test all workflows

### Phase 2: Voice Integration (Days 3-4)
**Hours:** 10 | **Deployment:** Render (Microservice)
- Setup STT service (OpenAI Whisper)
- Setup TTS service (Google Cloud)
- Create voice recording UI
- Integrate RL feedback loop
- Setup audit logging
- Test voice workflows

### Phase 3: Real-time Synchronization (Days 5-6)
**Hours:** 8 | **Deployment:** Render (Microservices)
- Add Socket.IO to Gateway
- Create state synchronizer microservice
- Setup Socket.IO clients in portals
- Test cross-portal synchronization

### Phase 4: Testing & Documentation (Day 7)
**Hours:** 6 | **Deliverable:** Complete sprint
- End-to-end testing
- Performance benchmarking
- Documentation completion
- Demo preparation

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      RENDER.COM HOSTING                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │ N8N Instance    │  │ Voice Service    │  │ State Sync      │ │
│  │ - Email         │  │ - STT (Whisper)  │  │ - Microservice  │ │
│  │ - WhatsApp      │  │ - TTS (Google)   │  │ - Sync Logic    │ │
│  │ - Telegram      │  │ - Sentiment      │  │ - Conflict Res  │ │
│  └────────┬────────┘  └─────────┬────────┘  └────────┬────────┘ │
│           │                     │                    │          │
│  ┌────────▼─────────────────────▼────────────────────▼────────┐ │
│  │                  API Gateway (FastAPI)                      │ │
│  │  - 79 REST endpoints                                        │ │
│  │  - Socket.IO server (WebSocket)                            │ │
│  │  - Webhook handlers                                         │ │
│  │  - RL integration endpoints                                 │ │
│  └────────┬─────────────────────────────────────────┬─────────┘ │
│           │                                         │            │
│  ┌────────▼────────┐  ┌─────────────┐  ┌──────────▼────────┐  │
│  │ Candidate       │  │ HR Portal   │  │ Client Portal     │  │
│  │ Portal          │  │ (Streamlit) │  │ (Streamlit)       │  │
│  │ (Streamlit)     │  │             │  │                   │  │
│  │ - Socket.IO     │  │ - Socket.IO │  │ - Socket.IO       │  │
│  │ - Voice UI      │  │ - Real-time │  │ - Real-time       │  │
│  │ - Real-time     │  │   updates   │  │   updates         │  │
│  └────────────────┘  └─────────────┘  └───────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         PostgreSQL Database (Primary)                     │  │
│  │  - Main schema (candidates, jobs, etc)                   │  │
│  │  - Voice interactions table                              │  │
│  │  - State snapshots & transitions                         │  │
│  │  - Audit logs                                            │  │
│  │  - Feedback rewards                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         PostgreSQL Database (N8N)                         │  │
│  │  - Workflow definitions                                  │  │
│  │  - Execution history                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

External Integrations:
├─ OpenAI (Whisper API for STT)
├─ Google Cloud (Text-to-Speech)
├─ Twilio (WhatsApp messaging)
├─ Telegram Bot API
└─ RL Agent (Ishan's system - optional for Phase 2)
```

---

## Phase 1: N8N Automation Layer - Detailed Steps

### Step 1.1: N8N Deployment (Manual - 15 min)

**Location:** Render.com

**Manual Steps:**
1. Go to Render Dashboard (render.com)
2. Click "New +" → "Web Service"
3. Select Docker runtime
4. Repository: BHIV-HR-PLATFORM (if forked) or Docker image: n8n:latest
5. Configuration:
   - Service Name: `bhiv-n8n`
   - Plan: Pro ($12/month)
   - Region: Select closest to your location
6. Environment Variables:
   ```
   N8N_USER_MANAGEMENT_DISABLED=true
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=SuperSecure!Pass@123
   DATABASE_URL=postgresql://user:pass@host:5432/n8n_db
   N8N_HOST=bhiv-n8n.onrender.com
   N8N_PROTOCOL=https
   WEBHOOK_URL=https://bhiv-n8n.onrender.com
   NODE_ENV=production
   ```
7. Click "Create Web Service"
8. Wait for deployment (5-10 minutes)
9. Verify: `curl https://bhiv-n8n.onrender.com/health`

**AI Assistant Prompt:**

```
TASK: Create N8N Deployment Configuration for Render

Generate complete setup guide and configuration files for N8N on Render.

REQUIREMENTS:
- Docker image: n8n:latest
- Separate PostgreSQL database for N8N workflows
- Basic authentication (username: admin)
- Custom domain: bhiv-n8n.onrender.com
- HTTPS/SSL configuration
- Health check setup
- Environment variable security

DELIVERABLES:
1. render.yaml Blueprint (if using infrastructure-as-code)
2. Environment variables checklist (.env.example)
3. PostgreSQL initialization script
4. Docker compose file (for local testing)
5. Post-deployment verification commands
6. Troubleshooting guide
7. Backup and recovery strategy

CONSTRAINTS:
- Free tier compatible setup
- No credit card required for testing phase
- Scalable architecture for production
```

---

### Step 1.2: Email Workflow Setup (Manual + AI - 30 min)

**Location:** N8N UI at https://bhiv-n8n.onrender.com

**Manual Steps:**
1. Login to N8N (admin / your-password)
2. Click "New Workflow"
3. Name: "Email Notifications"
4. Add HTTP Webhook trigger node:
   - Method: POST
   - Path: `/webhook/email-trigger`
5. Add conditional node (switch by event type)
6. Add Gmail Send Email node:
   - Authenticate with Gmail App Password
   - Create 4 branches (one per event)
7. Add database logging node
8. Activate workflow

**AI Assistant Prompt:**

```
TASK: Create Complete N8N Email Notification Workflow

Build production-ready email automation workflow.

WORKFLOW NAME: Email Notifications

TRIGGER: HTTP POST to /webhook/email-trigger

PAYLOAD SCHEMA:
{
  "event": "application_received|shortlisted|interview_scheduled|offer_sent",
  "recipient_email": "candidate@example.com",
  "recipient_name": "John Doe",
  "subject": "Email subject",
  "body": "Email body",
  "variables": {
    "job_title": "string",
    "company": "string",
    "date": "string",
    "time": "string"
  }
}

EMAIL TEMPLATES (Create 4 branches):

1. Application Received
   Subject: "Thank you for applying to {job_title} at {company}"
   Body: "Hi {name}, we've received your application and will review it shortly."

2. Candidate Shortlisted
   Subject: "Congratulations! You're shortlisted for {job_title}"
   Body: "Hi {name}, great news! We'd like to move forward with your application."

3. Interview Scheduled
   Subject: "Your interview is scheduled for {date} at {time}"
   Body: "Hi {name}, your interview for {job_title} is on {date} at {time}."

4. Offer Received
   Subject: "Exciting news! Job offer for {job_title}"
   Body: "Hi {name}, we're pleased to offer you the position of {job_title}."

N8N WORKFLOW STRUCTURE:

1. Webhook Trigger (HTTP POST)
2. Conditional Router (switch on "event" field)
   ├─ Branch 1: application_received
   ├─ Branch 2: shortlisted
   ├─ Branch 3: interview_scheduled
   └─ Branch 4: offer_sent
3. Email Template Formatter (per branch)
4. Gmail Send Email node (per branch)
5. Database Logger (log all sends)
6. Error Handler (catch failures)

GMAIL SETUP:
- Enable 2FA on Gmail account
- Create App Password (not regular password)
- Use SMTP: smtp.gmail.com:587
- Store credentials in N8N secrets

DELIVERABLES:
1. Complete N8N workflow JSON (export)
2. Email template library (HTML/plain text)
3. Test payloads for each event type
4. Gmail App Password setup guide
5. Webhook testing script (curl commands)
6. Monitoring dashboard for email success rate
```

---

### Step 1.3: WhatsApp Integration (Manual + AI - 45 min)

**Location:** Twilio + N8N

**Manual Steps - Twilio Setup:**
1. Go to twilio.com/console
2. Create project (or use existing)
3. Get Account SID and Auth Token
4. Enable WhatsApp:
   - Go to Messaging → WhatsApp
   - Get sandbox phone number
   - Write down: SID, Token, Phone Number
5. Test with your personal WhatsApp:
   - Message the sandbox number with: `join <code>`

**Manual Steps - N8N:**
1. In N8N, create new workflow: "WhatsApp Notifications"
2. Add HTTP Webhook trigger
3. Add Twilio Send WhatsApp node:
   - Account SID: (from Twilio)
   - Auth Token: (from Twilio)
   - From Number: (Twilio sandbox number)
   - To Number: (from webhook payload)
4. Add message formatter with template variables
5. Add delivery status logger
6. Test with sample message

**AI Assistant Prompt:**

```
TASK: Setup Twilio WhatsApp Messaging Integration in N8N

Configure WhatsApp notifications via Twilio.

TWILIO CONFIGURATION:
1. Create Twilio account (twilio.com)
2. Verify your personal phone (for testing)
3. Enable WhatsApp in console
4. Get:
   - Account SID: AC...
   - Auth Token: ...
   - Sandbox Number: +1234567890
5. Share sandbox number with candidate (ask them to message "join ...")

WORKFLOW: WhatsApp Notifications

WEBHOOK PAYLOAD:
{
  "event": "status_update|interview_reminder|offer_notification",
  "phone_number": "+91XXXXXXXXXX",
  "candidate_name": "John Doe",
  "variables": {
    "status": "shortlisted",
    "job_title": "Senior Developer",
    "date": "2025-11-08",
    "time": "2:00 PM"
  }
}

MESSAGE TEMPLATES:

1. Status Update
   "Hi {name}! Your application for {job_title} is now {status}. "
   "Check your dashboard for more details."

2. Interview Reminder (24h before)
   "Reminder: Your interview for {job_title} is tomorrow at {time}. "
   "Join here: {interview_link}"

3. Offer Notification
   "Congratulations {name}! 🎉 We're offering you the position of "
   "{job_title}. Check your email for details."

N8N WORKFLOW:
1. Webhook Trigger (POST)
2. Message Template Formatter (conditional per event)
3. Phone Number Validator
4. Twilio Send WhatsApp
5. Delivery Status Logger
6. Error Notification (to admin if failed)

TESTING:
1. Add your phone to sandbox
2. Send test webhook:
   curl -X POST https://bhiv-n8n.onrender.com/webhook/whatsapp-trigger \
   -H "Content-Type: application/json" \
   -d '{
     "event": "status_update",
     "phone_number": "+919999999999",
     "candidate_name": "John",
     "variables": {"status": "shortlisted"}
   }'
3. Verify message received on WhatsApp

DELIVERABLES:
1. Complete N8N workflow JSON
2. Twilio account setup guide
3. Message template library
4. Test scenarios and results
5. Production deployment checklist (enable for real numbers)
```

---

### Step 1.4: Telegram Bot Setup (Manual + AI - 20 min)

**Location:** Telegram BotFather + N8N

**Manual Steps:**
1. Open Telegram and search for @BotFather
2. Send `/newbot`
3. Follow prompts:
   - "What should your bot be called?" → BHIV HR Bot
   - "Give your bot a username." → bhiv_hr_bot (must end with _bot)
4. Copy the token (keep it secret!)
5. In N8N, create workflow: "Telegram Bot Handler"
6. Add Telegram node, paste token
7. Create command handlers

**AI Assistant Prompt:**

```
TASK: Create Telegram Bot Workflow in N8N

Build interactive Telegram bot for candidate communication.

BOT SETUP (BotFather):
1. Message @BotFather on Telegram
2. Send /newbot
3. Bot name: "BHIV HR Bot"
4. Bot username: "bhiv_hr_bot" (unique, must end with _bot)
5. Copy token (save in N8N secrets)

TELEGRAM COMMANDS:

/start
  Response: "Welcome to BHIV HR Bot! 🤖\n"
           "Available commands:\n"
           "/status - Check application status\n"
           "/interview - View interview details\n"
           "/feedback - Submit feedback\n"
           "/reschedule - Request reschedule\n"
           "/help - Show help"

/status
  Action: Query GET /v1/candidate/applications/{user_id}
  Response: "Your Applications:\n"
           "1. Senior Developer at TechCorp - Status: Shortlisted ✅\n"
           "2. DevOps Engineer at StartupXYZ - Status: Pending ⏳"

/interview
  Action: Query GET /v1/interviews/{user_id}
  Response: "📅 Interview scheduled!\n"
           "Date: Nov 8, 2025\n"
           "Time: 2:00 PM IST\n"
           "Interviewer: John Smith\n"
           "Link: https://meet.google.com/..."

/feedback
  Action: Start feedback collection flow
  Response: "Please share your feedback about your interview:\n"
           "1️⃣ Send text message\n"
           "2️⃣ Send voice message\n"
           "3️⃣ Choose from quick replies"

/reschedule
  Action: Show available time slots
  Response: "Available slots:\n"
           "1. Nov 9, 10:00 AM\n"
           "2. Nov 9, 2:00 PM\n"
           "3. Nov 10, 11:00 AM\n"
           "Reply with 1, 2, or 3"

N8N WORKFLOW STRUCTURE:
1. Telegram Webhook Trigger
2. Command Router (switch on /command)
3. API Query nodes (one per command)
4. Message Formatter
5. Telegram Send Message
6. Error Handler

INTEGRATION POINTS:
- /status → GET /v1/candidate/applications/{user_id}
- /interview → GET /v1/interviews/{user_id}
- /feedback → POST /v1/feedback/submit
- /reschedule → PUT /v1/interviews/{id}/reschedule

USER ID MAPPING:
- Store Telegram user_id with candidate_id in database
- Query mapping table when command received
- Create entry on first /start command

SECURITY:
- Verify Telegram bot token
- Add request signing
- Rate limit per user (10 req/minute)
- Log all commands

DELIVERABLES:
1. N8N workflow JSON
2. BotFather setup guide (screenshots)
3. Command handler definitions
4. API integration mapping
5. User ID mapping database schema
6. Test conversation scenarios
```

---

### Step 1.5: Gateway Webhook Endpoints (Code - 45 min)

**Location:** GitHub repo, file: `gateway/main.py`

**Manual Steps:**
1. Clone repository locally:
   ```bash
   git clone https://github.com/Shashank-0208/BHIV-HR-PLATFORM.git
   cd BHIV-HR-PLATFORM/gateway
   ```

2. Add new file `webhook_handlers.py`:
   ```python
   from fastapi import APIRouter, Request, HTTPException
   from fastapi.responses import JSONResponse
   import aiohttp
   import hmac
   import hashlib
   import json
   from datetime import datetime
   
   router = APIRouter(prefix="/webhooks", tags=["webhooks"])
   
   # Configuration
   N8N_BASE_URL = "https://bhiv-n8n.onrender.com"
   WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-secret-key")
   
   def verify_signature(payload: str, signature: str) -> bool:
       """Verify webhook signature using HMAC-SHA256"""
       expected = hmac.new(
           WEBHOOK_SECRET.encode(),
           payload.encode(),
           hashlib.sha256
       ).hexdigest()
       return hmac.compare_digest(signature, expected)
   
   @router.post("/candidate-applied")
   async def webhook_candidate_applied(request: Request):
       """
       Triggered when candidate applies for a job
       """
       try:
           payload = await request.json()
           
           # Validate required fields
           required = ["candidate_id", "job_id", "email", "name"]
           for field in required:
               if field not in payload:
                   raise HTTPException(status_code=400, detail=f"Missing: {field}")
           
           # Send to N8N for email notification
           n8n_payload = {
               "event": "application_received",
               "recipient_email": payload["email"],
               "recipient_name": payload["name"],
               "variables": {
                   "job_title": payload.get("job_title", "Unknown"),
                   "company": payload.get("company", "Our Company")
               }
           }
           
           async with aiohttp.ClientSession() as session:
               async with session.post(
                   f"{N8N_BASE_URL}/webhook/email-trigger",
                   json=n8n_payload,
                   timeout=aiohttp.ClientTimeout(total=10)
               ) as response:
                   if response.status != 200:
                       logger.error(f"N8N request failed: {response.status}")
           
           # Also send WhatsApp notification
           whatsapp_payload = {
               "event": "application_received",
               "phone_number": payload.get("phone"),
               "candidate_name": payload["name"],
               "variables": {"job_title": payload.get("job_title")}
           }
           
           async with aiohttp.ClientSession() as session:
               await session.post(
                   f"{N8N_BASE_URL}/webhook/whatsapp-trigger",
                   json=whatsapp_payload
               )
           
           # Log to database
           await db.webhook_logs.insert_one({
               "event": "candidate_applied",
               "payload": payload,
               "timestamp": datetime.now(),
               "status": "success"
           })
           
           return {"status": "webhook_processed"}
       
       except Exception as e:
           logger.error(f"Webhook error: {e}")
           await db.webhook_logs.insert_one({
               "event": "candidate_applied",
               "error": str(e),
               "timestamp": datetime.now(),
               "status": "failed"
           })
           raise HTTPException(status_code=500, detail="Webhook processing failed")
   
   # Repeat for other events...
   @router.post("/candidate-shortlisted")
   async def webhook_candidate_shortlisted(request: Request):
       """When HR shortlists a candidate"""
       payload = await request.json()
       # Similar logic...
   
   @router.post("/interview-scheduled")
   async def webhook_interview_scheduled(request: Request):
       """When interview is scheduled"""
       payload = await request.json()
       # Similar logic...
   
   @router.post("/feedback-received")
   async def webhook_feedback_received(request: Request):
       """When feedback is submitted"""
       payload = await request.json()
       # Similar logic...
   ```

3. Update `main.py` to include webhook router:
   ```python
   from webhook_handlers import router as webhook_router
   
   app.include_router(webhook_router)
   ```

4. Test locally:
   ```bash
   python -m uvicorn main:app --reload
   
   # In another terminal
   curl -X POST http://localhost:8000/webhooks/candidate-applied \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": "123",
       "job_id": "456",
       "email": "test@example.com",
       "name": "John Doe",
       "phone": "+919999999999",
       "job_title": "Senior Developer"
     }'
   ```

5. Deploy to Render:
   ```bash
   git add .
   git commit -m "Add N8N webhook endpoints"
   git push origin main
   ```

**AI Assistant Prompt:**

```
TASK: Create Production-Ready Webhook Endpoints for N8N

Implement webhook handlers in FastAPI Gateway for N8N integration.

WEBHOOK ENDPOINTS:

1. POST /webhooks/candidate-applied
2. POST /webhooks/candidate-shortlisted
3. POST /webhooks/interview-scheduled
4. POST /webhooks/feedback-received

REQUIREMENTS FOR EACH ENDPOINT:
- Validate required fields
- Verify webhook signature (HMAC-SHA256)
- Forward to N8N for workflow trigger
- Log all requests to database
- Handle errors gracefully
- Return appropriate HTTP status

SECURITY:
- HMAC signature verification
- Timestamp validation (max 5 min old)
- IP whitelist (N8N server only)
- Request/response logging
- Rate limiting

ERROR HANDLING:
- Field validation (400 Bad Request)
- N8N timeout (retry logic)
- Database error (queue for retry)
- Invalid signature (403 Forbidden)

IMPLEMENTATION PATTERN:
1. Receive webhook POST
2. Validate payload
3. Verify signature
4. Extract data
5. Forward to N8N
6. Log to database
7. Return success/error

DELIVERABLES:
1. webhook_handlers.py module
2. Endpoint implementations
3. Error handling strategy
4. Logging configuration
5. Testing script
6. Deployment checklist
```

---

### Step 1.6: N8N Workflow Testing (Manual - 60 min)

**Test Scenarios:**

1. **Email Workflow Test** (10 min)
   ```bash
   curl -X POST https://bhiv-n8n.onrender.com/webhook/email-trigger \
     -H "Content-Type: application/json" \
     -d '{
       "event": "application_received",
       "recipient_email": "youremail@gmail.com",
       "recipient_name": "Test User",
       "variables": {
         "job_title": "Senior Developer",
         "company": "TechCorp"
       }
     }'
   ```
   ✅ Check: Email received in inbox within 2 seconds

2. **WhatsApp Workflow Test** (10 min)
   - Use WhatsApp number registered with Twilio
   - Send webhook with your phone number
   - ✅ Check: Message received on WhatsApp

3. **Telegram Bot Test** (10 min)
   - Add @bhiv_hr_bot on Telegram
   - Send `/status` command
   - ✅ Check: Bot responds with status

4. **Error Handling Test** (10 min)
   - Send invalid email format
   - Send payload with missing fields
   - ✅ Check: Graceful error handling

5. **Load Test** (15 min)
   ```bash
   # Send 50 concurrent requests
   for i in {1..50}; do
     curl -X POST https://bhiv-gateway.com/webhooks/candidate-applied \
       -H "Content-Type: application/json" \
       -d "{...payload...}" &
   done
   wait
   ```
   ✅ Check: All requests processed successfully

6. **Logging Verification** (5 min)
   - Check database for webhook logs
   - Verify all events logged
   - ✅ Check: Complete audit trail

---

## Phase 2: Voice Integration

[**See implementation_guide.md for detailed steps on:**
- Voice Service (STT) Setup
- TTS Service Setup
- Voice Recording UI
- RL Loop Integration
- Audit Logging
- Testing
]

---

## Phase 3: Real-time Synchronization

[**See implementation_guide.md for detailed steps on:**
- Socket.IO Integration
- Agent-State Synchronizer
- Socket.IO Clients in Portals
- Testing & Verification
]

---

## Phase 4: Testing & Documentation

### Complete End-to-End Test Scenario

**Time:** 30 minutes

**Scenario:** Candidate applies → HR shortlists → Client schedules → Candidate gets interview

1. **Candidate applies for job** (5 min)
   - Open Candidate Portal
   - Browse jobs
   - Click "Apply" for Senior Developer role
   - Submit application
   - ✅ Verify: Email notification received

2. **HR reviews and shortlists** (5 min)
   - Open HR Portal
   - See new application in queue
   - Click "Shortlist"
   - ✅ Verify: WhatsApp sent to candidate

3. **Client schedules interview** (5 min)
   - Open Client Portal
   - See shortlisted candidate
   - Click "Schedule Interview"
   - Select date/time
   - ✅ Verify: Telegram reminder sent

4. **Candidate gets notifications** (5 min)
   - Check Candidate Portal
   - ✅ See interview scheduled
   - ✅ Check Telegram for reminder
   - ✅ Check email for confirmation

5. **Verify real-time sync** (5 min)
   - Open HR, Client, Candidate portals side-by-side
   - Update status in HR
   - ✅ See instant update in Client and Candidate
   - ✅ No manual refresh needed

6. **Check all logs** (5 min)
   - Query webhook logs
   - Query voice interaction logs
   - Query state transition logs
   - ✅ Verify complete audit trail

---

## Deployment Checklist

### Pre-Deployment
- [ ] All code pushed to GitHub
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Security review completed

### Deployment Order
1. [ ] N8N Service → Render
2. [ ] Voice Service → Render
3. [ ] State Sync Service → Render
4. [ ] Gateway Updates → Render
5. [ ] Portal Updates → Render

### Post-Deployment Verification
```bash
# Health checks
curl https://bhiv-n8n.onrender.com/health
curl https://bhiv-voice-service.onrender.com/health
curl https://bhiv-state-sync.onrender.com/health
curl https://bhiv-hr-gateway.onrender.com/health

# Database verification
psql $DATABASE_URL -c "SELECT COUNT(*) FROM candidates;"

# Service connectivity
curl https://bhiv-hr-gateway.onrender.com/v1/health

# Monitor logs
tail -f /var/logs/service.log
```

---

## Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Email send latency | <1s | Timestamp logs |
| WhatsApp delivery | <3s | Message timestamps |
| STT accuracy | 85%+ | Test transcriptions |
| Real-time sync latency | <100ms | Event logs |
| System uptime | 99.9% | Monitoring dashboard |
| User satisfaction | >4.5/5 | Feedback survey |

---

## Troubleshooting Guide

### Common Issues & Solutions

**N8N not starting:**
- Check Docker image is correct: `n8n:latest`
- Verify PostgreSQL connection string
- Check environment variables for typos

**Email not sending:**
- Verify Gmail App Password (not regular password)
- Check SMTP settings: smtp.gmail.com:587
- Verify recipient email is valid

**WhatsApp message failed:**
- Ensure Twilio credentials are correct
- Check phone number format: +country_code
- Verify WhatsApp sandbox is enabled

**WebSocket connection failing:**
- Check JWT token validity
- Verify Socket.IO CORS settings
- Check firewall/proxy settings

**Database connection errors:**
- Verify DATABASE_URL environment variable
- Check PostgreSQL server is running
- Verify network connectivity to database

---

## Monitoring & Maintenance

### Daily Checks (5 min)
- [ ] All services responding to /health
- [ ] No unusual error logs
- [ ] Database queries responding normally
- [ ] WebSocket connections stable

### Weekly Checks (30 min)
- [ ] Review workflow execution logs
- [ ] Check system resource usage
- [ ] Verify backup completion
- [ ] Update any dependencies with security patches

### Monthly Checks (1 hour)
- [ ] Load test under peak conditions
- [ ] Review and optimize slow queries
- [ ] Audit user access logs
- [ ] Update documentation

---

## Additional Resources

### Learning Materials
- **N8N:** https://docs.n8n.io
- **FastAPI:** https://fastapi.tiangolo.com
- **Socket.IO:** https://socket.io/docs/v4
- **OpenAI Whisper:** https://platform.openai.com/docs/guides/speech-to-text

### Tools & Services
- **Render:** https://render.com
- **Twilio:** https://www.twilio.com
- **Google Cloud TTS:** https://cloud.google.com/text-to-speech
- **Telegram Bot API:** https://core.telegram.org/bots/api

### Support Contacts
- **Technical Issues:** GitHub Issues or email
- **N8N Support:** N8N Slack Community
- **Render Support:** Render Help Center
- **Twilio Support:** Twilio Help Center

---

**Document Status:** Ready for Implementation  
**Last Updated:** November 6, 2025  
**Next Review:** November 13, 2025 (Post-Sprint)