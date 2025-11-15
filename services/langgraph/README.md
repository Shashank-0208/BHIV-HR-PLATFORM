# BHIV LangGraph Service

## Overview
AI-powered workflow orchestration service for BHIV HR Platform with intelligent Python-based automation.

## Features
- **Candidate Application Workflows**: Automated processing of job applications
- **AI-Driven Matching**: Intelligent candidate-job matching with scoring
- **Multi-Channel Notifications**: Email, WhatsApp, Telegram integration
- **Real-time Updates**: WebSocket support for live workflow status
- **Voice Integration**: STT/TTS capabilities for voice interactions

## API Endpoints

### Core Endpoints
- `GET /health` - Service health check
- `POST /workflows/application/start` - Start candidate application workflow
- `GET /workflows/{workflow_id}/status` - Get workflow status
- `POST /workflows/{workflow_id}/resume` - Resume paused workflow
- `WebSocket /ws/{workflow_id}` - Real-time workflow updates

### Workflow Types
1. **Application Processing**: Candidate applies for job
2. **Shortlist Notification**: Candidate gets shortlisted
3. **Interview Scheduling**: Interview gets scheduled
4. **AI Matching**: Semantic matching with scoring

## Local Development

### Prerequisites
- Python 3.12.7+
- PostgreSQL database
- OpenAI API key (optional)

### Setup
```bash
cd services/langgraph
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 9001 --reload
```

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/bhiv_hr
GATEWAY_URL=http://localhost:8000
API_KEY_SECRET=your_api_key
OPENAI_API_KEY=your_openai_key  # Optional
ENVIRONMENT=development
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