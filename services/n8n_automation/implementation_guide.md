# BHIV HR Platform - Implementation Execution Guide
## AI Assistant Prompts & Manual Deployment Steps

**Last Updated:** November 6, 2025  
**Sprint Status:** Implementation Phase  
**Target Completion:** 7 Days

---

## Quick Reference: Implementation Timeline

| Phase | Component | Days | Hours | Status |
|-------|-----------|------|-------|--------|
| **1** | N8N Automation | 1-2 | 8 | 🟡 Ready |
| **2** | Voice Integration | 3-4 | 10 | 🟡 Ready |
| **3** | Real-time Sync | 5-6 | 8 | 🟡 Ready |
| **4** | Testing & Docs | 7 | 6 | 🟡 Ready |

**Total Effort:** ~32 hours (can be parallelized)

---

## PHASE 1: N8N AUTOMATION LAYER

### Component 1: N8N Deployment on Render

**Manual Steps (15 minutes):**

1. Go to Render.com Dashboard
2. Click "New +" → "Web Service"
3. Select "Docker" as runtime
4. Configure:
   - Name: `bhiv-n8n`
   - Docker Image: `n8n:latest`
   - Plan: Pro Plan ($12/month recommended)
5. Set Environment Variables:
   ```
   N8N_USER_MANAGEMENT_DISABLED=true
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=<strong-random-password>
   DATABASE_URL=postgresql://<user>:<pass>@<render-postgres>:5432/n8n_db
   N8N_HOST=bhiv-n8n.onrender.com
   WEBHOOK_URL=https://bhiv-n8n.onrender.com
   ```
6. Click "Create Web Service"
7. Wait for deployment (~5 minutes)
8. Verify: Visit https://bhiv-n8n.onrender.com/health

**AI Assistant Prompt:**

```
TASK: Generate N8N Render Deployment Configuration

I need to deploy N8N on Render for workflow automation.

REQUIREMENTS:
- Docker image: n8n:latest
- PostgreSQL database (separate from main app DB)
- Basic authentication for security
- Custom domain: bhiv-n8n.onrender.com
- Environment variable template
- Health check configuration

DELIVERABLES:
1. Complete Render Blueprint YAML
2. Environment variables checklist
3. PostgreSQL setup script
4. Post-deployment verification steps
5. Backup strategy for workflows

CONSTRAINTS:
- Use free tier resources where possible
- No credit card required for testing
- Health check endpoint: /health
- CORS enabled for webhook access
```

---

### Component 2: Email Workflow in N8N

**Manual Steps (30 minutes):**

1. Login to N8N: https://bhiv-n8n.onrender.com
2. Click "Create New Workflow"
3. Name it: `Email Notifications`
4. Add nodes:
   - **Trigger:** HTTP Request (webhook)
     - Method: POST
     - URL: `/webhook/email-trigger`
   - **Condition:** Route based on event type
   - **Gmail Send:** Configure SMTP
     - From: your-email@gmail.com
     - SMTP Server: smtp.gmail.com:587
     - Use App Password (not regular password)
   - **Database Logger:** Log to PostgreSQL
5. Create 4 email templates:
   - Application Received
   - Shortlisted
   - Interview Scheduled
   - Offer Received
6. Activate workflow
7. Test with sample payload

**AI Assistant Prompt:**

```
TASK: Create N8N Email Notification Workflow

Build complete email automation workflow.

WORKFLOW: Email Notifications

EVENTS TO HANDLE:
1. application_received
   Template: "Thank you for applying to {job_title}"
   Variables: candidate_name, job_title, company_name

2. candidate_shortlisted
   Template: "Great news! You're shortlisted for {job_title}"
   Variables: candidate_name, next_steps, interview_date

3. interview_scheduled
   Template: "Your interview is scheduled for {date} at {time}"
   Variables: candidate_name, date, time, link, interviewer_name

4. offer_received
   Template: "We're pleased to offer you {job_title}"
   Variables: candidate_name, position, salary, benefits_link

WEBHOOK PAYLOAD SCHEMA:
{
  "event": "string (one of above)",
  "recipient_email": "string",
  "recipient_name": "string",
  "variables": {object}
}

N8N CONFIGURATION:
1. HTTP Webhook Trigger
   - Method: POST
   - Path: /webhook/email-trigger

2. Conditional Router
   - Route based on "event" field
   - 4 paths (one per event type)

3. Gmail Send Node
   - Configure SMTP credentials
   - Use email templates with variable substitution
   - Add signature

4. Error Handler
   - Catch SMTP errors
   - Log to database
   - Send alert to admin

DELIVERABLES:
1. Complete workflow JSON export
2. Email template HTML files
3. Test payloads for each event
4. Gmail setup guide (App Passwords)
5. Webhook verification script
```

---

### Component 3: WhatsApp Integration via Twilio

**Manual Steps (45 minutes):**

1. Create Twilio account at twilio.com
2. Get: Account SID, Auth Token, WhatsApp number
3. Setup WhatsApp sandbox:
   - Enable WhatsApp in Twilio Console
   - Get sandbox number (e.g., +1234567890)
4. In N8N, create new workflow: `WhatsApp Notifications`
5. Add Twilio node:
   - Account SID: (from console)
   - Auth Token: (from console)
   - From Number: (Twilio WhatsApp number)
6. Create 3 message templates:
   - Status Update
   - Interview Reminder (24h before)
   - Offer Notification
7. Test with sample phone number
8. Deploy to production

**AI Assistant Prompt:**

```
TASK: Setup Twilio WhatsApp Integration in N8N

Configure WhatsApp messaging via Twilio.

TWILIO SETUP:
1. Create Twilio account
2. Enable WhatsApp (apply for production)
3. Get:
   - Account SID
   - Auth Token
   - WhatsApp sender number
   - Webhook URL

WORKFLOW: WhatsApp Notifications

MESSAGE TEMPLATES:

1. Status Update
   "Hi {name}! Your application for {job_title} is now {status}. "
   "View details: {dashboard_link}"

2. Interview Reminder (24h before)
   "Don't forget! Your interview for {job_title} is tomorrow at {time}. "
   "Join here: {interview_link}"

3. Offer Notification
   "Congratulations {name}! 🎉 We're offering you the position of "
   "{job_title}. Check your email for details."

N8N WORKFLOW STRUCTURE:
1. HTTP Webhook Trigger
2. Message Template Formatter
3. Twilio Send WhatsApp
4. Delivery Status Logger
5. Error Notification Handler

WEBHOOK PAYLOAD:
{
  "phone_number": "+91XXXXXXXXXX",
  "candidate_name": "string",
  "event": "status_update|interview_reminder|offer_notification",
  "variables": {object}
}

SECURITY:
- Store credentials in N8N secrets
- Enable request signing
- Whitelist allowed phone numbers
- Add rate limiting (max 100 msg/hour per user)

TESTING:
- Start in WhatsApp sandbox mode
- Test with your own number
- Verify message formatting
- Check delivery status tracking
- Test error scenarios

DELIVERABLES:
1. N8N workflow JSON
2. Twilio account setup guide
3. Message template library
4. Test scenarios and results
5. Production deployment checklist
```

---

### Component 4: Telegram Bot Setup

**Manual Steps (20 minutes):**

1. Open Telegram and search for @BotFather
2. Send `/newbot` command
3. Follow prompts:
   - Name: BHIV HR Bot
   - Username: bhiv_hr_bot
4. Copy bot token (keep it secret!)
5. In N8N, create workflow: `Telegram Bot Handler`
6. Configure Telegram node with bot token
7. Create command handlers:
   - `/status` → Query application status API
   - `/interview` → Show interview details
   - `/feedback` → Start feedback submission
   - `/reschedule` → Show available slots
8. Test commands in Telegram

**AI Assistant Prompt:**

```
TASK: Create Telegram Bot for Candidate Communication

Build interactive Telegram bot in N8N.

BOT SETUP (Manual):
1. Message @BotFather on Telegram
2. Send /newbot
3. Bot name: BHIV HR Bot
4. Bot username: bhiv_hr_bot (must be unique)
5. Save token (required for N8N)

COMMANDS TO IMPLEMENT:

/start
  Response: "Welcome to BHIV HR Bot! Available commands: /status, /interview, /feedback"

/status
  Query: GET /v1/candidate/applications/{user_id}
  Response: List of applications with statuses
  Format: "Application #1: Senior Developer - Status: Shortlisted"

/interview
  Query: GET /v1/interviews/{user_id}
  Response: Next scheduled interview details
  Format: "Interview: Nov 8, 2025 at 2:00 PM with John Smith"

/feedback
  Action: Start feedback collection
  Options: Text input or Voice input
  Query: POST /v1/feedback/submit

/reschedule
  Action: Show available interview slots
  Response: Calendar picker or available times
  Action: PUT /v1/interviews/{id}/reschedule

/help
  Response: Show all commands with descriptions

N8N CONFIGURATION:
1. Telegram Webhook Trigger
2. Command Router (switch node)
3. API Query nodes (one per command)
4. Message Formatter
5. Telegram Send Message
6. Error Handler

PAYLOAD PROCESSING:
{
  "message_id": "integer",
  "chat_id": "integer (user ID)",
  "text": "/status",
  "from": {
    "id": "integer",
    "first_name": "string",
    "username": "string"
  }
}

DELIVERABLES:
1. Complete N8N workflow JSON
2. BotFather setup screenshot
3. Command handler code
4. API integration mapping
5. Test conversation logs
```

---

### Component 5: Webhook Endpoints in Gateway

**Manual Steps (45 minutes):**

1. Clone repository locally:
   ```bash
   git clone https://github.com/Shashank-0208/BHIV-HR-PLATFORM.git
   cd BHIV-HR-PLATFORM/gateway
   ```

2. Open `main.py` and add new routes:
   ```python
   # After existing routes, add:
   
   @app.post("/webhooks/candidate-applied")
   async def webhook_candidate_applied(request: Request):
       payload = await request.json()
       # Trigger email + WhatsApp via N8N
       n8n_payload = {
           "event": "application_received",
           "recipient_email": payload["email"],
           "recipient_name": payload["name"],
           "variables": {
               "job_title": payload["job_title"],
               "company": payload["company"]
           }
       }
       # POST to N8N webhook
       async with aiohttp.ClientSession() as session:
           await session.post(
               "https://bhiv-n8n.onrender.com/webhook/email-trigger",
               json=n8n_payload
           )
       return {"status": "webhook_sent"}
   
   # Repeat for other events
   ```

3. Add signature verification:
   ```python
   import hmac
   import hashlib
   
   def verify_webhook_signature(payload, signature, secret):
       expected = hmac.new(
           secret.encode(),
           payload.encode(),
           hashlib.sha256
       ).hexdigest()
       return hmac.compare_digest(signature, expected)
   ```

4. Add logging:
   ```python
   import logging
   logger = logging.getLogger("webhooks")
   
   logger.info(f"Webhook received: {event_type}")
   logger.error(f"Webhook failed: {error}")
   ```

5. Test webhooks locally:
   ```bash
   curl -X POST http://localhost:8000/webhooks/candidate-applied \
     -H "Content-Type: application/json" \
     -d '{
       "event": "application_received",
       "email": "test@example.com",
       "name": "John Doe",
       "job_title": "Senior Developer"
     }'
   ```

6. Deploy to Render:
   ```bash
   git add .
   git commit -m "Add N8N webhook endpoints"
   git push origin main
   ```

**AI Assistant Prompt:**

```
TASK: Create Webhook Endpoints for N8N Integration

Add webhook handlers to Gateway for event-triggered automation.

GATEWAY ENDPOINTS TO CREATE:

1. POST /webhooks/candidate-applied
   Purpose: Trigger when candidate applies for job
   Payload:
   {
     "candidate_id": "uuid",
     "job_id": "uuid",
     "email": "string",
     "name": "string",
     "phone": "string",
     "job_title": "string"
   }
   Action: Send confirmation email + WhatsApp

2. POST /webhooks/candidate-shortlisted
   Purpose: HR shortlists candidate
   Payload:
   {
     "candidate_id": "uuid",
     "job_id": "uuid",
     "hr_id": "uuid",
     "shortlist_date": "timestamp"
   }
   Action: Send congratulations via Email + WhatsApp

3. POST /webhooks/interview-scheduled
   Purpose: Interview scheduled
   Payload:
   {
     "candidate_id": "uuid",
     "interview_id": "uuid",
     "date": "YYYY-MM-DD",
     "time": "HH:MM",
     "link": "url",
     "interviewer_name": "string"
   }
   Action: Send reminder + Telegram notification

4. POST /webhooks/feedback-received
   Purpose: Feedback submitted
   Payload:
   {
     "candidate_id": "uuid",
     "hr_id": "uuid",
     "feedback_text": "string",
     "rating": 1-5,
     "timestamp": "ISO8601"
   }
   Action: Log + Process for RL

IMPLEMENTATION REQUIREMENTS:

1. Security
   - HMAC-SHA256 signature verification
   - Timestamp validation (max 5 min old)
   - IP whitelist for N8N server
   - Request logging

2. Error Handling
   - Validate all required fields
   - Graceful failure if N8N unavailable
   - Retry logic (exponential backoff)
   - Error notifications to admin

3. Logging
   - Log all webhook calls
   - Store payload + response
   - Track success/failure rate
   - Monitor latency

4. Rate Limiting
   - Max 100 req/minute per source
   - Queue if exceeded
   - Alert on suspicious patterns

PYTHON IMPLEMENTATION:
- Use FastAPI for routing
- Use aiohttp for async HTTP calls
- Store in database for audit trail
- Add metrics/monitoring

TESTING:
- Test locally with curl
- Test with N8N test send
- Verify database logging
- Load test with 100 concurrent requests

DELIVERABLES:
1. Webhook endpoint code
2. Signature verification implementation
3. Error handling strategy
4. Logging configuration
5. Test script with curl commands
6. Deployment checklist
```

---

### Component 6: N8N Integration Testing

**Manual Steps (60 minutes):**

1. **Email Workflow Test:**
   ```bash
   curl -X POST https://bhiv-gateway.com/webhooks/candidate-applied \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": "test-123",
       "email": "yourtestemail@gmail.com",
       "name": "Test Candidate",
       "job_title": "DevOps Engineer"
     }'
   ```
   ✓ Check email received within 2 seconds

2. **WhatsApp Workflow Test:**
   - Use test phone number from Twilio
   - Send test WhatsApp via N8N
   - ✓ Verify message received

3. **Telegram Bot Test:**
   - Add bot to Telegram
   - Send `/status` command
   - ✓ Verify bot responds with application status

4. **Error Scenario Tests:**
   - Invalid email format
   - Wrong phone number
   - Database connection failure
   - ✓ Verify graceful error handling

5. **Load Test:**
   ```bash
   # Send 100 concurrent requests
   for i in {1..100}; do
     curl -X POST https://bhiv-gateway.com/webhooks/candidate-applied \
       -H "Content-Type: application/json" \
       -d "{...}" &
   done
   wait
   ```
   ✓ All requests processed successfully

**AI Assistant Prompt:**

```
TASK: Create Comprehensive N8N Integration Testing Suite

Build test plan and automation for N8N workflows.

TEST COVERAGE:

Unit Tests:
- Email template rendering
- WhatsApp message formatting
- Telegram command parsing
- Webhook signature verification
- Error handling for each node

Integration Tests:
- Complete email workflow (trigger → send → log)
- WhatsApp workflow (trigger → API call → status tracking)
- Telegram bot (command → API query → response)
- Multi-step workflows (application → email → whatsapp)

End-to-End Tests:
- Full candidate journey (apply → email → WhatsApp → Telegram)
- Error recovery (failed email → retry → success)
- Concurrent operations (100 users applying simultaneously)

Performance Tests:
- Single email send latency (target: <1s)
- WhatsApp delivery latency (target: <3s)
- Telegram response latency (target: <1s)
- Throughput: 1000 messages/minute

Reliability Tests:
- N8N server downtime → graceful degradation
- Database connection failure → queuing
- API timeout → retry with exponential backoff
- Network partition → reconnection

TEST AUTOMATION:
1. Pytest for unit tests
2. Postman collection for API tests
3. Selenium for UI tests (if applicable)
4. Locust for load testing
5. Monitoring dashboard for continuous testing

DELIVERABLES:
1. Test plan document
2. Test automation code
3. Performance benchmark report
4. Load test results
5. Bug report template
6. Pass/fail criteria
```

---

## PHASE 2: VOICE INTEGRATION

### Component 1: Voice Service (STT) Setup

**Manual Steps (2 hours):**

1. Create new GitHub branch:
   ```bash
   git checkout -b feature/voice-integration
   ```

2. Create new service directory:
   ```bash
   mkdir -p services/voice-service
   cd services/voice-service
   ```

3. Create `requirements.txt`:
   ```
   fastapi==0.115.6
   python-multipart==0.0.5
   openai==1.6.1
   psycopg2-binary==2.9.9
   sqlalchemy==2.0.23
   numpy==1.24.3
   librosa==0.10.0
   python-dotenv==1.0.0
   aiohttp==3.9.1
   textblob==0.17.1
   ```

4. Create `main.py`:
   ```python
   from fastapi import FastAPI, UploadFile, File
   import openai
   import os
   
   app = FastAPI()
   openai.api_key = os.getenv("OPENAI_API_KEY")
   
   @app.post("/voice/transcribe")
   async def transcribe_audio(
       file: UploadFile = File(...),
       user_id: str = None,
       context: str = None
   ):
       # Read audio file
       content = await file.read()
       
       # Transcribe with OpenAI Whisper
       transcript_response = await openai.Audio.atranscribe(
           model="whisper-1",
           file=("audio.m4a", content),
           language="en"
       )
       
       # Analyze sentiment
       from textblob import TextBlob
       sentiment = TextBlob(transcript_response["text"]).sentiment
       
       # Store in database
       # ... database logic ...
       
       return {
           "transcript": transcript_response["text"],
           "confidence": 0.95,
           "sentiment": sentiment,
           "timestamp": datetime.now().isoformat()
       }
   ```

5. Create Render service:
   - Name: `bhiv-voice-service`
   - GitHub: BHIV-HR-PLATFORM
   - Root Directory: `services/voice-service`
   - Environment Variables:
     ```
     OPENAI_API_KEY=sk-...
     DATABASE_URL=postgresql://...
     ```

6. Test locally:
   ```bash
   python -m uvicorn main:app --reload
   ```

7. Deploy to Render

**AI Assistant Prompt:**

```
TASK: Build OpenAI Whisper STT Microservice

Create voice transcription service using OpenAI Whisper.

SERVICE: bhiv-voice-service
Framework: FastAPI
Language: Python 3.12

ENDPOINTS:

1. POST /voice/transcribe
   File: Audio file (WAV, MP3, M4A)
   Params:
     - user_id: string (optional)
     - context: string (interview_feedback|candidate_interaction)
     - language: string (default: en)
   
   Response:
   {
     "audio_id": "uuid",
     "transcript": "string",
     "confidence": 0.85-1.0,
     "duration": 45.5,
     "sentiment": "positive|neutral|negative",
     "sentiment_score": -1.0 to 1.0,
     "language_detected": "en",
     "timestamp": "ISO8601"
   }

2. GET /voice/transcript/{audio_id}
   Returns: Stored transcript with all metadata

3. GET /voice/audit
   Params: user_id, date_range, type
   Returns: Audit log of all transcriptions

FEATURES:

Audio Processing:
- Support multiple formats (WAV, MP3, M4A, OPUS)
- Automatic format detection
- File size validation (max 25MB)
- Client-side compression support

Transcription:
- Use OpenAI Whisper API
- Extract confidence score
- Language detection
- Support for multiple languages

Sentiment Analysis:
- Use TextBlob for quick analysis
- Fallback to Hugging Face transformers
- Score: -1.0 to +1.0
- Categories: Positive (>0.5), Neutral, Negative (<-0.5)

Storage:
- Store audio file (encrypted)
- Store transcript + metadata
- Create audit log entry
- Index for fast retrieval

Error Handling:
- Invalid file format → HTTP 400
- File too large → HTTP 413
- Transcription failed → retry + HTTP 503
- Database error → queue + retry

Security:
- API key in environment
- Encrypt audio files at rest
- Access control on query endpoints
- Rate limiting (100 req/user/hour)

DATABASE:
Table: voice_interactions
- id (UUID)
- user_id (String)
- audio_file_path (String)
- transcript (Text)
- confidence (Float)
- sentiment (String)
- sentiment_score (Float)
- duration_seconds (Float)
- context (String)
- created_at (Timestamp)
- expires_at (Timestamp - 30 days)

DELIVERABLES:
1. FastAPI service code
2. OpenAI API integration
3. Sentiment analysis module
4. Database schema migration
5. Docker configuration
6. Render deployment guide
7. Test audio files
8. API documentation
```

---

### Component 2: TTS Service Setup

**Manual Steps (1.5 hours):**

1. Add TTS endpoint to voice service:
   ```python
   from google.cloud import texttospeech
   
   @app.post("/voice/synthesize")
   async def synthesize_text(request: dict):
       client = texttospeech.TextToSpeechClient()
       
       synthesis_input = texttospeech.SynthesisInput(text=request["text"])
       
       voice = texttospeech.VoiceSelectionParams(
           language_code="en-US",
           name="en-US-Neural2-C"
       )
       
       audio_config = texttospeech.AudioConfig(
           audio_encoding=texttospeech.AudioEncoding.MP3
       )
       
       response = client.synthesize_speech(
           input=synthesis_input,
           voice=voice,
           audio_config=audio_config
       )
       
       # Store audio file and return URL
       return {"audio_url": "...", "duration": 45.2}
   ```

2. Setup Google Cloud TTS:
   - Create GCP project
   - Enable Text-to-Speech API
   - Create service account
   - Download JSON key

3. Configure environment:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
   ```

4. Test TTS:
   ```bash
   curl -X POST http://localhost:8000/voice/synthesize \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, this is a test message"}'
   ```

5. Deploy update to Render

**AI Assistant Prompt:**

```
TASK: Build Google Cloud TTS Service Integration

Add text-to-speech capability to voice service.

ENDPOINT: POST /voice/synthesize

Request:
{
  "text": "string (max 5000 chars)",
  "language": "en-US",
  "voice_name": "en-US-Neural2-C",
  "speaking_rate": 1.0,
  "pitch": 0.0,
  "audio_format": "mp3|wav|ogg",
  "user_id": "string"
}

Response:
{
  "audio_id": "uuid",
  "audio_url": "https://storage.bhiv.ai/audio/xxx.mp3",
  "duration_seconds": 45.2,
  "size_bytes": 184000,
  "format": "mp3",
  "created_at": "ISO8601"
}

USE CASES:

1. Interview Reminders
   Text: "Hi John, your interview for Senior Developer is "
         "scheduled for Nov 8 at 2:00 PM. Click the link to join."
   Voice: en-US-Neural2-A (female)

2. Job Status Updates
   Text: "Congratulations! Your application for DevOps Engineer "
         "has been shortlisted."
   Voice: en-US-Neural2-C (male)

3. Offer Announcements
   Text: "We're pleased to offer you the position of Senior Developer."
   Voice: en-US-Neural2-A (female)

FEATURES:

Voice Options:
- Male: en-US-Neural2-C
- Female: en-US-Neural2-A
- Different accents available

Audio Formats:
- MP3 (compressed, default)
- WAV (uncompressed, high quality)
- OGG (compressed, alternative)

Caching:
- Cache by text hash + voice settings
- TTL: 30 days
- Avoid re-generating same audio

GOOGLE CLOUD SETUP:
1. Create GCP project
2. Enable Text-to-Speech API
3. Create service account
4. Download JSON key
5. Set GOOGLE_APPLICATION_CREDENTIALS environment variable

STORAGE:
- Store generated audio in cloud storage (AWS S3 or GCS)
- Return CDN URL for playback
- Implement access control

DELIVERABLES:
1. TTS integration code
2. Google Cloud setup guide
3. Voice selection documentation
4. Storage configuration
5. Caching strategy
6. Cost estimation
```

---

### Component 3: Voice UI Component

**Manual Steps (1.5 hours - Streamlit):**

1. Create voice recording component in Candidate Portal:
   ```python
   # In app.py (Candidate Portal)
   import streamlit as st
   from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
   import requests
   
   st.subheader("📞 Provide Voice Feedback")
   
   rtc_configuration = RTCConfiguration(
       {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
   )
   
   class AudioProcessor:
       def recv(self, frame):
           return frame
   
   webrtc_ctx = webrtc_streamer(
       key="sendrecv",
       mode=WebRtcMode.SENDRECV,
       rtc_configuration=rtc_configuration,
       audio_frame_callback=AudioProcessor(),
       async_processing=True,
   )
   
   if st.button("🎤 Start Recording Feedback"):
       st.session_state.recording = True
   
   if st.button("⏹️ Stop Recording"):
       st.session_state.recording = False
       # Upload audio to voice service
       if webrtc_ctx.audio_processor:
           audio_data = webrtc_ctx.audio_processor.frames
           # Send to /voice/transcribe endpoint
           response = requests.post(
               "https://bhiv-voice-service.onrender.com/voice/transcribe",
               files={"file": audio_data},
               params={"user_id": st.session_state.user_id}
           )
           transcript = response.json()["transcript"]
           st.success(f"Transcribed: {transcript}")
   ```

2. Install requirements:
   ```bash
   pip install streamlit-webrtc
   ```

3. Update app and deploy:
   ```bash
   git add .
   git commit -m "Add voice feedback UI component"
   git push origin feature/voice-integration
   ```

4. Test locally:
   ```bash
   streamlit run app.py
   ```

**AI Assistant Prompt:**

```
TASK: Create Voice Recording Component

Build Streamlit component for collecting voice feedback.

COMPONENT: VoiceRecorder

FEATURES:

1. Recording Controls
   - "Start Recording" button (🎤)
   - "Stop Recording" button (⏹️)
   - "Cancel" button (❌)
   - Real-time timer showing elapsed seconds
   - Visual indicator (red dot when recording)

2. Audio Visualization
   - Waveform display during recording
   - Real-time frequency analyzer
   - Volume level indicator

3. Playback
   - Play recorded audio
   - Speed controls (0.75x, 1x, 1.25x, 1.5x)
   - Seek bar for navigation
   - Duration display

4. Upload
   - "Submit Feedback" button
   - Progress indicator (%)
   - Status message ("Uploading...", "Processing...", "Complete")

5. Error Handling
   - Microphone permission denied
   - Recording interrupted
   - Upload failed (show retry button)
   - File size too large

WORKFLOW:

1. User clicks "Record Feedback"
2. Browser requests microphone permission
3. User approves (or denies → error)
4. Recording starts (show timer + waveform)
5. User records audio
6. User clicks "Stop"
7. Shows playback option
8. User can re-record or proceed
9. Click "Submit Feedback"
10. Upload to /voice/transcribe
11. Show "Processing..." spinner
12. Display transcript
13. Ask for confirmation
14. Submit feedback with transcript

UI LAYOUT:

┌─────────────────────────────────────┐
│ 📞 VOICE FEEDBACK                   │
├─────────────────────────────────────┤
│                                     │
│ [🎤 Start] [⏹️ Stop] [❌ Cancel]   │
│                                     │
│ ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁ (Waveform)        │
│ Volume: ████████░░ 80%              │
│ Time: 00:45                         │
│                                     │
│ ► [───────────────●───────────────] │
│   0:45 / 2:30                       │
│                                     │
│ Speed: [0.75x] [1x] [1.25x] [1.5x] │
│                                     │
│ [Re-record] [Submit Feedback ✓]     │
│                                     │
└─────────────────────────────────────┘

TECHNICAL REQUIREMENTS:

1. Frontend (Streamlit)
   - streamlit-webrtc for audio capture
   - Audio compression (MP3 encoding)
   - Client-side buffering
   - Progress tracking

2. Backend (Voice Service)
   - Receive audio file
   - Transcribe with Whisper
   - Analyze sentiment
   - Return transcript + metadata

3. Mobile Support
   - iOS Safari compatible
   - Android Chrome compatible
   - Low bandwidth handling
   - Battery consumption optimization

4. Accessibility
   - Keyboard controls (Space to start/stop)
   - Screen reader compatible
   - High contrast mode support
   - Voice command support (if browser supports)

DELIVERABLES:
1. Streamlit component code
2. CSS styling
3. JavaScript for audio capture
4. Accessibility audit report
5. Browser compatibility test results
6. Mobile testing screenshots
```

---

### Component 4: RL Loop Integration

**Manual Steps (1 hour):**

1. Add RL reward endpoint to Gateway:
   ```python
   @app.post("/rl/feedback-reward")
   async def record_feedback_reward(feedback: FeedbackRewardSchema):
       # Map sentiment to reward
       if feedback.sentiment_score > 0.7:
           reward = 1.0  # Positive
       elif feedback.sentiment_score < -0.7:
           reward = -1.0  # Negative
       else:
           reward = 0.0  # Neutral
       
       # Send to RL agent (Ishan's system)
       rl_payload = {
           "candidate_id": str(feedback.candidate_id),
           "job_id": str(feedback.job_id),
           "reward": reward,
           "feedback_text": feedback.transcript,
           "timestamp": datetime.now().isoformat()
       }
       
       # POST to RL agent endpoint
       async with aiohttp.ClientSession() as session:
           await session.post(
               os.getenv("RL_AGENT_URL") + "/learn",
               json=rl_payload
           )
       
       # Log feedback
       db.feedback_rewards.insert_one({
           "candidate_id": feedback.candidate_id,
           "reward": reward,
           "created_at": datetime.now()
       })
       
       return {"reward_recorded": True, "reward": reward}
   ```

2. Add database table for feedback rewards:
   ```sql
   CREATE TABLE feedback_rewards (
       id UUID PRIMARY KEY,
       candidate_id UUID REFERENCES candidates(id),
       job_id UUID REFERENCES jobs(id),
       audio_id UUID,
       reward_signal FLOAT,
       sentiment_score FLOAT,
       feedback_category VARCHAR(50),
       rl_updated BOOLEAN DEFAULT false,
       created_at TIMESTAMP DEFAULT NOW(),
       processed_at TIMESTAMP
   );
   ```

3. Deploy changes:
   ```bash
   git add .
   git commit -m "Add RL feedback reward integration"
   git push origin feature/voice-integration
   ```

**AI Assistant Prompt:**

```
TASK: Implement RL Feedback Loop Integration

Connect voice feedback to reinforcement learning system.

FLOW:
1. Candidate submits voice feedback
2. Transcription + sentiment analysis completed
3. Calculate reward signal from sentiment
4. Send reward to RL agent (Ishan's system)
5. RL updates matching weights
6. Log for monitoring

REWARD CALCULATION:

Sentiment Ranges:
- Positive (>0.7): Reward = +1.0
- Neutral (-0.3 to 0.3): Reward = 0.0
- Negative (<-0.7): Reward = -1.0

Feedback Quality Multipliers:
- Transcript length > 100 words: 1.0x
- Confidence > 0.9: 1.0x (high quality)
- Confidence 0.7-0.9: 0.8x (medium quality)
- Confidence < 0.7: 0.5x (low quality - still process but with lower weight)

Final Reward = Base Reward × Quality Multiplier

RL ENDPOINT:

POST /rl/feedback-reward

Request:
{
  "candidate_id": "uuid",
  "job_id": "uuid",
  "audio_id": "uuid",
  "transcript": "string",
  "sentiment_score": float (-1 to 1),
  "reward_signal": float (-1 to 1),
  "confidence": float (0 to 1),
  "feedback_category": "interview_quality|communication|job_fit|company_culture",
  "timestamp": "ISO8601"
}

Response:
{
  "reward_recorded": true,
  "rl_update_sent": true,
  "updated_weights": {object},
  "next_prediction_improvement": "5%"
}

DATABASE TRACKING:

Table: feedback_rewards
- id (UUID)
- candidate_id (UUID)
- job_id (UUID)
- audio_id (UUID)
- reward_signal (Float)
- sentiment_score (Float)
- confidence (Float)
- feedback_category (String)
- rl_updated (Boolean)
- created_at (Timestamp)
- processed_at (Timestamp)

INTEGRATION POINTS:

1. Voice Service → Gateway
   - Audio transcription completed
   - Sentiment analysis done
   - POST to /rl/feedback-reward

2. Gateway → RL Agent
   - Construct reward payload
   - Send via API
   - Handle timeout/failure

3. RL Agent → Model Update
   - Update matching weights
   - Recalculate match scores
   - Store new policy state

MONITORING:

Dashboard Metrics:
- Total feedback processed: int
- Average reward signal: float
- Positive feedback ratio: percentage
- RL update success rate: percentage
- Policy update frequency: int (per day)

Alerts:
- No feedback received (>24h)
- High failure rate (>10%)
- RL agent unreachable
- Unusual reward distribution

DELIVERABLES:
1. RL integration endpoint code
2. Reward calculation logic
3. Database schema
4. RL API communication module
5. Monitoring dashboard setup
6. Error handling strategy
```

---

### Component 5: Audit Logging

**Manual Steps (45 minutes):**

1. Create audit table in database:
   ```sql
   CREATE TABLE voice_audit_logs (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       interaction_id UUID NOT NULL,
       user_id VARCHAR(255) NOT NULL,
       user_role VARCHAR(50),
       interaction_type VARCHAR(50),
       transcript TEXT,
       sentiment_score FLOAT,
       confidence_score FLOAT,
       audio_file_hash VARCHAR(64),
       ip_address INET,
       user_agent TEXT,
       source_device VARCHAR(50),
       duration_seconds FLOAT,
       file_size_bytes INT,
       processing_time_ms INT,
       error_message TEXT,
       created_at TIMESTAMP DEFAULT NOW(),
       expires_at TIMESTAMP DEFAULT NOW() + INTERVAL '30 days',
       status VARCHAR(50),
       CONSTRAINT fk_interaction FOREIGN KEY (interaction_id) 
           REFERENCES voice_interactions(id)
   );
   
   CREATE INDEX idx_voice_audit_user ON voice_audit_logs(user_id);
   CREATE INDEX idx_voice_audit_created ON voice_audit_logs(created_at);
   CREATE INDEX idx_voice_audit_expires ON voice_audit_logs(expires_at);
   ```

2. Add audit logging to voice service:
   ```python
   from datetime import datetime, timedelta
   import hashlib
   
   async def log_voice_interaction(
       interaction_id: str,
       user_id: str,
       transcript: str,
       sentiment_score: float,
       request: Request
   ):
       audio_hash = hashlib.sha256(request.body).hexdigest()
       
       audit_log = {
           "interaction_id": interaction_id,
           "user_id": user_id,
           "transcript": transcript,
           "sentiment_score": sentiment_score,
           "ip_address": request.client.host,
           "user_agent": request.headers.get("user-agent"),
           "created_at": datetime.now(),
           "expires_at": datetime.now() + timedelta(days=30),
           "audio_file_hash": audio_hash,
           "status": "success"
       }
       
       # Insert into database
       await db.voice_audit_logs.insert_one(audit_log)
   ```

3. Add audit query endpoint:
   ```python
   @app.get("/audit/voice-interactions")
   async def get_audit_logs(
       user_id: str = None,
       date_from: str = None,
       date_to: str = None,
       skip: int = 0,
       limit: int = 100
   ):
       query = {}
       if user_id:
           query["user_id"] = user_id
       if date_from:
           query["created_at"] = {"$gte": datetime.fromisoformat(date_from)}
       
       logs = await db.voice_audit_logs.find(query)\
           .skip(skip)\
           .limit(limit)\
           .sort("created_at", -1)
       
       return {"logs": logs, "total": await db.voice_audit_logs.count_documents(query)}
   ```

4. Deploy updates

**AI Assistant Prompt:**

```
TASK: Setup Voice Audit Logging & Compliance

Create comprehensive audit trail for voice interactions.

DATABASE SCHEMA:

Table: voice_audit_logs

Columns:
- id (UUID primary key)
- interaction_id (UUID foreign key)
- user_id (String indexed)
- user_role (enum: candidate, hr, recruiter)
- interaction_type (enum: recording, feedback, reminder)
- transcript (Text encrypted)
- sentiment_score (Float)
- confidence_score (Float)
- audio_file_hash (String SHA-256)
- ip_address (INET indexed)
- user_agent (Text)
- source_device (enum: web, mobile, api)
- duration_seconds (Float)
- file_size_bytes (Int)
- processing_time_ms (Int)
- error_message (Text nullable)
- created_at (Timestamp indexed)
- expires_at (Timestamp indexed - 30 days)
- status (enum: success, failed, processing)

COMPLIANCE:

GDPR:
- Data retention: 30 days maximum
- Right to erasure: Implemented (soft delete)
- Data portability: Export endpoint
- Access control: Role-based

Privacy:
- Encrypt PII at rest
- Anonymize on export
- Audit access to logs
- Secure deletion after retention

QUERY ENDPOINTS:

GET /audit/voice-interactions
  Filters:
    - user_id (required or admin)
    - date_range
    - interaction_type
    - status
  Returns: Paginated audit logs

GET /audit/voice-interactions/{id}
  Returns: Full audit record

DELETE /audit/voice-interactions/{id}
  Soft delete (mark deleted, keep 7 more days)

GET /audit/voice-analytics
  Returns:
  {
    "total_interactions": int,
    "success_rate": 0.95,
    "avg_sentiment": 0.45,
    "by_source": {...},
    "by_date": {...}
  }

CLEANUP JOBS:

Scheduled Daily (2:00 AM UTC):
- Hard delete records older than 30 days
- Archive logs to cold storage
- Generate compliance report

Scheduled Weekly (Sunday 3:00 AM):
- Generate audit summary
- Check for anomalies
- Alert on suspicious patterns

SECURITY:

Access Control:
- Users can only view their own logs
- HR can view candidate logs (with consent)
- Admins can view all logs
- All access logged

Encryption:
- Encrypt transcript at rest
- Use TLS for transmission
- Secure key management

Logging:
- Log all audit log queries
- Track who accessed what and when
- Store in separate secure table

DELIVERABLES:
1. Database schema migration
2. Logging middleware
3. Query endpoints
4. Cleanup scripts
5. Compliance documentation
6. Access control matrix
```

---

## PHASE 3: REAL-TIME SYNCHRONIZATION

### Component 1: Socket.IO Integration

**Manual Steps (2 hours):**

1. Update Gateway requirements:
   ```bash
   pip install python-socketio python-engineio python-socketio-client
   ```

2. Add to `requirements.txt` and deploy

3. Modify Gateway `main.py`:
   ```python
   from fastapi import FastAPI
   from fastapi_cors import CORSMiddleware
   from socketio import ASGIApp, Server
   
   # Create FastAPI app
   app = FastAPI()
   
   # Create Socket.IO instance
   sio = Server(
       async_mode='asgi',
       cors_allowed_origins='*',
       ping_interval=60,
       ping_timeout=120,
       max_http_buffer_size=1e6
   )
   
   # Combine FastAPI + Socket.IO
   asgi_app = ASGIApp(socketio_server=sio, fastapi_app=app)
   
   # Socket.IO event handlers
   @sio.event
   async def connect(sid, environ):
       token = environ.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
       user_data = verify_jwt(token)  # Verify JWT
       
       # Store user connection
       user_connections[sid] = {
           'user_id': user_data['user_id'],
           'portal': user_data.get('portal', 'unknown'),
           'connected_at': datetime.now()
       }
       
       # Join user-specific room
       sio.enter_room(sid, f"user_{user_data['user_id']}")
       
       # Join portal-specific room
       sio.enter_room(sid, f"{user_data['portal']}_users")
       
       print(f"User {user_data['user_id']} connected")
   
   @sio.event
   async def disconnect(sid):
       if sid in user_connections:
           user_id = user_connections[sid]['user_id']
           print(f"User {user_id} disconnected")
           del user_connections[sid]
   
   # Event emitter function
   async def emit_application_update(application_id, new_status):
       # Query application to get candidate and job info
       app_data = db.job_applications.find_one({"_id": application_id})
       
       event_data = {
           "application_id": str(application_id),
           "candidate_id": str(app_data['candidate_id']),
           "new_status": new_status,
           "updated_at": datetime.now().isoformat()
       }
       
       # Broadcast to HR dashboard
       sio.emit('application_status_updated', event_data, room='hr_dashboard')
       
       # Notify candidate
       sio.emit('your_application_updated', event_data, 
                room=f"candidate_{app_data['candidate_id']}")
   ```

4. Update database interaction endpoints to emit events:
   ```python
   # When HR shortlists candidate
   @app.post("/v1/shortlist")
   async def shortlist_candidate(data: ShortlistSchema):
       # Save to database
       result = db.shortlists.insert_one({...})
       
       # Emit Socket.IO event
       await emit_application_update(
           data.application_id,
           "shortlisted"
       )
       
       return {"status": "shortlisted"}
   ```

5. Test WebSocket connection:
   ```bash
   # Install WebSocket testing tool
   pip install websocket-client
   
   # Test script
   import websocket
   ws = websocket.WebSocket()
   ws.connect("wss://bhiv-gateway.onrender.com/socket.io/?transport=websocket")
   ```

**AI Assistant Prompt:**

```
TASK: Integrate Socket.IO for Real-time Updates

Add WebSocket support to Gateway for real-time cross-portal synchronization.

INSTALLATION:
pip install python-socketio python-engineio uvicorn[standard]

SOCKET.IO SETUP:

Configuration:
- async_mode: 'asgi'
- CORS: Allow all origins (secure later)
- Ping interval: 60 seconds
- Ping timeout: 120 seconds
- Max buffer: 1MB

AUTHENTICATION:
- Extract JWT from Connection URL
- Verify token validity
- Store user connection info
- Disconnect invalid tokens

ROOMS (Topic Subscriptions):

1. Portal Rooms
   - "hr_dashboard" - All HR team members
   - "client_dashboard_{company_id}" - Client company users
   - "candidate_portal" - All candidates

2. User-Specific Rooms
   - "user_{user_id}" - Individual user updates
   - "candidate_{candidate_id}" - Candidate-specific updates
   - "recruiter_{recruiter_id}" - Recruiter-specific updates

3. Team Rooms
   - "hr_team_{hr_manager_id}" - HR team members
   - "company_{company_id}" - Company-wide updates

EVENTS TO EMIT:

Event: "application_received"
Data:
{
  "application_id": "uuid",
  "candidate_id": "uuid",
  "job_id": "uuid",
  "candidate_name": "string",
  "job_title": "string",
  "applied_at": "ISO8601"
}
Rooms: hr_dashboard, client_dashboard_{company_id}

Event: "candidate_shortlisted"
Data:
{
  "candidate_id": "uuid",
  "job_title": "string",
  "shortlist_date": "ISO8601"
}
Rooms: candidate_{candidate_id}, hr_dashboard

Event: "interview_scheduled"
Data:
{
  "interview_id": "uuid",
  "date": "YYYY-MM-DD",
  "time": "HH:MM",
  "link": "url",
  "interviewer_name": "string"
}
Rooms: candidate_{candidate_id}, hr_dashboard

Event: "offer_extended"
Data:
{
  "candidate_id": "uuid",
  "job_title": "string",
  "salary": "string",
  "benefits": "string"
}
Rooms: candidate_{candidate_id}

IMPLEMENTATION STEPS:

1. Add Socket.IO to requirements.txt
2. Create Socket.IO server instance
3. Implement connection handler
4. Implement disconnect handler
5. Create room management logic
6. Emit events from API endpoints
7. Test with Socket.IO client
8. Implement fallback polling
9. Add connection status indicator
10. Deploy to Render

ERROR HANDLING:
- Invalid token: Disconnect immediately
- Connection timeout: Auto-reconnect (3s, 6s, 12s, 30s)
- Message delivery failure: Log and retry
- Server crash: Clients auto-reconnect

DELIVERABLES:
1. Socket.IO server code
2. Event definitions and data schemas
3. Room management logic
4. Client connection guide
5. Test client script
6. Deployment checklist
```

---

### Component 2: Agent-State Synchronizer

**Manual Steps (3 hours):**

1. Create new microservice repository:
   ```bash
   mkdir bhiv-state-sync
   cd bhiv-state-sync
   git init
   ```

2. Create `requirements.txt`:
   ```
   fastapi==0.115.6
   sqlalchemy==2.0.23
   psycopg2-binary==2.9.9
   aiohttp==3.9.1
   python-socketio==5.9.0
   ```

3. Create `main.py`:
   ```python
   from fastapi import FastAPI, BackgroundTasks
   from sqlalchemy import create_engine
   import asyncio
   
   app = FastAPI()
   
   # Database connection
   engine = create_engine(os.getenv("DATABASE_URL"))
   
   class StateStore:
       def __init__(self):
           self.states = {}  # In-memory cache
       
       async def update_state(self, entity_type, entity_id, new_state):
           key = f"{entity_type}:{entity_id}"
           
           # Check for conflicts
           if key in self.states:
               old_state = self.states[key]
               conflict = self.detect_conflict(old_state, new_state)
               if conflict:
                   new_state = self.resolve_conflict(old_state, new_state)
           
           # Update state
           self.states[key] = new_state
           
           # Persist to database
           await self.persist_state(entity_type, entity_id, new_state)
           
           # Broadcast via Socket.IO
           await self.broadcast_state_change(entity_type, entity_id, new_state)
       
       def detect_conflict(self, old_state, new_state):
           # Compare timestamps
           old_time = old_state.get('updated_at')
           new_time = new_state.get('updated_at')
           
           if old_time and new_time and (new_time - old_time).total_seconds() < 1:
               return True  # Concurrent update
           
           return False
       
       def resolve_conflict(self, old_state, new_state):
           # Last-write-wins strategy
           old_time = old_state.get('updated_at')
           new_time = new_state.get('updated_at')
           
           if new_time > old_time:
               return new_state
           else:
               return old_state
   
   state_store = StateStore()
   
   @app.post("/state/update")
   async def update_state(entity_type: str, entity_id: str, new_state: dict):
       await state_store.update_state(entity_type, entity_id, new_state)
       return {"status": "updated"}
   
   @app.get("/state/{entity_type}/{entity_id}")
   async def get_state(entity_type: str, entity_id: str):
       key = f"{entity_type}:{entity_id}"
       return state_store.states.get(key, {})
   ```

4. Deploy on Render:
   - Create new service: `bhiv-state-sync`
   - Set environment variables
   - Deploy

**AI Assistant Prompt:**

```
TASK: Build State Synchronizer Microservice

Create service for maintaining unified state across portals.

SERVICE: bhiv-state-sync
Framework: FastAPI
Deployment: Render (separate instance)

RESPONSIBILITIES:
- Listen to all state change events
- Maintain unified state in database + memory cache
- Detect and resolve conflicts
- Broadcast updates via Socket.IO
- Provide state query endpoints

STATE ENTITIES:

CandidateState:
{
  candidate_id: UUID,
  email: String,
  name: String,
  phone: String,
  profile_complete: Boolean,
  total_applications: Int,
  total_interviews: Int,
  total_offers: Int,
  status: "active|inactive|archived",
  last_updated: Timestamp,
  updated_by: String,
  version: Int (for conflict detection)
}

ApplicationState:
{
  application_id: UUID,
  candidate_id: UUID,
  job_id: UUID,
  status: "applied|shortlisted|interviewed|offered|rejected",
  timeline: {
    applied: Timestamp,
    shortlisted: Timestamp,
    interviewed: Timestamp,
    offered: Timestamp,
    rejected: Timestamp
  },
  last_updated: Timestamp,
  updated_by: String,
  version: Int
}

InterviewState:
{
  interview_id: UUID,
  candidate_id: UUID,
  interviewer_id: UUID,
  date: Date,
  time: Time,
  status: "scheduled|completed|cancelled|rescheduled",
  link: String,
  notes: String,
  feedback_submitted: Boolean,
  last_updated: Timestamp,
  version: Int
}

STATE UPDATE FLOW:

1. Event received from Gateway
   Example: HR shortlists candidate
   
2. Construct state change
   ApplicationState.status = "shortlisted"
   
3. Query current state from database
   Get previous version and timestamp
   
4. Conflict Detection
   - Compare versions
   - Check timestamps
   - Detect concurrent updates
   
5. Conflict Resolution
   - Last-write-wins (default)
   - Merge non-conflicting fields
   - Log conflict for audit
   
6. Update state
   - Save to database
   - Update in-memory cache
   - Increment version
   
7. Broadcast
   - Emit via Socket.IO to relevant rooms
   - Notify HR, Client, Candidate portals
   
8. Logging
   - Store in state_transitions table
   - Include conflict info

DATABASE SCHEMA:

Table: state_snapshots
- id (UUID)
- entity_type (String: candidate, application, interview)
- entity_id (UUID)
- state (JSONB)
- version (Int)
- hash (String SHA-256)
- created_at (Timestamp)
- updated_at (Timestamp)
- created_by (String)
- updated_by (String)

Table: state_transitions
- id (UUID)
- entity_type (String)
- entity_id (UUID)
- from_state (JSONB)
- to_state (JSONB)
- transition_time (Timestamp)
- triggered_by (String)
- trigger_event (String)
- conflict_detected (Boolean)
- conflict_resolution_strategy (String)

ENDPOINTS:

GET /state/{entity_type}/{entity_id}
  Returns: Current state of entity

GET /state/history/{entity_type}/{entity_id}
  Params: limit (default 100)
  Returns: State transition history

POST /state/merge
  Body: {old_state, new_state, conflict_policy}
  Returns: {merged_state, conflicts}

GET /health/state-sync
  Returns: Service health + queue depth

CONFLICT RESOLUTION STRATEGIES:

Last-Write-Wins (Default)
- Most recent update wins
- Use updated_at timestamp
- Simple, fast

Field-Level Merge
- Merge non-conflicting fields
- Conflict only on same field updated
- Complex but less data loss

Version Vector
- Track version per field
- Detect causally related updates
- Most complex, most accurate

DELIVERABLES:
1. FastAPI service code
2. State management logic
3. Conflict detection algorithm
4. Database schema migration
5. State query endpoints
6. Integration with Socket.IO
7. Testing strategy
8. Deployment guide
```

---

### Component 3: Socket.IO Clients in Portals

**Manual Steps (1.5 hours - Streamlit):**

1. Update Candidate Portal `app.py`:
   ```python
   import socketio
   
   # Initialize Socket.IO client
   sio = socketio.Client(
       reconnection=True,
       reconnection_delay=1,
       reconnection_delay_max=5,
       reconnection_attempts=10
   )
   
   @sio.event
   def connect():
       st.session_state.socket_connected = True
       st.toast("✅ Connected to real-time updates")
       
       # Join rooms based on user role
       sio.emit('join', {
           'room': f'candidate_{st.session_state.user_id}',
           'portal': 'candidate'
       })
   
   @sio.event
   def disconnect():
       st.session_state.socket_connected = False
       st.toast("⚠️ Connection lost. Retrying...")
   
   @sio.event
   def application_status_updated(data):
       # Application status changed
       st.session_state.applications_updated = True
       st.rerun()
   
   @sio.event
   def interview_scheduled(data):
       # New interview scheduled
       st.session_state.interview_notification = data
       st.toast(f"📅 Interview scheduled for {data['date']}")
       st.rerun()
   
   @sio.event
   def offer_received(data):
       # Job offer received
       st.session_state.offer_notification = data
       st.toast(f"🎉 Offer received for {data['job_title']}")
       st.rerun()
   
   # Connect on app load
   if 'socket_connected' not in st.session_state:
       token = st.session_state.get('jwt_token')
       sio.connect(
           f'https://bhiv-gateway.onrender.com',
           auth={'token': token},
           headers={'Authorization': f'Bearer {token}'}
       )
   
   # Show connection status
   col1, col2 = st.columns([3, 1])
   with col2:
       if st.session_state.get('socket_connected'):
           st.success("🟢 Live")
       else:
           st.warning("🔴 Offline")
   ```

2. Deploy updates

**AI Assistant Prompt:**

```
TASK: Implement Socket.IO Clients in Candidate Portal

Add real-time listeners to Candidate Portal.

IMPLEMENTATION (Streamlit):

Connection Setup:
- Connect on app load
- Pass JWT token for authentication
- Join candidate-specific rooms
- Handle reconnections

Event Listeners:

1. application_status_updated
   Data: {application_id, new_status, updated_at}
   Action: Refresh dashboard, show toast notification

2. interview_scheduled
   Data: {interview_id, date, time, link, interviewer}
   Action: Add to calendar, show modal, send reminder

3. interview_cancelled
   Data: {interview_id, reason}
   Action: Remove from calendar, notify user

4. offer_received
   Data: {job_title, company, salary, link}
   Action: Highlight in dashboard, show celebration

5. message_from_recruiter
   Data: {message, recruiter_name}
   Action: Show in-app notification, add to message thread

6. feedback_acknowledged
   Data: {feedback_id, status}
   Action: Confirm to user

UI UPDATES:

Connection Status:
- Green dot: Connected
- Orange dot: Connecting
- Red dot: Offline
- Show in sidebar or top bar

Notifications:
- Toast notifications for events
- Badge count for unread items
- Highlight new items in lists
- Sound alert option (opt-in)

Dashboard Auto-Refresh:
- Application list updates without reload
- Status badges update in real-time
- Interview schedule updates live
- Metrics update automatically

RELIABILITY:

Reconnection:
- Attempt up to 10 reconnections
- Exponential backoff (1s, 2s, 4s...)
- Max wait: 5 seconds
- Auto-sync on reconnection

Fallback:
- If WebSocket fails, use polling
- Poll every 5 seconds
- Reduce load gradually
- Show "Offline mode" warning

Error Handling:
- Invalid token: Show login page
- Server error: Show retry button
- Network error: Auto-retry
- Timeout: Log and alert user

DELIVERABLES:
1. Socket.IO client code
2. Event handler definitions
3. UI component updates
4. Connection management
5. Offline fallback implementation
6. Error handling strategy
```

---

## DEPLOYMENT & VERIFICATION CHECKLIST

### Pre-Deployment Checklist

- [ ] All code committed to GitHub
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Dependencies updated (requirements.txt)
- [ ] Tests passing (unit + integration)
- [ ] Documentation updated
- [ ] Security audit completed
- [ ] Performance benchmarks acceptable

### Deployment Order

1. **N8N Service** (Render)
2. **Voice Service** (Render)
3. **State Sync Service** (Render)
4. **Gateway Updates** (Render)
5. **Portal Updates** (Render)
6. **Testing & Verification**

### Post-Deployment Verification

```bash
# Check all services running
curl https://bhiv-n8n.onrender.com/health
curl https://bhiv-voice-service.onrender.com/health
curl https://bhiv-state-sync.onrender.com/health
curl https://bhiv-hr-gateway.onrender.com/health

# Verify databases
psql $DATABASE_URL -c "SELECT version();"

# Test endpoints
curl https://bhiv-hr-gateway.onrender.com/v1/health

# Monitor logs
tail -f /var/log/deployment.log
```

---

## Success Metrics

| Component | Metric | Target | Current |
|-----------|--------|--------|---------|
| N8N | Email send latency | <1s | TBD |
| N8N | WhatsApp delivery | <3s | TBD |
| Voice | STT latency | <2s | TBD |
| Voice | Sentiment accuracy | 85%+ | TBD |
| Sync | Event broadcast | <100ms | TBD |
| Overall | System uptime | 99.9% | TBD |

---

**Document Updated:** November 6, 2025  
**Next Review:** November 8, 2025