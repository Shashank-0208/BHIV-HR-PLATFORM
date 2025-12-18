# BHIV LangGraph Service

**FastAPI + LangGraph + RL Integration**  
**Production URL**: https://bhiv-hr-langgraph.onrender.com  
**Endpoints**: 33 total (25 workflow + 8 RL)  
**Status**: ✅ Operational with 100% RL Test Pass Rate  
**Database**: PostgreSQL 17 Schema v4.3.1 (19 tables + RL integration)

## Overview
AI-powered workflow orchestration service for BHIV HR Platform with intelligent Python-based automation and reinforcement learning capabilities.

## Features
- **Candidate Application Workflows**: Automated processing of job applications
- **AI-Driven Matching**: Intelligent candidate-job matching with scoring
- **Multi-Channel Notifications**: Email, WhatsApp, Telegram integration (✅ Confirmed Working)
- **Real-time Updates**: WebSocket support for live workflow status
- **RL Integration**: 8 operational endpoints with 100% test success
- **Database Integration**: 5 RL predictions, 17 feedback records, 340% feedback rate
- **Model Training**: RL model v1.0.1 with 80% accuracy

## API Endpoints (33 Total)

### Core Endpoints (2)
- `GET /` - Service information
- `GET /health` - Service health check

### Workflow Endpoints (25)
- `POST /workflows/application/start` - Start candidate application workflow
- `GET /workflows/{workflow_id}/status` - Get workflow status
- `POST /workflows/{workflow_id}/resume` - Resume paused workflow
- `GET /workflows` - List all workflows
- `GET /workflows/stats` - Workflow statistics
- `POST /tools/send-notification` - Multi-channel notifications
- Additional workflow and communication endpoints

### RL Integration Endpoints (8) - ✅ 100% Operational
- `POST /rl/predict` - ML-powered candidate matching
- `POST /rl/feedback` - Submit hiring outcome feedback
- `GET /rl/analytics` - System performance metrics
- `GET /rl/performance/{model_version}` - Model performance data
- `GET /rl/history/{candidate_id}` - Candidate decision history
- `POST /rl/retrain` - Trigger model retraining
- `GET /test-integration` - RL system integration test

### Workflow Types
1. **Application Processing**: Candidate applies for job
2. **Shortlist Notification**: Candidate gets shortlisted
3. **Interview Scheduling**: Interview gets scheduled
4. **AI Matching**: Semantic matching with scoring

## Local Development

### Prerequisites
- Python 3.12.7+
- PostgreSQL database
- Gemini API key (optional)

### Setup
```bash
cd services/langgraph
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 9001 --reload
```

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/bhiv_hr
GATEWAY_SERVICE_URL=http://localhost:8000
API_KEY_SECRET=your_api_key
JWT_SECRET_KEY=your_jwt_secret
CANDIDATE_JWT_SECRET_KEY=your_candidate_jwt_secret
GEMINI_API_KEY=your_gemini_key  # Optional
GEMINI_MODEL=gemini-pro
TWILIO_AUTH_TOKEN_SECRET_KEY=your_twilio_token  # Optional
GMAIL_APP_PASSWORD_SECRET_KEY=your_gmail_password  # Optional
TELEGRAM_BOT_TOKEN_SECRET_KEY=your_telegram_token  # Optional
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Docker Deployment
```bash
docker build -t bhiv-langgraph .
docker run -p 9001:9001 bhiv-langgraph
```

## Production Deployment (Render)
- Service URL: `https://bhiv-langgraph.onrender.com`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python -m uvicorn app:app --host 0.0.0.0 --port $PORT`

## Integration with Gateway
The LangGraph service integrates with the BHIV Gateway through:
- `/api/v1/workflows/*` endpoints in gateway
- Provides intelligent workflow automation
- Provides AI-powered workflow orchestration

## Testing
```bash
# Health check
curl http://localhost:9001/health

# Start workflow
curl -X POST http://localhost:9001/workflows/application/start \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "application_id": 1,
    "candidate_email": "test@example.com",
    "candidate_name": "Test User",
    "job_title": "Software Engineer"
  }'
```