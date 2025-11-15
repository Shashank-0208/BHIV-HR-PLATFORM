# 🚀 Render Deployment Steps for LangGraph Service

## 📋 Pre-Deployment Checklist

### 1. Local Testing
```bash
# Run complete local test
python test_local_complete.py

# Start all services
docker-compose -f deployment/docker/docker-compose.production.yml up -d

# Verify LangGraph specifically
curl http://localhost:9001/health
```

### 2. Environment Variables Required
```env
DATABASE_URL=postgresql://username:password@host:port/database
OPENAI_API_KEY=sk-your-openai-api-key
GATEWAY_URL=https://bhiv-hr-gateway-ltg0.onrender.com
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## 🌐 Render Deployment Process

### Step 1: Create New Web Service
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select branch: `main`

### Step 2: Service Configuration
```yaml
Name: bhiv-hr-langgraph
Environment: Python 3
Region: Oregon (US West)
Branch: main
Build Command: pip install -r services/langgraph/requirements.txt
Start Command: cd services/langgraph && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 3: Environment Variables
Add these in Render dashboard:
- `DATABASE_URL`: Your PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `GATEWAY_URL`: https://bhiv-hr-gateway-ltg0.onrender.com
- `ENVIRONMENT`: production
- `LOG_LEVEL`: INFO

### Step 4: Advanced Settings
```yaml
Auto-Deploy: Yes
Health Check Path: /health
Docker Command: (leave empty)
Root Directory: services/langgraph
```

## 🔧 Gateway Integration Update

### Update Gateway Service
Add LangGraph URL to Gateway environment variables:
```env
LANGGRAPH_URL=https://bhiv-hr-langgraph-[your-id].onrender.com
```

### Test Integration
```bash
# Test Gateway → LangGraph connection
curl -H "Authorization: Bearer your-api-key" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/workflow/test
```

## 📊 Post-Deployment Verification

### 1. Service Health Check
```bash
curl https://bhiv-hr-langgraph-[your-id].onrender.com/health
```

### 2. Workflow Test
```bash
curl -X POST https://bhiv-hr-langgraph-[your-id].onrender.com/workflow/start \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "candidate_name": "Test User",
       "candidate_email": "test@example.com",
       "job_title": "Software Engineer"
     }'
```

### 3. Integration Test
```bash
python test_integration.py  # Update URLs to production
```

## 🎯 Expected Results

### Service Status
- **LangGraph Service**: ✅ https://bhiv-hr-langgraph-[id].onrender.com
- **Health Check**: ✅ Returns {"status": "healthy"}
- **Workflow Endpoints**: ✅ 8 endpoints operational
- **AI Agents**: ✅ 4 agents (screener, notification, hr_update, feedback)

### Updated Platform Status
```
Total Services: 6/6 ✅
- Gateway: bhiv-hr-gateway-ltg0.onrender.com (82 endpoints)
- Agent: bhiv-hr-agent-nhgg.onrender.com (6 endpoints)  
- LangGraph: bhiv-hr-langgraph-[id].onrender.com (8 endpoints) ← NEW
- HR Portal: bhiv-hr-portal-u670.onrender.com
- Client Portal: bhiv-hr-client-portal-3iod.onrender.com
- Candidate Portal: bhiv-hr-candidate-portal-abe6.onrender.com
```

## 🚨 Troubleshooting

### Common Issues
1. **Build Fails**: Check requirements.txt path
2. **Start Fails**: Verify uvicorn command and port binding
3. **Health Check Fails**: Ensure /health endpoint returns 200
4. **OpenAI Errors**: Verify API key is valid and has credits

### Debug Commands
```bash
# Check Render logs
# Go to service dashboard → Logs tab

# Test locally first
docker run -p 9001:9001 -e PORT=9001 your-langgraph-image

# Verify environment variables
curl https://your-service.onrender.com/debug/env
```

## 📈 Success Metrics
- ✅ Service deploys successfully
- ✅ Health check returns 200
- ✅ All 8 endpoints respond
- ✅ Workflow execution completes
- ✅ Integration with Gateway works
- ✅ AI agents process requests
- ✅ Notifications are sent