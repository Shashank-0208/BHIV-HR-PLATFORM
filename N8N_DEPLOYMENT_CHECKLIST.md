# 🚀 N8N Integration Deployment Checklist

## Current Status ✅
- **Gateway Service**: Running and healthy (200 OK)
- **N8N Webhook Endpoints**: Deployed and accessible (3/3 endpoints responding)
- **Issue**: `notification_service` module not found on deployed service
- **N8N Routes**: Not included in deployment (404 errors)

## 📋 Step-by-Step Deployment Guide

### Step 1: Add N8N Environment Variables to Render ⚙️

1. **Go to Render Dashboard**:
   - Visit https://dashboard.render.com
   - Navigate to your `bhiv-hr-gateway` service

2. **Add Environment Variables**:
   ```
   N8N_GMAIL_WEBHOOK=https://bhivhrplatform.app.n8n.cloud/webhook/1a108336-bfad-489c-8c38-4f907045a2ed
   N8N_WHATSAPP_WEBHOOK=https://bhivhrplatform.app.n8n.cloud/webhook/aafbb77b-2dce-41c1-8c34-33fef4cb8ead
   N8N_TELEGRAM_WEBHOOK=https://bhivhrplatform.app.n8n.cloud/webhook/17543422-01c7-4f75-ad76-9504c5fc9499
   ```

3. **Save and Deploy**:
   - Click "Save Changes"
   - This will trigger an automatic redeployment

### Step 2: Verify File Structure 📁

Ensure these files exist in your repository:
```
services/gateway/app/
├── main.py                    ✅ (contains N8N webhook endpoints)
├── notification_service.py   ✅ (N8N notification service)
└── n8n_routes.py             ✅ (additional N8N routes)
```

### Step 3: Test N8N Integration 🧪

After deployment completes, run these tests:

```bash
# Test 1: Basic webhook functionality
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/webhooks/candidate-applied" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Test User",
    "job_title": "Software Engineer", 
    "email": "test@example.com",
    "phone": "+1234567890"
  }'

# Test 2: Check if notification service is working
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/webhooks/candidate-shortlisted" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Test User",
    "job_title": "Software Engineer",
    "email": "test@example.com"
  }'

# Test 3: Interview scheduling webhook
curl -X POST "https://bhiv-hr-gateway-ltg0.onrender.com/webhooks/interview-scheduled" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Test User",
    "job_title": "Software Engineer",
    "email": "test@example.com",
    "date": "2024-12-01",
    "time": "10:00 AM",
    "interviewer": "HR Team"
  }'
```

### Step 4: Manual Verification Steps 🔍

#### A. Check Render Deployment Logs
1. Go to Render Dashboard > bhiv-hr-gateway > Logs
2. Look for any import errors related to `notification_service`
3. Verify successful deployment completion

#### B. Verify N8N Workspace
1. Login to https://bhivhrplatform.app.n8n.cloud
2. Check workflow status:
   - **Gmail Notification Workflow**: Should be active
   - **WhatsApp Notification Workflow**: Should be active  
   - **Telegram Notification Workflow**: Should be active
3. Test webhook URLs manually in N8N interface

#### C. Test API Documentation
1. Visit https://bhiv-hr-gateway-ltg0.onrender.com/docs
2. Look for "N8N Webhooks" section with 3 endpoints:
   - `POST /webhooks/candidate-applied`
   - `POST /webhooks/candidate-shortlisted`
   - `POST /webhooks/interview-scheduled`

### Step 5: Notification Channel Testing 📧📱💬

#### Gmail Testing
- Send test notification to your email
- Check spam folder if not received
- Verify N8N Gmail workflow execution logs

#### WhatsApp Testing (Twilio Sandbox)
- Ensure phone number is verified in Twilio sandbox
- Send "join <sandbox-keyword>" to Twilio WhatsApp number first
- Test with verified phone number format: +1234567890

#### Telegram Testing
- Verify bot token is valid in N8N
- Get correct chat ID for testing
- Test with valid chat ID or @username

### Step 6: Expected Results ✅

After successful deployment, you should see:

1. **Webhook Responses**:
   ```json
   {
     "status": "n8n_workflows_triggered",
     "notification_result": {
       "status": "processed",
       "channels": ["email", "whatsapp"],
       "results": {
         "email": {"status": "sent", "response_code": 200},
         "whatsapp": {"status": "sent", "response_code": 200}
       }
     },
     "triggered_at": "2025-11-08T15:00:00Z"
   }
   ```

2. **Actual Notifications**:
   - Email received in inbox
   - WhatsApp message received (if sandbox configured)
   - Telegram message received (if bot configured)

### Step 7: Troubleshooting Guide 🔧

#### Issue: "No module named 'notification_service'"
**Solution**: 
- Verify `notification_service.py` is in `services/gateway/app/` directory
- Redeploy Gateway service
- Check deployment logs for file inclusion

#### Issue: N8N webhook returns 500 error
**Solution**:
- Check N8N workspace execution limits
- Verify webhook URLs are accessible
- Check N8N workflow configuration

#### Issue: Notifications not received
**Solution**:
- Verify email addresses are correct
- Check WhatsApp sandbox setup
- Validate Telegram bot token and chat IDs
- Monitor N8N execution logs

### Step 8: Monitoring and Maintenance 📊

1. **Set up monitoring**:
   - Track notification delivery rates
   - Monitor N8N execution limits
   - Set up alerts for failed notifications

2. **Regular checks**:
   - Verify N8N workspace is active
   - Check environment variables are set
   - Test notification channels monthly

## 🎯 Success Criteria

✅ All 3 N8N webhook endpoints return success responses  
✅ Notifications are delivered to all configured channels  
✅ N8N workspace shows successful executions  
✅ Environment variables are properly configured  
✅ No import errors in deployment logs  

## 📞 Next Steps After Deployment

1. **Test with real data**: Use actual candidate information
2. **Monitor performance**: Track notification delivery rates
3. **Scale if needed**: Upgrade N8N plan if execution limits reached
4. **Documentation**: Update API documentation with N8N integration details
5. **User training**: Train HR team on new notification features

---

**Total Endpoints After N8N Integration**: 88 (85 existing + 3 N8N webhooks)
**Estimated Deployment Time**: 5-10 minutes
**Testing Time**: 15-20 minutes