# 🔧 Render Environment Variables Guide

⚠️ **SECURITY WARNING**: This guide uses placeholder values. Never commit actual credentials to version control.

## 📋 Service-Specific Environment Variables

### **Gateway Service (bhiv-hr-gateway)**
```bash
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_JWT_SECRET_KEY]
CANDIDATE_JWT_SECRET=[YOUR_CANDIDATE_JWT_SECRET]
AGENT_SERVICE_URL=https://[YOUR_AGENT_SERVICE_URL]
```

### **Agent Service (bhiv-hr-agent)**
```bash
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_JWT_SECRET_KEY]
```

### **LangGraph Workflow Service (bhiv-hr-langgraph)**
```bash
# Core Configuration
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
GATEWAY_URL=https://[YOUR_GATEWAY_URL]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
JWT_SECRET_KEY=[YOUR_JWT_SECRET_KEY]
CANDIDATE_JWT_SECRET=[YOUR_CANDIDATE_JWT_SECRET]
ENVIRONMENT=production
LOG_LEVEL=INFO

# AI Configuration (Optional but recommended)
OPENAI_API_KEY=[YOUR_OPENAI_API_KEY]
OPENAI_MODEL=gpt-4-turbo-preview

# Communication Services (Optional)
TWILIO_ACCOUNT_SID=[YOUR_TWILIO_SID]
TWILIO_AUTH_TOKEN=[YOUR_TWILIO_TOKEN]
TWILIO_WHATSAPP_NUMBER=+14155238886

# Email Configuration (Optional)
GMAIL_EMAIL=[YOUR_EMAIL@gmail.com]
GMAIL_APP_PASSWORD=[YOUR_APP_PASSWORD]

# Telegram Configuration (Optional)
TELEGRAM_BOT_TOKEN=[YOUR_TELEGRAM_BOT_TOKEN]
TELEGRAM_BOT_USERNAME=@[YOUR_BOT_USERNAME]
```

### **HR Portal Service (bhiv-hr-portal)**
```bash
GATEWAY_URL=https://[YOUR_GATEWAY_URL]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
AGENT_SERVICE_URL=https://[YOUR_AGENT_SERVICE_URL]
LANGGRAPH_SERVICE_URL=https://[YOUR_LANGGRAPH_SERVICE_URL]
```

### **Client Portal Service (bhiv-hr-client-portal)**
```bash
GATEWAY_URL=https://[YOUR_GATEWAY_URL]
API_KEY_SECRET=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_JWT_SECRET_KEY]
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
AGENT_SERVICE_URL=https://[YOUR_AGENT_SERVICE_URL]
LANGGRAPH_SERVICE_URL=https://[YOUR_LANGGRAPH_SERVICE_URL]
```

### **Candidate Portal Service (bhiv-hr-candidate-portal)**
```bash
GATEWAY_URL=https://[YOUR_GATEWAY_URL]
API_KEY=[YOUR_SECURE_API_KEY]
JWT_SECRET=[YOUR_CANDIDATE_JWT_SECRET]
DATABASE_URL=postgresql://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]
LANGGRAPH_SERVICE_URL=https://[YOUR_LANGGRAPH_SERVICE_URL]
```

## 🔒 Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate credentials** regularly
4. **Use strong, unique secrets** for each environment
5. **Limit access** to production credentials

## 🔧 Setup Instructions

1. Access Render Dashboard
2. Select your service
3. Go to Environment tab
4. Add variables with your actual values
5. Deploy changes

## 🧪 Testing

```bash
# Test with your actual API key
curl -H "Authorization: Bearer [YOUR_API_KEY]" \
     https://[YOUR_GATEWAY_URL]/health
```

*Last Updated: November 15, 2025*
