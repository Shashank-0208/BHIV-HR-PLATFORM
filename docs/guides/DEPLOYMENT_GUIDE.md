# 🚀 BHIV HR Platform - Critical Issues Deployment Guide

## 📋 **Issues to Fix:**
1. **Database Schema v4.2.0** - Missing columns and tables
2. **Gateway Service** - AI Agent URL connection

---

## 🗄️ **STEP 1: Deploy Database Schema (CRITICAL)**

### **1.1 Access Render PostgreSQL Console**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your PostgreSQL service: `bhiv-hr-jcuu-w5fl`
3. Click **"Connect"** tab
4. Click **"External Connection"**
5. Copy the connection command

### **1.2 Execute Schema Update**
**Option A: Via Render Web Console (Recommended)**
1. In Render PostgreSQL service, click **"Connect"** → **"Web Console"**
2. Execute these SQL commands one by one:

```sql
-- Add missing columns to clients table
ALTER TABLE clients 
ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP;

-- Update existing records
UPDATE clients 
SET failed_login_attempts = 0 
WHERE failed_login_attempts IS NULL;

-- Create job_applications table
CREATE TABLE IF NOT EXISTS job_applications (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL REFERENCES candidates(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    cover_letter TEXT,
    status VARCHAR(50) DEFAULT 'applied' CHECK (status IN ('applied', 'reviewed', 'shortlisted', 'rejected', 'withdrawn')),
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(candidate_id, job_id)
);

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_job_applications_candidate ON job_applications(candidate_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_job ON job_applications(job_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_status ON job_applications(status);
CREATE INDEX IF NOT EXISTS idx_job_applications_date ON job_applications(applied_date);

-- Update schema version
INSERT INTO schema_version (version, description) VALUES 
('4.2.0', 'Production schema with job_applications table and client auth fixes')
ON CONFLICT (version) DO UPDATE SET applied_at = CURRENT_TIMESTAMP;
```

**Option B: Via Command Line (If you have psql)**
```bash
psql "postgresql://<username>:<password>@<host>:<port>/<database>schema_production.sql
```

---

## 🌐 **STEP 2: Redeploy Gateway Service (CRITICAL)**

### **2.1 Access Gateway Service**
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on **"bhiv-hr-gateway-ltg0"** service

### **2.2 Force Redeploy**
1. Click **"Manual Deploy"** button
2. Select **"Deploy latest commit"**
3. Click **"Deploy"**
4. Wait for deployment to complete (2-3 minutes)

---

## ✅ **STEP 3: Verify Deployment**

### **3.1 Test Database Schema**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"client_id":"TECH001","password":"demo123"}' \
https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login
```
**Expected:** Should return success with JWT token

### **3.2 Test AI Matching**
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
https://bhiv-hr-gateway-ltg0.onrender.com/v1/match/1/top
```
**Expected:** Should show `"agent_status": "connected"` and Phase 3 algorithm

### **3.3 Check Schema Version**
```bash
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/schema
```
**Expected:** Should show `"schema_version": "4.2.0"`

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
- ✅ Client login returns JWT token
- ✅ AI matching shows "agent_status": "connected"
- ✅ Schema version shows "4.2.0"
- ✅ All 85 endpoints functional

**Estimated Time:** 10-15 minutes total
