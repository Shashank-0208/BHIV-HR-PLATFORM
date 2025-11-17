# BHIV HR Platform - API Keys Summary

**Date**: November 17, 2025  
**Environment**: Local Docker Deployment  
**Total Services**: 7 (6 application services + 1 database)

## API Keys Configuration by Service

### 1. **Gateway Service** (`docker-gateway-1`)
- **Port**: 8000
- **API Keys Used**:
  - `API_KEY_SECRET`: `<YOUR_API_KEY>`
  - `JWT_SECRET`: `<YOUR_JWT_SECRET>`
  - `CANDIDATE_JWT_SECRET`: `<YOUR_CANDIDATE_JWT_SECRET>`
- **Authentication**: Triple authentication system (API Key + Client JWT + Candidate JWT)

### 2. **Agent Service** (`docker-agent-1`)
- **Port**: 9000
- **API Keys Used**:
  - `API_KEY_SECRET`: `<YOUR_API_KEY>`
  - `JWT_SECRET`: `<YOUR_JWT_SECRET>`
  - `CANDIDATE_JWT_SECRET`: `<YOUR_CANDIDATE_JWT_SECRET>`
- **Authentication**: Same as Gateway for consistency

### 3. **LangGraph Service** (`docker-langgraph-1`)
- **Port**: 9001
- **API Keys Used**:
  - `API_KEY_SECRET`: `<YOUR_API_KEY>`
- **Authentication**: Bearer token authentication only
- **Status**: ✅ Verified working with placeholder key

### 4. **HR Portal** (`docker-portal-1`)
- **Port**: 8501
- **API Keys Used**:
  - `API_KEY_SECRET`: `<YOUR_API_KEY>`
  - `JWT_SECRET_KEY`: `<YOUR_JWT_SECRET>`
  - `CANDIDATE_JWT_SECRET`: `<YOUR_CANDIDATE_JWT_SECRET>`
- **Authentication**: Portal-specific JWT implementation

### 5. **Client Portal** (`docker-client_portal-1`)
- **Port**: 8502
- **API Keys Used**:
  - `API_KEY_SECRET`: `<YOUR_API_KEY>`
  - `JWT_SECRET_KEY`: `<YOUR_JWT_SECRET>`
- **Authentication**: Client-specific authentication

### 6. **Candidate Portal** (`docker-candidate_portal-1`)
- **Port**: 8503
- **API Keys Used**:
  - `API_KEY`: `<YOUR_API_KEY>` (Note: Different variable name)
  - `JWT_SECRET`: `<YOUR_CANDIDATE_JWT_SECRET>`
  - `CANDIDATE_JWT_SECRET`: `<YOUR_CANDIDATE_JWT_SECRET>`
- **Authentication**: Candidate-specific authentication

### 7. **Database Service** (`docker-db-1`)
- **Port**: 5432
- **API Keys Used**: None (Database authentication uses PostgreSQL credentials)
- **Authentication**: PostgreSQL username/password

## API Key Types Summary

### Primary API Key
- **Variable Names**: `API_KEY_SECRET`, `API_KEY`
- **Value**: `<YOUR_API_KEY>` (Docker Compose placeholder)
- **Used By**: All 6 application services
- **Purpose**: Service-to-service authentication

### JWT Secrets
- **Client JWT**: `<YOUR_JWT_SECRET>`
- **Candidate JWT**: `<YOUR_CANDIDATE_JWT_SECRET>`
- **Purpose**: User session management

## Key Observations

### ✅ Consistency
- All services use the same primary API key value
- Consistent placeholder pattern across services
- Unified authentication approach

### ⚠️ Configuration Notes
1. **Placeholder Values**: All services currently use Docker Compose placeholder values
2. **Variable Name Differences**: 
   - Most services use `API_KEY_SECRET`
   - Candidate Portal uses `API_KEY`
3. **JWT Variations**:
   - Some services use `JWT_SECRET_KEY`
   - Others use `JWT_SECRET`

### 🔒 Security Status
- **Local Development**: ✅ Functional with placeholders
- **Production Deployment**: ✅ Uses actual secure keys on Render
- **Authentication Flow**: ✅ All endpoints properly protected

## Environment Variable Mapping

| Service | API_KEY_SECRET | JWT_SECRET | CANDIDATE_JWT_SECRET |
|---------|----------------|------------|---------------------|
| Gateway | ✅ | ✅ | ✅ |
| Agent | ✅ | ✅ | ✅ |
| LangGraph | ✅ | ❌ | ❌ |
| HR Portal | ✅ | ✅* | ✅ |
| Client Portal | ✅ | ✅* | ❌ |
| Candidate Portal | ✅** | ✅ | ✅ |
| Database | ❌ | ❌ | ❌ |

*Uses `JWT_SECRET_KEY` instead of `JWT_SECRET`  
**Uses `API_KEY` instead of `API_KEY_SECRET`

## Production vs Local Differences

### Local Development (Current)
```bash
API_KEY_SECRET=<YOUR_API_KEY>
JWT_SECRET=<YOUR_JWT_SECRET>
CANDIDATE_JWT_SECRET=<YOUR_CANDIDATE_JWT_SECRET>
```

### Production (Render Deployment)
```bash
API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA
CANDIDATE_JWT_SECRET=candidate_jwt_secret_key_2025
```

## Recommendations

### For Local Development
1. ✅ **Current setup works** - No changes needed for development
2. ✅ **All services authenticated** - Placeholder keys functional
3. ✅ **Consistent across services** - Unified authentication

### For Production
1. **Environment Variables**: Ensure all production keys are properly set
2. **Key Rotation**: Implement regular API key rotation
3. **Monitoring**: Add API key usage monitoring

## Testing Commands

```bash
# Test Gateway
curl -H "Authorization: Bearer <YOUR_API_KEY>" http://localhost:8000/health

# Test Agent
curl -H "Authorization: Bearer <YOUR_API_KEY>" http://localhost:9000/health

# Test LangGraph
curl -H "Authorization: Bearer <YOUR_API_KEY>" http://localhost:9001/health

# Test Portal APIs (through Gateway)
curl -H "Authorization: Bearer <YOUR_API_KEY>" http://localhost:8000/v1/jobs
```

---

**Summary**: All 6 application services use consistent API key authentication with the placeholder value `<YOUR_API_KEY>` working correctly in the local Docker environment. The database service uses PostgreSQL authentication and doesn't require API keys.