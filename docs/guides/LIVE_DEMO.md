# 🌐 BHIV HR Platform - Live Demo Links

## 🚀 Production Deployment

### Render Cloud Platform
**Status**: ✅ Active  
**Region**: Oregon (US West)  
**Cost**: $0/month (Free tier)  

**Live Services**:
- **API Gateway**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
- **AI Matching Engine**: https://bhiv-hr-agent-nhgg.onrender.com/docs
- **LangGraph Workflows**: https://bhiv-hr-langgraph.onrender.com/docs
- **HR Portal**: https://bhiv-hr-portal-u670.onrender.com/
- **Client Portal**: https://bhiv-hr-client-portal-3iod.onrender.com/
- **Candidate Portal**: https://bhiv-hr-candidate-portal-abe6.onrender.com/

**Platform Resources**:
```
├── PostgreSQL Database: Internal Render service (1GB)
├── Web Services: 6 containerized applications
├── Auto-Deploy: GitHub integration enabled
├── HTTPS: SSL certificates included
├── Monitoring: Built-in health checks
├── Workflow Automation: LangGraph AI orchestration
└── Logs: Accessible via Render dashboard
```

## 🔧 Demo Credentials

### HR Portal Access
```
URL: https://bhiv-hr-portal-u670.onrender.com/
Authentication: Direct access (no login required)
Features: Full HR dashboard access
```

### Client Portal Access
```
URL: https://bhiv-hr-client-portal-3iod.onrender.com/

Demo Accounts:
├── TECH001 / demo123 (Technology Company)
├── STARTUP01 / startup123 (Startup Company)  
└── ENTERPRISE01 / enterprise123 (Enterprise Client)
```

### API Access
```
Base URL: https://bhiv-hr-gateway-ltg0.onrender.com
API Key: <YOUR_API_KEY>
Documentation: https://bhiv-hr-gateway-ltg0.onrender.com/docs
Health Check: https://bhiv-hr-gateway-ltg0.onrender.com/health
```

## 📊 Live Demo Features

### Real-Time Data
- **AI Matching**: <0.02s response time
- **Resume Processing**: 75-96% accuracy
- **API Endpoints**: 107 interactive endpoints (94 Gateway + 6 Agent + 7 LangGraph)
- **Security Features**: Rate limiting, 2FA, input validation

### Interactive Demos
1. **API Explorer**: Test all 107 endpoints via Swagger UI
2. **AI Matching**: Real-time candidate matching
3. **Workflow Automation**: LangGraph AI orchestration demos
4. **HR Dashboard**: Complete recruitment workflow
5. **Client Portal**: Job posting and candidate review
6. **Candidate Portal**: Job seeker interface and applications
7. **Security Testing**: 2FA, password policies, penetration testing

## 🔍 Interactive API Explorer

### Swagger UI
**URL**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
**Features**:
- 107 interactive endpoints (94 Gateway + 6 Agent + 7 LangGraph)
- Real-time API testing
- Workflow automation demos
- Authentication examples
- Response schemas
- Advanced monitoring endpoints

### Quick API Tests
```bash
# Health Check
curl https://bhiv-hr-gateway-ltg0.onrender.com/health

# API Root
curl https://bhiv-hr-gateway-ltg0.onrender.com/

# Authenticated Endpoint
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/jobs

# AI Agent Health
curl https://bhiv-hr-agent-nhgg.onrender.com/health

# LangGraph Workflow Health
curl https://bhiv-hr-langgraph.onrender.com/health
```

## 🧪 Testing Environment

### Production Testing
**Purpose**: Live production environment
**Data**: Real-time processing
**Access**: Public access via URLs above

### Performance Metrics
- **Cold Start**: 30-60 seconds (free tier)
- **Response Time**: <100ms average
- **Uptime**: 99.9% target
- **Rate Limiting**: 60 requests/minute

## 📈 Performance Monitoring

### Health Endpoints
```bash
# Gateway Health
curl https://bhiv-hr-gateway-ltg0.onrender.com/health

# AI Agent Health  
curl https://bhiv-hr-agent-nhgg.onrender.com/health

# System Metrics
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics

# Database Test
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/test-candidates
```

### Monitoring Features
- Built-in Render monitoring
- Health check endpoints
- Error tracking
- Performance metrics
- Prometheus metrics export
- Real-time system monitoring
- Business analytics dashboard

## 🔐 Security Demonstration

### Security Features
- **API Authentication**: Bearer token required
- **Rate Limiting**: 60 requests/minute per IP
- **Security Headers**: CSP, XSS protection, Frame Options
- **Input Validation**: XSS/SQL injection protection
- **2FA Support**: TOTP compatible
- **Password Policies**: Enterprise-grade validation

### Security Testing Endpoints
```bash
# Rate Limit Status
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/rate-limit-status

# Security Headers Test
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/security/security-headers-test

# 2FA Demo Setup
curl -H "Authorization: Bearer <YOUR_API_KEY>" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/2fa/demo-setup
```

## 🎯 Demo Scenarios

### Scenario 1: HR Recruiter Workflow
1. **Access**: Visit https://bhiv-hr-portal-u670.onrender.com/
2. **Dashboard**: Explore HR interface
3. **API**: Test endpoints via https://bhiv-hr-gateway-ltg0.onrender.com/docs
4. **AI**: Test matching via https://bhiv-hr-agent-nhgg.onrender.com/docs
5. **Workflows**: Test automation via https://bhiv-hr-langgraph.onrender.com/docs

### Scenario 2: Client Company Workflow  
1. **Login**: Visit https://bhiv-hr-client-portal-3iod.onrender.com/
2. **Credentials**: Use TECH001 / demo123
3. **Interface**: Explore client dashboard
4. **Features**: Test job posting and candidate review

### Scenario 3: API Integration
1. **Documentation**: Visit https://bhiv-hr-gateway-ltg0.onrender.com/docs
2. **Authentication**: Use Bearer token: <YOUR_API_KEY>
3. **Testing**: Try different endpoints
4. **Monitoring**: Check health and metrics endpoints

## 🌍 Global Accessibility

### Render Platform Features
- **Global CDN**: Worldwide content delivery
- **HTTPS**: SSL certificates included
- **Auto-scaling**: Automatic resource management
- **Monitoring**: Built-in health checks
- **Logs**: Centralized logging system

### Access Information
- **Region**: Oregon (US West)
- **Latency**: Optimized for global access
- **Availability**: 99.9% uptime target
- **Support**: Render platform reliability

## 📞 Demo Support

### Platform Information
**Repository**: https://github.com/shashankmishraa/BHIV-HR-Platform
**Documentation**: Available in repository
**Deployment Guide**: RENDER_DEPLOYMENT_GUIDE.md

### Technical Details
**Platform**: Render Cloud
**Services**: 6 (Database + 6 Web Services)
**Cost**: $0/month (Free tier)
**Auto-Deploy**: GitHub integration

---

## 🚀 Quick Demo Access

**For immediate access to live demos:**

1. **API Documentation**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
2. **HR Portal**: https://bhiv-hr-portal-u670.onrender.com/
3. **Client Portal**: https://bhiv-hr-client-portal-3iod.onrender.com/ (TECH001/demo123)
4. **Candidate Portal**: https://bhiv-hr-candidate-portal-abe6.onrender.com/
5. **AI Matching**: https://bhiv-hr-agent-nhgg.onrender.com/docs
6. **Workflow Automation**: https://bhiv-hr-langgraph.onrender.com/docs

**Demo Features**:
- ✅ **107 API Endpoints**: Complete REST API with monitoring (94 Gateway + 6 Agent + 7 LangGraph)
- ✅ **AI Matching**: Real-time candidate matching with bias mitigation
- ✅ **Workflow Automation**: LangGraph AI orchestration with multi-channel notifications
- ✅ **Security**: Rate limiting, 2FA, input validation
- ✅ **Advanced Monitoring**: Prometheus metrics, health checks, performance analytics
- ✅ **Documentation**: Interactive Swagger UI, daily reflections, bias analysis

**Platform Status**: 🟪 ALL 6 SERVICES OPERATIONAL

---

*Live platform deployed on Render with zero monthly cost*

**Last Updated**: November 15, 2025  
**Platform Version**: 4.2.0-langgraph-production  
**Deployment**: ✅ Production Ready  
**Cost**: $0/month
