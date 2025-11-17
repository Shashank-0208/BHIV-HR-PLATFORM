# 🔧 BHIV HR Platform - Troubleshooting Guide

**Generated**: November 15, 2025  
**Platform**: Production Environment (Render Cloud)  
**Status**: ✅ **COMPREHENSIVE TROUBLESHOOTING** - Complete diagnostic and resolution guide

---

## 🚨 Quick Issue Resolution

### **Service Status Check**
```bash
# Check all services quickly
curl https://bhiv-hr-gateway-ltg0.onrender.com/health
curl https://bhiv-hr-agent-nhgg.onrender.com/health
curl https://bhiv-hr-langgraph.onrender.com/health

# Expected Response:
{"status":"healthy","service":"BHIV HR Gateway","version":"4.2.0"}
```

### **Common Issues & Quick Fixes**
```
❌ Service Unavailable → Check service URLs and health endpoints
❌ Authentication Failed → Verify API keys and JWT tokens
❌ Database Connection → Check database connectivity
❌ Slow Response → Check rate limiting and system resources
❌ Portal Not Loading → Clear browser cache and check HTTPS
```

---

## 🌐 Gateway Service Issues

### **Gateway Not Responding**
**Symptoms**: 
- Gateway URL returns 503/504 errors
- Health endpoint not accessible
- API documentation not loading

**Diagnosis**:
```bash
# Check service status
curl -I https://bhiv-hr-gateway-ltg0.onrender.com/health

# Check specific endpoints
curl https://bhiv-hr-gateway-ltg0.onrender.com/docs
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics
```

**Solutions**:
1. **Service Restart**: Render auto-restarts failed services
2. **Check Logs**: Review Render dashboard logs
3. **Resource Limits**: Verify memory/CPU usage
4. **Database Connection**: Ensure database connectivity

### **Authentication Failures**
**Symptoms**:
- 401 Unauthorized responses
- Invalid API key errors
- JWT token validation failures

**Diagnosis**:
```bash
# Test API key authentication
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates

# Test JWT authentication
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/dashboard
```

**Solutions**:
1. **API Key Issues**:
   - Verify API key format (32 characters)
   - Check key exists in database
   - Ensure proper Authorization header format

2. **JWT Token Issues**:
   - Check token expiration
   - Verify token signature
   - Ensure proper claims structure

### **Rate Limiting Issues**
**Symptoms**:
- 429 Too Many Requests errors
- Requests being throttled
- Slow API responses

**Diagnosis**:
```bash
# Check current rate limit
curl https://bhiv-hr-gateway-ltg0.onrender.com/v1/rate-limit/status

# Monitor system resources
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics
```

**Solutions**:
1. **Reduce Request Frequency**: Space out API calls
2. **Check System Resources**: High CPU/memory triggers lower limits
3. **Use Batch Endpoints**: Process multiple items in single request
4. **Implement Retry Logic**: Exponential backoff for rate-limited requests

---

## 🤖 Agent Service Issues

### **AI Matching Not Working**
**Symptoms**:
- AI matching returns empty results
- Long processing times (>2 minutes)
- Phase 3 engine errors

**Diagnosis**:
```bash
# Test AI service health
curl https://bhiv-hr-agent-nhgg.onrender.com/health

# Test basic matching
curl -X POST https://bhiv-hr-agent-nhgg.onrender.com/match \
     -H "Content-Type: application/json" \
     -d '{"job_id": 1}'

# Check database connectivity
curl https://bhiv-hr-agent-nhgg.onrender.com/test-db
```

**Solutions**:
1. **Phase 3 Engine Issues**:
   - Service automatically falls back to database matching
   - Check memory usage (ML models require more memory)
   - Restart service if memory issues persist

2. **Database Connection Issues**:
   - Verify database credentials
   - Check connection pool status
   - Ensure database is accessible

3. **Performance Issues**:
   - Use batch matching for multiple candidates
   - Check system resources during processing
   - Consider processing during off-peak hours

### **Slow AI Processing**
**Symptoms**:
- Matching takes >60 seconds
- Timeout errors
- High memory usage

**Solutions**:
1. **Optimize Batch Size**: Use 50 candidates per batch
2. **Memory Management**: Restart service if memory usage >80%
3. **Database Optimization**: Ensure proper indexing
4. **Fallback Mode**: Use database matching for faster results

---

## 🔄 LangGraph Service Issues

### **Workflow Not Triggering**
**Symptoms**:
- Workflows not starting
- No notifications sent
- Workflow status stuck

**Diagnosis**:
```bash
# Check LangGraph service
curl https://bhiv-hr-langgraph.onrender.com/health

# Test workflow trigger via Gateway
curl -X POST http://localhost:8000/api/v1/workflow/trigger \
     -H "Content-Type: application/json" \
     -d '{
       "candidate_id": 1,
       "job_id": 1,
       "candidate_name": "Test User",
       "candidate_email": "test@example.com",
       "job_title": "Software Engineer"
     }'
```

**Solutions**:
1. **Service Connection**: Ensure LangGraph service is running
2. **Gateway Integration**: Verify Gateway can reach LangGraph service
3. **Workflow Configuration**: Check workflow definitions
4. **Notification Setup**: Verify notification channels configured

### **Notification Failures**
**Symptoms**:
- Emails not being sent
- WhatsApp/SMS not working
- Notification status shows failed

**Solutions**:
1. **Email Configuration**: Verify SMTP settings
2. **API Keys**: Check notification service API keys
3. **Template Issues**: Verify notification templates
4. **Rate Limits**: Check notification service rate limits

---

## 🖥️ Portal Issues

### **HR Portal Not Loading**
**Symptoms**:
- Portal shows loading screen indefinitely
- Streamlit errors
- Connection timeouts

**Diagnosis**:
```bash
# Check portal status
curl -I https://bhiv-hr-portal-u670.onrender.com/

# Check if service is running
curl https://bhiv-hr-portal-u670.onrender.com/_stcore/health
```

**Solutions**:
1. **Browser Issues**:
   - Clear browser cache and cookies
   - Try incognito/private browsing mode
   - Disable browser extensions

2. **Service Issues**:
   - Check Render service status
   - Verify service logs for errors
   - Restart service if needed

3. **API Connection**:
   - Verify Gateway service is accessible
   - Check API endpoints from portal
   - Ensure proper authentication

### **Client Portal Login Issues**
**Symptoms**:
- Login fails with valid credentials
- JWT token errors
- Session expires immediately

**Diagnosis**:
```bash
# Test client authentication
curl -X POST https://bhiv-hr-gateway-ltg0.onrender.com/v1/client/login \
     -H "Content-Type: application/json" \
     -d '{"username": "TECH001", "password": "demo123"}'
```

**Solutions**:
1. **Credential Issues**:
   - Verify username/password in database
   - Check password hashing
   - Ensure client account is active

2. **JWT Issues**:
   - Check JWT secret configuration
   - Verify token expiration settings
   - Ensure proper token validation

### **Candidate Portal Registration**
**Symptoms**:
- Registration fails
- Email validation errors
- Profile creation issues

**Solutions**:
1. **Validation Errors**: Check input format requirements
2. **Database Issues**: Verify candidate table constraints
3. **Email Conflicts**: Check for existing email addresses
4. **API Connection**: Ensure Gateway endpoints accessible

---

## 🗄️ Database Issues

### **Connection Failures**
**Symptoms**:
- Database connection timeouts
- Connection pool exhausted
- Query execution failures

**Diagnosis**:
```bash
# Test database connectivity via Gateway
curl https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/health

# Check connection pool status
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics
```

**Solutions**:
1. **Connection Pool**: 
   - Check pool size configuration (10 + 5 overflow)
   - Monitor active connections
   - Restart services if pool exhausted

2. **Database Performance**:
   - Check query execution times
   - Verify proper indexing
   - Monitor database resource usage

3. **Network Issues**:
   - Verify database URL accessibility
   - Check SSL connection requirements
   - Ensure proper credentials

### **Schema Issues**
**Symptoms**:
- Table not found errors
- Column constraint violations
- Migration failures

**Solutions**:
1. **Schema Version**: Verify current schema is v4.2.0
2. **Table Structure**: Check all 13 core tables exist
3. **Constraints**: Verify foreign key relationships
4. **Indexes**: Ensure proper indexing for performance

---

## 🔒 Security Issues

### **Authentication Problems**
**Symptoms**:
- API key validation failures
- JWT token errors
- 2FA setup issues

**Solutions**:
1. **API Key Issues**:
   ```bash
   # Generate new API key
   curl -X POST https://bhiv-hr-gateway-ltg0.onrender.com/v1/auth/generate-key \
        -H "Content-Type: application/json" \
        -d '{"description": "New API Key"}'
   ```

2. **JWT Problems**:
   - Check token expiration
   - Verify secret key configuration
   - Ensure proper claims structure

3. **2FA Issues**:
   - Regenerate TOTP secret
   - Verify QR code generation
   - Check time synchronization

### **Rate Limiting Problems**
**Symptoms**:
- Unexpected rate limit errors
- Inconsistent rate limiting
- Rate limit not adjusting

**Solutions**:
1. **System Resources**: Check CPU/memory usage
2. **Rate Limit Logic**: Verify dynamic adjustment working
3. **Per-Key Limits**: Check individual client limits
4. **Reset Limits**: Clear rate limit counters if needed

---

## 📊 Performance Issues

### **Slow Response Times**
**Symptoms**:
- API responses >5 seconds
- Portal loading slowly
- Database queries timing out

**Diagnosis**:
```bash
# Check system metrics
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics

# Test specific endpoint performance
time curl https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates
```

**Solutions**:
1. **Database Optimization**:
   - Check query execution plans
   - Verify proper indexing
   - Optimize complex queries

2. **Memory Management**:
   - Monitor memory usage
   - Restart services if memory leaks
   - Optimize data structures

3. **Connection Pooling**:
   - Verify pool configuration
   - Monitor connection usage
   - Adjust pool size if needed

### **High Memory Usage**
**Symptoms**:
- Services running out of memory
- Frequent service restarts
- Slow performance

**Solutions**:
1. **AI Service**: ML models require more memory - consider batch processing
2. **Connection Pools**: Reduce pool size if memory constrained
3. **Data Processing**: Process large datasets in chunks
4. **Service Restart**: Regular restarts can help with memory leaks

---

## 🔧 Development Issues

### **Local Development Setup**
**Symptoms**:
- Docker containers not starting
- Environment variables not loading
- Service communication failures

**Solutions**:
1. **Environment Setup**:
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Update database URL for local development
   DATABASE_URL=postgresql://user:password@localhost:5432/bhiv_hr
   ```

2. **Docker Issues**:
   ```bash
   # Rebuild containers
   docker-compose -f deployment/docker/docker-compose.production.yml down
   docker-compose -f deployment/docker/docker-compose.production.yml up --build -d
   ```

3. **Service Communication**:
   - Verify service URLs in environment
   - Check Docker network configuration
   - Ensure proper port mapping

### **Testing Issues**
**Symptoms**:
- Tests failing unexpectedly
- Database connection errors in tests
- Authentication failures in tests

**Solutions**:
1. **Test Database**: Use separate test database
2. **Test Data**: Ensure proper test data setup
3. **Authentication**: Use test API keys and tokens
4. **Service Dependencies**: Mock external services for testing

---

## 📋 Monitoring & Diagnostics

### **Health Check Endpoints**
```bash
# Service Health Checks
curl https://bhiv-hr-gateway-ltg0.onrender.com/health
curl https://bhiv-hr-agent-nhgg.onrender.com/health
curl https://bhiv-hr-langgraph.onrender.com/health

# Detailed Health Information
curl https://bhiv-hr-gateway-ltg0.onrender.com/health/detailed
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics
```

### **Log Analysis**
**Common Log Patterns**:
```
# Authentication Success
INFO: Authentication successful for API key: api_key_***

# Rate Limit Hit
WARNING: Rate limit exceeded for key: api_key_***

# Database Connection
INFO: Database connection established successfully

# AI Processing
INFO: Phase 3 matching completed in 0.02 seconds

# Error Patterns
ERROR: Database connection failed: connection timeout
ERROR: JWT token validation failed: token expired
ERROR: AI matching failed: insufficient memory
```

### **Performance Monitoring**
```bash
# System Metrics
curl https://bhiv-hr-gateway-ltg0.onrender.com/metrics

# Response Time Testing
time curl https://bhiv-hr-gateway-ltg0.onrender.com/v1/candidates

# Database Performance
curl https://bhiv-hr-gateway-ltg0.onrender.com/v1/database/stats
```

---

## 🚨 Emergency Procedures

### **Service Outage Response**
1. **Immediate Assessment**:
   - Check all service health endpoints
   - Review Render dashboard for alerts
   - Identify affected services

2. **Communication**:
   - Update status page if available
   - Notify stakeholders of issues
   - Provide estimated resolution time

3. **Resolution Steps**:
   - Restart affected services
   - Check resource limits
   - Review recent deployments
   - Implement temporary workarounds

### **Data Recovery**
1. **Database Issues**:
   - Check Render automated backups
   - Verify data integrity
   - Restore from backup if needed

2. **File Recovery**:
   - Check asset file availability
   - Restore from version control
   - Verify file permissions

---

## 📞 Support Resources

### **Documentation Links**
- [Quick Start Guide](QUICK_START_GUIDE.md)
- [API Documentation](docs/api/API_DOCUMENTATION.md)
- [Security Guide](docs/security/SECURITY_AUDIT.md)
- [Deployment Guide](docs/deployment/RENDER_DEPLOYMENT_GUIDE.md)

### **Service URLs**
- **Gateway API**: https://bhiv-hr-gateway-ltg0.onrender.com/docs
- **Agent API**: https://bhiv-hr-agent-nhgg.onrender.com/docs
- **HR Portal**: https://bhiv-hr-portal-u670.onrender.com/
- **Client Portal**: https://bhiv-hr-client-portal-3iod.onrender.com/
- **Candidate Portal**: https://bhiv-hr-candidate-portal-abe6.onrender.com/

### **Emergency Contacts**
- **Technical Support**: Check service logs and documentation
- **Platform Issues**: Render support dashboard
- **Security Issues**: Follow security incident procedures

---

**BHIV HR Platform Troubleshooting Guide** - Comprehensive diagnostic and resolution guide for all platform issues.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: November 15, 2025 | **Status**: ✅ Complete Guide | **Coverage**: All Services | **Issues**: 0 Active | **Resolution**: Step-by-step procedures