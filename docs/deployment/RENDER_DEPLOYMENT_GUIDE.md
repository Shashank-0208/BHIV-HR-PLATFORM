# 🚀 BHIV HR Platform - Render Deployment Guide

## 📋 Current Deployment Status

✅ **SUCCESSFULLY DEPLOYED ON RENDER**

| Service | URL | Status |
|---------|-----|--------|
| **API Gateway** | https://bhiv-hr-gateway-ltg0.onrender.com/docs | ✅ Live (74 endpoints) |
| **AI Matching Engine** | https://bhiv-hr-agent-nhgg.onrender.com/docs | ✅ Live (6 endpoints) |
| **LangGraph Workflows** | https://bhiv-hr-langgraph.onrender.com/docs | ✅ Live (9 endpoints) |
| **HR Portal** | https://bhiv-hr-portal-u670.onrender.com/ | ✅ Live |
| **Client Portal** | https://bhiv-hr-client-portal-3iod.onrender.com/ | ✅ Live |
| **Candidate Portal** | https://bhiv-hr-candidate-portal-abe6.onrender.com/ | ✅ Live |
| **Database** | PostgreSQL 17 (Internal) | ✅ Live |

## 🎯 Quick Access

### 🌐 Production URLs
- **API Documentation**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
- **HR Dashboard**: https://bhiv-hr-portal-u670.onrender.com/
- **Client Login**: https://bhiv-hr-client-portal-3iod.onrender.com/
  - Username: `TECH001`
  - Password: `demo123`

### 🔧 API Testing
```bash
# Health Check
curl https://bhiv-hr-gateway-ltg0.onrender.com/health

# Test Authentication
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs

# AI Matching Test
curl https://bhiv-hr-agent-nhgg.onrender.com/health

# LangGraph Workflows Test
curl https://bhiv-hr-langgraph.onrender.com/health
```

## 📊 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Render Cloud Platform                    │
│                     Oregon (US West)                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   PostgreSQL    │  │   API Gateway   │  │  AI Agent    │ │
│  │   Database      │  │   (FastAPI)     │  │  (FastAPI)   │ │
│  │   Port: 5432    │  │   Port: 8000    │  │  Port: 9000  │ │
│  │   Free Tier     │  │   74 Endpoints  │  │  Matching    │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│           │                     │                    │      │
│           └─────────────────────┼────────────────────┘      │
│                                 │                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   HR Portal     │  │  Client Portal  │  │  LangGraph   │ │
│  │  (Streamlit)    │  │  (Streamlit)    │  │  Workflows   │ │
│  │   Port: 8501    │  │   Port: 8502    │  │  Port: 9001  │ │
│  │   Dashboard     │  │   Client UI     │  │  9 Endpoints │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                             │
│  ┌─────────────────┐                                       │
│  │ Candidate Portal│                                       │
│  │  (Streamlit)    │                                       │
│  │   Port: 8503    │                                       │
│  │   Candidate UI  │                                       │
│  └─────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Service Configuration Details

### 1. Database Service
```yaml
Name: bhiv-hr-database
Type: PostgreSQL
Plan: Free (1GB storage)
Database: bhiv_hr
User: bhiv_user
Version: 17
Region: Oregon (US West)
```

### 2. API Gateway Service
```yaml
Name: bhiv-hr-gateway
Type: Web Service
Plan: Free
Root Directory: services/gateway
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Environment Variables:
  - DATABASE_URL: [Internal PostgreSQL URL]
  - API_KEY_SECRET: <YOUR_API_KEY>
  - JWT_SECRET_KEY: <YOUR_JWT_SECRET_KEY>
  - CANDIDATE_JWT_SECRET_KEY: <YOUR_CANDIDATE_JWT_SECRET_KEY>
  - AGENT_SERVICE_URL: https://bhiv-hr-agent-nhgg.onrender.com
  - LANGGRAPH_SERVICE_URL: https://bhiv-hr-langgraph.onrender.com
Service Structure:
  - app/main.py: FastAPI application entry point
  - routes/: API route definitions (auth.py, ai_integration.py, rl_routes.py)
  - logs/: Service-specific logs
  - Dockerfile: Container configuration for Render deployment
```

### 3. AI Agent Service
```yaml
Name: bhiv-hr-agent
Type: Web Service
Plan: Free
Root Directory: services/agent
Build Command: pip install -r requirements.txt
Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT
Environment Variables:
  - DATABASE_URL: [Internal PostgreSQL URL]
  - API_KEY_SECRET: <YOUR_API_KEY>
  - JWT_SECRET_KEY: <YOUR_JWT_SECRET_KEY>
  - CANDIDATE_JWT_SECRET_KEY: <YOUR_CANDIDATE_JWT_SECRET_KEY>
Service Structure:
  - app.py: FastAPI application with AI matching endpoints
  - semantic_engine/: Phase 3 semantic matching engine
  - Dockerfile: Container configuration for Render deployment
```

### 4. LangGraph Workflow Service
```yaml
Name: bhiv-hr-langgraph
Type: Web Service
Plan: Free
Language: Docker
Root Directory: services/langgraph
Build Command: [Empty - Docker handles this]
Start Command: [Empty - Docker handles this]
Docker Build Context Directory: services/langgraph
Dockerfile Path: services/langgraph/Dockerfile
Environment Variables:
  - DATABASE_URL: [Internal PostgreSQL URL]
  - GATEWAY_SERVICE_URL: https://bhiv-hr-gateway-ltg0.onrender.com
  - API_KEY_SECRET: <YOUR_API_KEY>
  - JWT_SECRET_KEY: <YOUR_JWT_SECRET_KEY>
  - CANDIDATE_JWT_SECRET_KEY: <YOUR_CANDIDATE_JWT_SECRET_KEY>
  - ENVIRONMENT: production
  - LOG_LEVEL: INFO
  - TWILIO_ACCOUNT_SID: <TWILIO_SID>
  - TWILIO_AUTH_TOKEN_SECRET_KEY: <TWILIO_TOKEN>
  - TWILIO_WHATSAPP_NUMBER: +14155238886
  - GMAIL_EMAIL: <GMAIL_EMAIL>
  - GMAIL_APP_PASSWORD_SECRET_KEY: <GMAIL_APP_PASSWORD>
  - TELEGRAM_BOT_TOKEN_SECRET_KEY: <TELEGRAM_BOT_TOKEN>
  - TELEGRAM_BOT_USERNAME: <TELEGRAM_BOT_USERNAME>
  - OPENAI_API_SECRET_KEY: <OPENAI_API_KEY>
  - OPENAI_MODEL: gpt-4-turbo-preview
```

### 5. HR Portal Service
```yaml
Name: bhiv-hr-portal
Type: Web Service
Plan: Free
Root Directory: services/portal
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Environment Variables:
  - GATEWAY_SERVICE_URL: https://bhiv-hr-gateway-ltg0.onrender.com
  - AGENT_SERVICE_URL: https://bhiv-hr-agent-nhgg.onrender.com
  - LANGGRAPH_SERVICE_URL: https://bhiv-hr-langgraph.onrender.com
  - API_KEY_SECRET: <YOUR_API_KEY>
  - JWT_SECRET_KEY: <YOUR_JWT_SECRET_KEY>
  - CANDIDATE_JWT_SECRET_KEY: <YOUR_CANDIDATE_JWT_SECRET_KEY>
Service Structure:
  - app.py: Main Streamlit application with HR dashboard
  - auth_manager.py: Authentication management for portal
  - components/: Reusable UI components (2FA setup)
  - Dockerfile: Container configuration for Render deployment
```

### 6. Client Portal Service
```yaml
Name: bhiv-hr-client-portal
Type: Web Service
Plan: Free
Root Directory: services/client_portal
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Environment Variables:
  - GATEWAY_SERVICE_URL: https://bhiv-hr-gateway-ltg0.onrender.com
  - AGENT_SERVICE_URL: https://bhiv-hr-agent-nhgg.onrender.com
  - LANGGRAPH_SERVICE_URL: https://bhiv-hr-langgraph.onrender.com
  - API_KEY_SECRET: <YOUR_API_KEY>
  - JWT_SECRET_KEY: <YOUR_JWT_SECRET_KEY>
  - DATABASE_URL: [Internal PostgreSQL URL]
Service Structure:
  - app.py: Streamlit application for client job management
  - auth_manager.py: Authentication management for client portal
  - Dockerfile: Container configuration for Render deployment
```

### 7. Candidate Portal Service
```yaml
Name: bhiv-hr-candidate-portal
Type: Web Service
Plan: Free
Root Directory: services/candidate_portal
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
Environment Variables:
  - GATEWAY_SERVICE_URL: https://bhiv-hr-gateway-ltg0.onrender.com
  - API_KEY_SECRET: <YOUR_API_KEY>
  - JWT_SECRET_KEY: <YOUR_JWT_SECRET_KEY>
  - CANDIDATE_JWT_SECRET_KEY: <YOUR_CANDIDATE_JWT_SECRET_KEY>
  - DATABASE_URL: [Internal PostgreSQL URL]
Service Structure:
  - app.py: Streamlit application for candidate job applications
  - auth_manager.py: Authentication management for candidate portal
  - Dockerfile: Container configuration for Render deployment
```

## 🚀 Deployment Process (Completed)

### Phase 1: Database Setup ✅
1. Created PostgreSQL service on Render
2. Configured database: `bhiv_hr`
3. Set user: `bhiv_user`
4. Obtained internal database URL

### Phase 2: API Gateway Deployment ✅
1. Connected GitHub repository
2. Set root directory: `services/gateway`
3. Configured build and start commands
4. Added environment variables
5. Service live at: https://bhiv-hr-gateway-ltg0.onrender.com

### Phase 3: AI Agent Deployment ✅
1. Deployed AI matching service
2. Connected to database
3. Service live at: https://bhiv-hr-agent-nhgg.onrender.com

### Phase 4: LangGraph Workflow Deployment ✅
1. Deployed LangGraph workflow service using Docker
2. Connected to database and Gateway
3. Service live at: https://bhiv-hr-langgraph.onrender.com
4. Configured workflow automation
5. Docker configuration:
   - Language: Docker
   - Build/Start Commands: Empty (Docker handles)
   - Docker Build Context: services/langgraph
   - Dockerfile Path: services/langgraph/Dockerfile
   - Uses dynamic PORT environment variable
   - No render.yaml file (uses Docker deployment like other services)

### Phase 5: Portal Deployments ✅
1. Deployed HR Portal (Streamlit)
2. Deployed Client Portal (Streamlit)
3. Deployed Candidate Portal (Streamlit)
4. Connected all portals to API Gateway
5. Configured authentication

## 📈 Performance & Monitoring

### Current Performance Metrics
- **API Response Time**: <100ms average
- **AI Matching Speed**: <0.02 seconds
- **Cold Start Time**: 30-60 seconds (free tier)
- **Uptime**: 99.9% target
- **Rate Limiting**: 60 requests/minute

### Monitoring Endpoints
```bash
# System Health
curl https://bhiv-hr-gateway-ltg0.onrender.com/health

# Detailed Health Check
curl https://bhiv-hr-gateway-ltg0.onrender.com/health/detailed

# Prometheus Metrics
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics

# Real-time Dashboard
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics/dashboard

# Database Status
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/test-candidates
```

## 🔒 Security Features

### Authentication & Authorization
- **API Key**: `<YOUR_API_KEY>`
- **Bearer Token**: Required for protected endpoints
- **Client Portal**: Username/Password authentication
- **Rate Limiting**: 60 requests/minute per IP

### Security Headers
- Content Security Policy (CSP)
- X-XSS-Protection
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security

### Additional Security
- Input validation (XSS/SQL injection protection)
- 2FA support (TOTP compatible)
- Password strength validation
- Automated security testing endpoints

## 💰 Cost Breakdown

### Current Costs (Free Tier)
- **Database**: $0/month (Free PostgreSQL)
- **API Gateway**: $0/month (Free web service)
- **AI Agent**: $0/month (Free web service)
- **LangGraph Service**: $0/month (Free web service)
- **HR Portal**: $0/month (Free web service)
- **Client Portal**: $0/month (Free web service)
- **Candidate Portal**: $0/month (Free web service)
- **Total**: $0/month

### Free Tier Limitations
- **Monthly Hours**: 750 hours total across all services
- **Sleep Timer**: Services sleep after 15 minutes of inactivity
- **Cold Starts**: 30-60 seconds wake-up time
- **Concurrent Requests**: Limited on free tier
- **Storage**: 1GB database storage

## 🔄 Maintenance & Updates

### Auto-Deployment
- **Enabled**: Automatic deployment on GitHub push
- **Branch**: `main`
- **Trigger**: Code changes in respective service directories

### Manual Operations
```bash
# Trigger manual deployment
# Use Render dashboard "Manual Deploy" button

# View logs
# Access through Render dashboard for each service

# Environment variable updates
# Update through Render dashboard settings
```

## 🧪 Testing & Validation

### API Endpoint Testing
```bash
# Test all core endpoints
curl https://bhiv-hr-gateway-ltg0.onrender.com/
curl https://bhiv-hr-gateway-ltg0.onrender.com/health
curl https://bhiv-hr-gateway-ltg0.onrender.com/docs

# Test authenticated endpoints
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs

curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/candidates/stats
```

### Portal Testing
1. **HR Portal**: Visit https://bhiv-hr-portal-u670.onrender.com/
2. **Client Portal**: Visit https://bhiv-hr-client-portal-3iod.onrender.com/
   - Login with: TECH001 / demo123
3. **API Documentation**: Visit https://bhiv-hr-gateway-ltg0.onrender.com/docs

### LangGraph Communication Testing
```bash
# Test complete workflow with real notifications
curl -X POST \
  https://bhiv-hr-langgraph.onrender.com/workflows/application/start \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "application_id": 1,
    "candidate_email": "test@example.com",
    "candidate_phone": "+14155238886",
    "candidate_name": "Test User",
    "job_title": "Software Engineer"
  }'

# Test direct notification
curl -X POST \
  https://bhiv-hr-langgraph.onrender.com/tools/send-notification \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Test User",
    "job_title": "Test Position",
    "message": "Test notification",
    "channels": ["email", "whatsapp"]
  }'
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Service Not Responding
- **Cause**: Service sleeping (15min inactivity)
- **Solution**: Wait 30-60 seconds for cold start

#### Database Connection Errors
- **Cause**: Database URL misconfiguration
- **Solution**: Verify DATABASE_URL environment variable

#### Authentication Failures
- **Cause**: Missing or incorrect API key
- **Solution**: Check API_KEY_SECRET environment variable

#### Build Failures
- **Cause**: Missing dependencies or incorrect paths
- **Solution**: Verify requirements.txt and root directory settings

### Debug Commands
```bash
# Check service health
curl https://bhiv-hr-gateway-ltg0.onrender.com/health

# Test database connectivity
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/test-candidates

# View API documentation
open https://bhiv-hr-gateway-ltg0.onrender.com/docs
```

## 📚 Additional Resources

### Documentation Links
- **API Documentation**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
- **GitHub Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
- **Render Dashboard**: https://dashboard.render.com/

### Support & Contact
- **Platform**: Render Cloud Platform
- **Region**: Oregon (US West)
- **Deployment Date**: January 3, 2025
- **Status**: Production Ready ✅

---

## 🎉 Deployment Success Summary

✅ **7/7 services successfully deployed on Render** (6 web services + 1 database)
✅ **Zero monthly cost (Free tier)**
✅ **Production-ready with 99.9% uptime target**
✅ **Comprehensive API with 89 endpoints (74 Gateway + 6 Agent + 9 LangGraph) including advanced monitoring**
✅ **AI-powered candidate matching (Phase 3 operational)**
✅ **LangGraph workflow automation with real multi-channel communications (Email, WhatsApp, Telegram)**
✅ **Triple portal system operational**
✅ **Enterprise-grade security features**

**BHIV HR Platform is now live and accessible worldwide! 🌍**
