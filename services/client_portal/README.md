# Client Portal Service

**Streamlit 1.41.1 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-client-portal-3iod.onrender.com  
**Status**: ✅ Operational with RL Integration  
**Database**: PostgreSQL 17 Schema v4.3.1 (19 tables + RL integration)  
**API Access**: 119 endpoints via Gateway service  

## Overview

External client interface for enterprise job posting and candidate review.

## Key Features

- **Enterprise Authentication**: JWT-based secure login
- **Job Posting**: Create and manage job listings (29 production jobs)
- **Candidate Review**: Access AI + RL matched candidates (35 candidates)
- **Interview Coordination**: Schedule and manage interviews
- **Real-time Sync**: Instant updates with HR portal
- **RL Analytics**: Access to ML model insights (80% accuracy)
- **Advanced Matching**: RL-enhanced candidate recommendations

## Architecture

```
client_portal/
├── app.py              # Client interface (800+ lines) with RL integration
├── auth_manager.py     # Enterprise authentication with unified auth
├── config.py           # Configuration
└── requirements.txt    # Streamlit dependencies
```

## Authentication

- **Demo Credentials**: TECH001 / demo123
- **JWT Tokens**: Secure session management
- **Account Protection**: Lockout and session timeout

## Local Development

```bash
cd services/client_portal
pip install -r requirements.txt
streamlit run app.py --server.port 8502
```
