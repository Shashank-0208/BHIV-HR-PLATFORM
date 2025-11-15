# 🔄 LangGraph Workflow Automation Guide

## 🎯 Overview
This guide provides comprehensive instructions for LangGraph AI-powered workflow orchestration in the BHIV HR Platform v4.2.0.

## 📋 Prerequisites
- Docker and Docker Compose installed
- Python 3.12.7 or higher
- Access to BHIV HR Platform codebase
- LangGraph service operational (Port 9001)

## ✅ Current Implementation Status
✅ LangGraph service fully integrated
✅ AI workflow automation operational
✅ Multi-channel notifications active
✅ 7 workflow endpoints functional

## Step 2: LangGraph Service Setup (COMPLETED)
✅ Consolidated into `services/langgraph/` directory
✅ Full LangGraph orchestrator with AI workflows
✅ Removed duplicate langgraph_service
✅ Updated Docker Compose configuration

## Step 3: Manual Deployment Steps

### Local Development Setup

1. **Start LangGraph Service Locally**
```bash
cd "c:\BHIV HR PLATFORM\services\langgraph"
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 9001 --reload
```

2. **Verify LangGraph Service**
```bash
curl http://localhost:9001/health
```
Expected response:
```json
{
  "status": "healthy",
  "service": "LangGraph Workflow Service",
  "version": "1.0.0",
  "timestamp": "2025-01-02T..."
}
```

3. **Start Full Platform with Docker Compose**
```bash
cd "c:\BHIV HR PLATFORM"
docker-compose -f deployment/docker/docker-compose.production.yml up -d
```

4. **Test LangGraph Integration**
```bash
# Test workflow status
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     http://localhost:8000/api/v1/workflows/status

# Test candidate application workflow
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "email": "test@example.com",
       "name": "Test Candidate",
       "job_title": "Software Engineer"
     }' \
     http://localhost:8000/api/v1/workflows/candidate-applied
```

### Production Deployment (Render)

1. **Create New Render Service**
   - Go to Render Dashboard
   - Create new Web Service
   - Connect GitHub repository
   - Set build command: `cd services/langgraph_service && pip install -r requirements.txt`
   - Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables for Render**
```
EMAIL_SERVICE_URL=http://localhost:8080
WHATSAPP_SERVICE_URL=http://localhost:8081
PORT=9001
```

3. **Update Gateway Service Environment**
Add to existing gateway service on Render:
```
LANGGRAPH_URL=https://bhiv-langgraph-service.onrender.com
LANGGRAPH_PRODUCTION_URL=https://bhiv-langgraph-service.onrender.com
```

## Step 4: Testing Workflows

### Test Candidate Application Workflow
```bash
curl -X POST \
  https://bhiv-hr-gateway-ltg0.onrender.com/api/v1/workflows/candidate-applied \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "email": "candidate@example.com",
    "name": "John Doe",
    "job_title": "Software Engineer",
    "phone": "+1234567890"
  }'
```

### Test Shortlist Notification
```bash
curl -X POST \
  https://bhiv-hr-gateway-ltg0.onrender.com/api/v1/workflows/candidate-shortlisted \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "email": "candidate@example.com",
    "name": "John Doe",
    "job_title": "Software Engineer"
  }'
```

### Test Interview Scheduling
```bash
curl -X POST \
  https://bhiv-hr-gateway-ltg0.onrender.com/api/v1/workflows/interview-scheduled \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "email": "candidate@example.com",
    "name": "John Doe",
    "job_title": "Software Engineer",
    "date": "2025-01-10",
    "time": "10:00 AM"
  }'
```

## Step 5: Verification Checklist

### Local Environment
- [ ] LangGraph service starts on port 9001
- [ ] Gateway service connects to LangGraph
- [ ] Workflow endpoints respond correctly
- [ ] Docker Compose includes all 6 services (including LangGraph)

### Production Environment  
- [ ] LangGraph service deployed on Render
- [ ] Gateway service updated with LangGraph URLs
- [ ] All workflow endpoints functional
- [x] LangGraph handles all workflow automation

## Step 6: Monitoring and Logs

### Check LangGraph Service Status
```bash
curl https://bhiv-hr-gateway-ltg0.onrender.com/api/v1/workflows/status
```

### View Service Logs (Local)
```bash
docker-compose logs langgraph_service
```

### View Service Logs (Render)
- Go to Render Dashboard
- Select LangGraph service
- View Logs tab

## Troubleshooting

### Common Issues

1. **LangGraph Service Not Starting**
   - Check port 9001 is available
   - Verify requirements.txt dependencies
   - Check Python version (3.12.7 required)

2. **Gateway Cannot Connect to LangGraph**
   - Verify LANGGRAPH_URL environment variable
   - Check network connectivity
   - Ensure LangGraph service is healthy

3. **Workflow Endpoints Return Errors**
   - Check API key authentication
   - Verify request payload format
   - Review LangGraph service logs

### Support Commands
```bash
# Check all services status
docker-compose ps

# Restart LangGraph service
docker-compose restart langgraph_service

# View real-time logs
docker-compose logs -f langgraph_service
```

## Migration Complete

✅ **LangGraph Integrated**: AI workflow service fully operational  
✅ **Endpoints Active**: 7 workflow endpoints providing complete automation
✅ **Multi-Channel**: Email, WhatsApp, SMS, Telegram notifications
✅ **Docker Ready**: Full containerized deployment
✅ **Production Ready**: Render deployment active at bhiv-hr-langgraph.onrender.com

The BHIV HR Platform uses LangGraph for comprehensive AI-powered workflow orchestration and automation.