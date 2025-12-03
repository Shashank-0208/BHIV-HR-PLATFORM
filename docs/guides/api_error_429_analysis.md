# API Error 429 Analysis - BHIV HR Platform

## Issue Identified
**Error**: `Registration failed: API Error: 429`
**Cause**: Rate limiting on Gateway service

## What HTTP 429 Means
- **429 Too Many Requests**: Server is rate limiting the client
- **Common Causes**:
  - Too many requests in short time period
  - Rate limiting configuration too strict
  - Multiple users hitting same endpoint

## Immediate Solutions

### 1. Check Gateway Rate Limiting
- Gateway service has rate limiting configured
- May be set too low for registration attempts
- Check Gateway logs for rate limit details

### 2. Retry with Delay
- Wait 30-60 seconds before trying again
- Rate limits usually reset after time window

### 3. Use Different Credentials
- Try registering with different email/phone
- Current combination may be temporarily blocked

## Technical Investigation Needed

### Check Gateway Service Configuration
```python
# Look for rate limiting in Gateway service
# Common locations:
# - middleware configuration
# - FastAPI rate limiting
# - nginx/proxy rate limits
```

### Check Gateway Logs
```bash
# Check Gateway service logs on Render
# Look for rate limiting messages
# Check current request counts
```

## Quick Test
1. Wait 2-3 minutes
2. Try registration again with same credentials
3. If still fails, try different email
4. Check Gateway API documentation for rate limits

## Root Cause
Gateway service rate limiting is preventing candidate registration - this is a backend configuration issue, not a portal issue.