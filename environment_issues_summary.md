# Environment Variable Issues - BHIV HR Platform

## Found Issues

### 1. Missing Environment Variables in Docker Compose

**Portal Service Missing:**
- `LANGGRAPH_SERVICE_URL` (needed for LangGraph integration)

**Candidate Portal Status:**
- ✅ CORRECTLY CONFIGURED - Only needs `GATEWAY_SERVICE_URL`
- ❌ AGENT_SERVICE_URL NOT NEEDED - All API calls go through Gateway
- ❌ LANGGRAPH_SERVICE_URL NOT NEEDED - No direct LangGraph calls

### 2. Current Docker Compose Configuration

```yaml
# ✅ CORRECT - Portal service
portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Set
    AGENT_SERVICE_URL: http://agent:9000      # ✅ Set
    # ❌ MISSING: LANGGRAPH_SERVICE_URL

# ✅ CORRECT - Client Portal service  
client_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Set
    AGENT_SERVICE_URL: http://agent:9000      # ✅ Set
    # ❌ MISSING: LANGGRAPH_SERVICE_URL

# ✅ CORRECT - Candidate Portal service
candidate_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000  # ✅ Set and sufficient
    # ✅ AGENT_SERVICE_URL not needed - uses Gateway API
    # ✅ LANGGRAPH_SERVICE_URL not needed - no direct calls
```

### 3. What Portal Apps Expect

**Portal Config (services/portal/config.py):**
```python
GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_URL")  # ✅ Available
AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL")      # ✅ Available
# Missing: LANGGRAPH_SERVICE_URL
```

**Client Portal Config (services/client_portal/config.py):**
```python
GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_URL")  # ✅ Available
AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL")      # ✅ Available
# Missing: LANGGRAPH_SERVICE_URL
```

**Candidate Portal Config (services/candidate_portal/config.py):**
```python
GATEWAY_SERVICE_URL = os.getenv("GATEWAY_SERVICE_URL")  # ✅ Available and sufficient
# Code analysis shows: Only uses Gateway API via make_api_request()
# AGENT_SERVICE_URL not referenced in code
# LANGGRAPH_SERVICE_URL not referenced in code
```

## Quick Fix

Add missing environment variables to Docker Compose:

```yaml
portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000
    AGENT_SERVICE_URL: http://agent:9000
    LANGGRAPH_SERVICE_URL: http://langgraph:9001  # ADD THIS

client_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000
    AGENT_SERVICE_URL: http://agent:9000
    LANGGRAPH_SERVICE_URL: http://langgraph:9001  # ADD THIS

candidate_portal:
  environment:
    GATEWAY_SERVICE_URL: http://gateway:8000      # ✅ SUFFICIENT
    # AGENT_SERVICE_URL not needed - verified by code analysis
    # LANGGRAPH_SERVICE_URL not needed - verified by code analysis
```

## Test Script Issues

The test script uses production URLs correctly, but API endpoints return 404 because:

1. **Gateway service** may not have the expected endpoints
2. **Agent service** may not have matching endpoints  
3. **LangGraph service** may not have workflow endpoints

## What You Can Check

1. **Portal URLs** - All accessible:
   - HR Portal: https://bhiv-hr-portal-u670.onrender.com ✅
   - Client Portal: https://bhiv-hr-client-portal-3iod.onrender.com ✅
   - Candidate Portal: https://bhiv-hr-candidate-portal-abe6.onrender.com ✅

2. **API Documentation** - Check available endpoints:
   - Gateway: https://bhiv-hr-gateway-ltg0.onrender.com/docs
   - Agent: https://bhiv-hr-agent-nhgg.onrender.com/docs
   - LangGraph: https://bhiv-hr-langgraph.onrender.com/docs

3. **Manual Workflow** - Test through browser interfaces using credentials:
   - Email: shashankmishra0411@gmail.com
   - Phone: 9284967526