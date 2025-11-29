# Environment Variable Analysis - BHIV HR Platform (Updated)

## Issues Found

### 1. **Environment Variable Requirements Analysis**

**Candidate Portal (✅ CORRECT):**
- Only needs `GATEWAY_SERVICE_URL` - all API calls go through Gateway
- Does NOT need `AGENT_SERVICE_URL` or `LANGGRAPH_SERVICE_URL`
- Current Docker Compose configuration is sufficient

**HR Portal & Client Portal:**
- Need `GATEWAY_SERVICE_URL` ✅ (present)
- Need `AGENT_SERVICE_URL` ✅ (present) 
- May need `LANGGRAPH_SERVICE_URL` for direct LangGraph calls

### 2. **Current Docker Compose Status**

**✅ Candidate Portal - CORRECT:**
```yaml
candidate_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Only needed variable
```

**⚠️ HR Portal & Client Portal - May need LangGraph URL:**
```yaml
portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Present
    AGENT_SERVICE_URL: http://agent:9000      # ✅ Present
    # May need: LANGGRAPH_SERVICE_URL

client_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Present
    AGENT_SERVICE_URL: http://agent:9000      # ✅ Present
    # May need: LANGGRAPH_SERVICE_URL
```

### 3. **Production URLs vs Local URLs**

**Test Script Uses Production URLs:**
```python
URLS = {
    'gateway': 'https://bhiv-hr-gateway-ltg0.onrender.com',
    'agent': 'https://bhiv-hr-agent-nhgg.onrender.com',
    'langgraph': 'https://bhiv-hr-langgraph.onrender.com',
    # ...
}
```

**But Portal Apps Expect Environment Variables:**
```python
# This will be None if not set in environment
GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_URL")
```

## Solutions

### 1. **Environment Variable Requirements (Updated)**

**Candidate Portal - No Changes Needed:**
```yaml
candidate_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Sufficient
    # AGENT_SERVICE_URL not needed - uses Gateway for all API calls
    # LANGGRAPH_SERVICE_URL not needed - no direct LangGraph calls
```

**HR Portal & Client Portal - Only if direct LangGraph calls exist:**
```yaml
portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Present
    AGENT_SERVICE_URL: http://agent:9000      # ✅ Present
    LANGGRAPH_SERVICE_URL: http://langgraph:9001  # Add only if needed

client_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Present
    AGENT_SERVICE_URL: http://agent:9000      # ✅ Present
    LANGGRAPH_SERVICE_URL: http://langgraph:9001  # Add only if needed
```

### 2. **Update Test Script for Production**

The test script should use the production URLs directly since the portals are deployed on Render:

```python
# For production testing, use actual Render URLs
PRODUCTION_URLS = {
    'gateway': 'https://bhiv-hr-gateway-ltg0.onrender.com',
    'agent': 'https://bhiv-hr-agent-nhgg.onrender.com', 
    'langgraph': 'https://bhiv-hr-langgraph.onrender.com',
    'hr_portal': 'https://bhiv-hr-portal-u670.onrender.com',
    'client_portal': 'https://bhiv-hr-client-portal-3iod.onrender.com',
    'candidate_portal': 'https://bhiv-hr-candidate-portal-abe6.onrender.com'
}
```

### 3. **Environment Variable Validation**

All portal config files properly validate required environment variables:

```python
# ✅ Good - All portals do this
GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_URL")
if not GATEWAY_SERVICE_URL:
    raise ValueError("GATEWAY_SERVICE_URL environment variable is required")
```

## Updated Assessment

**✅ Candidate Portal**: Environment variables are correctly configured - no changes needed

**⚠️ HR Portal & Client Portal**: May need `LANGGRAPH_SERVICE_URL` only if they make direct LangGraph calls

**✅ Production Testing**: All portals are accessible and functional

## Recommendations

1. **Candidate Portal**: No environment variable changes needed
2. **HR/Client Portals**: Add `LANGGRAPH_SERVICE_URL` only if direct LangGraph integration exists
3. **Production Testing**: Use browser-based testing with provided credentials
4. **API Endpoints**: 404 errors indicate missing Gateway routes, not environment issues

## Next Steps

1. Test workflow manually through browser interfaces
2. Check Gateway API documentation for correct endpoints
3. Add `LANGGRAPH_SERVICE_URL` to HR/Client portals only if needed
4. Focus on API endpoint verification rather than environment variables