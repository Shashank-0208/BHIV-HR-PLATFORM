# 🎯 N8N No-Code Automation - External N8N Approach
## BHIV HR Platform Integration (Visual Workflows)

**Cost**: $0/month (N8N Cloud Free + Render Free Tier)  
**Approach**: Use N8N.cloud external service + minimal webhook endpoints  
**Timeline**: 1-2 Days  
**Focus**: **NO-CODE visual workflows** as per task requirements

---

## 🎯 No-Code Strategy (As Per Task PDF)

Following the 7-day task requirements:
- ✅ **N8N Cloud Free Tier**: Visual workflow editor (no hosting needed)
- ✅ **No-code automation**: Drag-and-drop workflow creation
- ✅ **External channels**: Gmail, WhatsApp (Twilio), Telegram
- ✅ **API integration**: Connect to your BHIV Gateway
- ✅ **Render Free Tier**: Only add minimal webhook endpoints

---

## 🚀 Step 1: N8N Cloud Setup (Manual - 10 minutes)

### **Create N8N Cloud Account**
1. Go to [n8n.cloud](https://n8n.cloud)
2. Sign up for **Free Plan** (5,000 workflow executions/month)
3. Create workspace: "BHIV-HR-Automation"
4. Access your N8N editor at: `https://your-workspace.app.n8n.cloud`

### **N8N Cloud Free Tier Limits:**
- ✅ **5,000 executions/month** (sufficient for HR automation)
- ✅ **Unlimited workflows**
- ✅ **All integrations** (Gmail, Twilio, Telegram, HTTP)
- ✅ **Visual editor** (drag-and-drop)
- ✅ **No hosting required**

---

## 📧 Step 2: Gmail Integration (N8N Visual - 15 minutes)

### **Setup Gmail Credentials in N8N:**
1. In N8N Cloud → Settings → Credentials
2. Add "Gmail OAuth2 API" credential
3. Follow OAuth flow to connect your Gmail
4. Test connection

### **Create Email Workflow (Visual):**
1. **New Workflow**: "BHIV Email Notifications"
2. **Drag nodes**:
   ```
   [Webhook] → [Switch] → [Gmail] → [Respond to Webhook]
   ```

3. **Configure Webhook Node:**
   - Method: POST
   - Path: `email-trigger`
   - Response: Immediately

4. **Configure Switch Node:**
   - Route by: `{{ $json.event }}`
   - Routes: application_received, shortlisted, interview_scheduled, offer_sent

5. **Configure Gmail Nodes (4 branches):**
   ```
   Branch 1 (application_received):
   To: {{ $json.recipient_email }}
   Subject: Thank you for applying to {{ $json.variables.job_title }}
   Body: Hi {{ $json.recipient_name }}, we received your application...
   
   Branch 2 (shortlisted):
   Subject: Congratulations! You're shortlisted for {{ $json.variables.job_title }}
   Body: Hi {{ $json.recipient_name }}, great news! We'd like to move forward...
   
   Branch 3 (interview_scheduled):
   Subject: Interview scheduled for {{ $json.variables.date }}
   Body: Hi {{ $json.recipient_name }}, your interview is on {{ $json.variables.date }}...
   
   Branch 4 (offer_sent):
   Subject: Job offer for {{ $json.variables.job_title }}
   Body: Hi {{ $json.recipient_name }}, we're pleased to offer you...
   ```

6. **Activate Workflow**
7. **Copy Webhook URL**: `https://your-workspace.app.n8n.cloud/webhook/email-trigger`

---

## 📱 Step 3: WhatsApp Integration (N8N Visual - 20 minutes)

### **Setup Twilio Credentials:**
1. Create Twilio account → Get Account SID, Auth Token
2. In N8N → Add "Twilio API" credential
3. Enter SID and Token

### **Create WhatsApp Workflow (Visual):**
1. **New Workflow**: "BHIV WhatsApp Notifications"
2. **Drag nodes**:
   ```
   [Webhook] → [Switch] → [HTTP Request (Twilio)] → [Respond]
   ```

3. **Configure Webhook:**
   - Path: `whatsapp-trigger`

4. **Configure Switch:**
   - Route by: `{{ $json.template_type }}`
   - Routes: status_update, interview_reminder, offer_notification

5. **Configure HTTP Request (Twilio API):**
   ```
   Method: POST
   URL: https://api.twilio.com/2010-04-01/Accounts/{{ $credentials.twilio.accountSid }}/Messages.json
   Authentication: Basic Auth (use Twilio credential)
   
   Body (Form):
   From: whatsapp:+14155238886
   To: whatsapp:{{ $json.phone_number }}
   Body: {{ $json.message }}
   ```

6. **Message Templates in Switch branches:**
   ```
   status_update: "Hi {{ $json.candidate_name }}! Your application for {{ $json.job_title }} is now {{ $json.status }}."
   interview_reminder: "Reminder: Your interview for {{ $json.job_title }} is tomorrow at {{ $json.time }}."
   offer_notification: "Congratulations {{ $json.candidate_name }}! 🎉 We're offering you {{ $json.job_title }}."
   ```

7. **Activate Workflow**
8. **Copy Webhook URL**: `https://your-workspace.app.n8n.cloud/webhook/whatsapp-trigger`

---

## 🤖 Step 4: Telegram Bot (N8N Visual - 25 minutes)

### **Setup Telegram Bot:**
1. Message @BotFather → Create bot: "BHIV HR Bot"
2. Get bot token
3. In N8N → Add "Telegram Bot API" credential

### **Create Telegram Workflow (Visual):**
1. **New Workflow**: "BHIV Telegram Bot"
2. **Drag nodes**:
   ```
   [Telegram Trigger] → [Switch] → [HTTP Request] → [Telegram Send]
   ```

3. **Configure Telegram Trigger:**
   - Bot Token: (your bot token)
   - Updates: Message

4. **Configure Switch (Command Router):**
   - Route by: `{{ $json.message.text }}`
   - Routes: /start, /status, /interview, /feedback

5. **Configure HTTP Request (API calls to BHIV Gateway):**
   ```
   For /status:
   URL: https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidate/applications/{{ $json.message.from.id }}
   Headers: Authorization: Bearer YOUR_API_KEY
   
   For /interview:
   URL: https://bhiv-hr-gateway-ltg0.onrender.com/v1/interviews
   Headers: Authorization: Bearer YOUR_API_KEY
   ```

6. **Configure Telegram Send Response:**
   ```
   /start: "Welcome to BHIV HR Bot! 🤖\nCommands: /status, /interview, /feedback"
   /status: "Your Applications:\n{{ $json.applications[0].job_title }} - Status: {{ $json.applications[0].status }}"
   /interview: "📅 Interview: {{ $json.date }} at {{ $json.time }}"
   ```

7. **Activate Workflow**

---

## 🔗 Step 5: Minimal Gateway Integration (Code - 15 minutes)

### **Add Only Webhook Endpoints to Gateway**
Add to `services/gateway/app/main.py`:

```python
import httpx

# N8N Webhook Integration (Minimal Code)
@app.post("/webhooks/candidate-applied", tags=["N8N Triggers"])
async def trigger_candidate_applied(request: Request):
    """Trigger N8N workflows when candidate applies"""
    payload = await request.json()
    
    # Trigger N8N Email Workflow
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://your-workspace.app.n8n.cloud/webhook/email-trigger",
            json={
                "event": "application_received",
                "recipient_email": payload["email"],
                "recipient_name": payload["name"],
                "variables": {
                    "job_title": payload["job_title"],
                    "company": "BHIV Partners"
                }
            }
        )
        
        # Trigger WhatsApp if phone provided
        if payload.get("phone"):
            await client.post(
                "https://your-workspace.app.n8n.cloud/webhook/whatsapp-trigger",
                json={
                    "template_type": "status_update",
                    "phone_number": payload["phone"],
                    "candidate_name": payload["name"],
                    "job_title": payload["job_title"],
                    "status": "received"
                }
            )
    
    return {"status": "n8n_workflows_triggered"}

@app.post("/webhooks/candidate-shortlisted", tags=["N8N Triggers"])
async def trigger_candidate_shortlisted(request: Request):
    """Trigger N8N when candidate is shortlisted"""
    payload = await request.json()
    
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://your-workspace.app.n8n.cloud/webhook/email-trigger",
            json={
                "event": "shortlisted",
                "recipient_email": payload["email"],
                "recipient_name": payload["name"],
                "variables": {"job_title": payload["job_title"]}
            }
        )
    
    return {"status": "shortlist_notification_triggered"}

@app.post("/webhooks/interview-scheduled", tags=["N8N Triggers"])
async def trigger_interview_scheduled(request: Request):
    """Trigger N8N when interview is scheduled"""
    payload = await request.json()
    
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://your-workspace.app.n8n.cloud/webhook/email-trigger",
            json={
                "event": "interview_scheduled",
                "recipient_email": payload["email"],
                "recipient_name": payload["name"],
                "variables": {
                    "job_title": payload["job_title"],
                    "date": payload["date"],
                    "time": payload["time"],
                    "interviewer": payload.get("interviewer", "HR Team")
                }
            }
        )
    
    return {"status": "interview_notification_triggered"}
```

### **Update requirements.txt (Minimal):**
```
httpx==0.25.2
```

---

## 🧪 Step 6: Testing No-Code Workflows

### **Test Email Workflow:**
```bash
curl -X POST https://your-workspace.app.n8n.cloud/webhook/email-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "event": "application_received",
    "recipient_email": "test@example.com",
    "recipient_name": "John Doe",
    "variables": {
      "job_title": "Senior Developer",
      "company": "TechCorp"
    }
  }'
```

### **Test WhatsApp Workflow:**
```bash
curl -X POST https://your-workspace.app.n8n.cloud/webhook/whatsapp-trigger \
  -H "Content-Type: application/json" \
  -d '{
    "template_type": "status_update",
    "phone_number": "+1234567890",
    "candidate_name": "John Doe",
    "job_title": "Senior Developer",
    "status": "shortlisted"
  }'
```

### **Test Gateway Integration:**
```bash
curl -X POST https://bhiv-hr-gateway-ltg0.onrender.com/webhooks/candidate-applied \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "John Doe",
    "phone": "+1234567890",
    "job_title": "Senior Developer"
  }'
```

---

## 📊 No-Code Benefits

### **Cost Breakdown:**
- **N8N Cloud Free**: $0/month (5,000 executions)
- **Render Services**: $0/month (existing free tier)
- **External APIs**: ~$5/month (Twilio, minimal usage)
- **Total**: ~$5/month

### **No-Code Features:**
✅ **Visual workflow editor** (drag-and-drop)  
✅ **No coding required** for workflow logic  
✅ **Built-in integrations** (Gmail, Twilio, Telegram)  
✅ **Workflow monitoring** and execution history  
✅ **Error handling** and retry logic  
✅ **Template management** with variables  
✅ **Real-time testing** in N8N editor

### **Learning Objectives Met:**
✅ **Creating triggers** (webhook nodes)  
✅ **Gmail/Outlook integration** (OAuth2 setup)  
✅ **WhatsApp via Twilio** (HTTP request nodes)  
✅ **Telegram bots** (Telegram trigger/send nodes)  
✅ **API call nodes** (HTTP requests to BHIV Gateway)

---

## 🎯 Implementation Steps

### **Phase 1: N8N Cloud Setup (30 minutes)**
1. Create N8N Cloud account
2. Setup Gmail OAuth2 credentials
3. Setup Twilio API credentials
4. Create Telegram bot and add credentials

### **Phase 2: Visual Workflows (60 minutes)**
1. Create Email workflow (4 templates)
2. Create WhatsApp workflow (3 message types)
3. Create Telegram bot workflow (4 commands)
4. Test each workflow individually

### **Phase 3: Gateway Integration (15 minutes)**
1. Add 3 webhook endpoints to Gateway
2. Deploy Gateway updates
3. Test end-to-end integration

### **Phase 4: Portal Integration (30 minutes)**
1. Add webhook calls to HR Portal actions
2. Add webhook calls to Client Portal actions
3. Test complete candidate journey

---

## 🔧 Workflow Monitoring

### **N8N Cloud Dashboard:**
- **Executions**: View all workflow runs
- **Logs**: Debug failed executions
- **Performance**: Monitor execution times
- **Errors**: Handle failed workflows

### **Success Metrics:**
- **Email delivery rate**: >95%
- **WhatsApp delivery rate**: >90%
- **Telegram response time**: <2 seconds
- **Workflow execution time**: <5 seconds
- **Error rate**: <5%

---

## 🚀 Next Steps

Once no-code workflows are operational:
1. **Add more triggers** (job posted, offer sent, feedback received)
2. **Enhance templates** with HTML formatting
3. **Add conditional logic** (send WhatsApp only if phone exists)
4. **Create workflow analytics** dashboard
5. **Scale to handle higher volume**

---

**N8N No-Code Automation Complete!**  
*Visual workflow automation without coding*

**Platform**: N8N Cloud Free Tier  
**Cost**: $0/month (N8N) + $0/month (Render)  
**Features**: Email + WhatsApp + Telegram automation  
**Approach**: 100% visual, no-code workflows