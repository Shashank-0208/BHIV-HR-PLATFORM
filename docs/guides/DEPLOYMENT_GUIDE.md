# 🚀 BHIV HR Platform - Complete Deployment Guide v4.2.0

## 📋 **Current System Status:**
- **Version**: 4.2.0 with LangGraph Integration
- **Services**: 6 operational (Gateway, Agent, LangGraph, HR Portal, Client Portal, Candidate Portal)
- **Database**: PostgreSQL 17 with Schema v4.2.0 (13 core tables)
- **Endpoints**: 107 total (94 Gateway + 6 Agent + 7 LangGraph)
- **Platform**: Render Cloud (6/6 services live)

---

## 🗄️ **STEP 1: Verify Current Deployment Status**

### **1.1 Check All Services Status**
```bash
# Gateway Service (94 endpoints)
curl https://bhiv-hr-gateway-ltg0.onrender.com/health

# AI Agent Service (6 endpoints)
curl https://bhiv-hr-agent-nhgg.onrender.com/health

# LangGraph Service (7 endpoints) - NEW
curl https://bhiv-hr-langgraph.onrender.com/health

# Portal Services
curl -I https://bhiv-hr-portal-u670.onrender.com/
curl -I https://bhiv-hr-client-portal-3iod.onrender.com/
curl -I https://bhiv-hr-candidate-portal-abe6.onrender.com/
```

### **1.2 Verify Database Schema v4.2.0**
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/schema
```
**Expected Response:**
```json
{
  "schema_version": "4.2.0",
  "tables": 13,
  "total_endpoints": 107,
  "services": 6
}
```

### **1.3 Test LangGraph Integration**
```bash
# Test workflow creation
curl -X POST "https://bhiv-hr-langgraph.onrender.com/workflows/application/start" \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "application_id": 123,
       "candidate_email": "test@example.com",
       "candidate_phone": "+1234567890",
       "candidate_name": "Test Candidate",
       "job_title": "Software Engineer"
     }'
```

---

## 🌐 **STEP 2: Deploy New Services (If Needed)**

### **2.1 LangGraph Service Deployment**
If LangGraph service is not deployed:

1. **Create New Web Service on Render:**
   - Repository: `https://github.com/shashankmishraa/BHIV-HR-Platform`
   - Root Directory: `services/langgraph`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Environment Variables:**
   ```
   GATEWAY_URL=https://bhiv-hr-gateway-ltg0.onrender.com
   API_KEY_SECRET=<YOUR_API_KEY>
   DATABASE_URL=<POSTGRESQL_URL>
   OPENAI_API_KEY=<YOUR_OPENAI_KEY>
   ENVIRONMENT=production
   ```

### **2.2 Update Gateway Integration**
Ensure Gateway service includes LangGraph endpoints:

1. **Verify LangGraph Integration:**
   ```bash
   curl -H "Authorization: Bearer <YOUR_API_KEY>" \
        https://bhiv-hr-gateway-ltg0.onrender.com/api/v1/workflow/health
   ```

2. **Test Workflow Triggers:**
   ```bash
   curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
        -H "Content-Type: application/json" \
        https://bhiv-hr-gateway-ltg0.onrender.com/api/v1/workflow/trigger \
        -d '{"workflow_type": "candidate_application", "data": {}}'
   ```

---

## ✅ **STEP 3: Complete System Verification**

### **3.1 Verify All 107 Endpoints**
```bash
# Gateway Service (94 endpoints)
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs

# AI Agent Service (6 endpoints)
curl -X POST -H "Authorization: Bearer <YOUR_API_KEY>" \
     -H "Content-Type: application/json" \
     https://bhiv-hr-agent-nhgg.onrender.com/match \
     -d '{"candidate_id": 1, "job_id": 1}'

# LangGraph Service (7 endpoints)
curl https://bhiv-hr-langgraph.onrender.com/workflows
```

### **3.2 Test Complete Workflow**
```bash
# 1. Create workflow
WORKFLOW_ID=$(curl -X POST "https://bhiv-hr-langgraph.onrender.com/workflows/application/start" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "application_id": 123,
    "candidate_email": "test@example.com",
    "candidate_phone": "+1234567890",
    "candidate_name": "Test Candidate",
    "job_title": "Software Engineer"
  }' | jq -r '.workflow_id')

# 2. Check workflow status
curl "https://bhiv-hr-langgraph.onrender.com/workflows/$WORKFLOW_ID/status"
```

### **3.3 Verify Portal Integration**
```bash
# Test client authentication
curl -X POST -H "Content-Type: application/json" \
     -d '{"client_id":"TECH001","password":"demo123"}' \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login

# Test candidate portal
curl -I https://bhiv-hr-candidate-portal-abe6.onrender.com/

# Test HR portal
curl -I https://bhiv-hr-portal-u670.onrender.com/
```

---

## 🔧 **Automated Verification**
Run the verification script:
```bash
python check_database_structure.py
```

---

## 📞 **Troubleshooting**

### **If Database Deployment Fails:**
- Check PostgreSQL connection in Render dashboard
- Verify SQL syntax in web console
- Try executing commands one by one

### **If Gateway Deployment Fails:**
- Check build logs in Render dashboard
- Verify GitHub repository is connected
- Try manual redeploy again

### **If Tests Still Fail:**
- Wait 2-3 minutes for services to fully restart
- Check service logs in Render dashboard
- Verify environment variables are set

---

## 🎯 **Success Criteria**
- ✅ All 6 services operational (Gateway, Agent, LangGraph, HR Portal, Client Portal, Candidate Portal)
- ✅ All 107 endpoints functional (94 Gateway + 6 Agent + 7 LangGraph)
- ✅ Database schema v4.2.0 with 13 core tables
- ✅ LangGraph workflows creating and processing successfully
- ✅ Client authentication returns JWT tokens
- ✅ AI matching shows Phase 3 algorithm connectivity
- ✅ Multi-channel notifications working in development mode
- ✅ All portal services accessible and responsive

**Estimated Time:** 15-20 minutes total
**Current Status:** 🟪 6/6 Services Operational
**Last Updated:** November 15, 2025
