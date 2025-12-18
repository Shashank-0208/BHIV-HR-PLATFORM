# Candidate Portal Service

**Streamlit 1.41.1 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-candidate-portal-abe6.onrender.com  
**Status**: ✅ Operational with RL Integration  
**Database**: PostgreSQL 17 Schema v4.3.1 (19 tables + RL integration)  
**Available Jobs**: 29 production job postings  

## Overview

Job seeker interface for registration, job search, and application management.

## Key Features

- **Registration**: Secure account creation with validation (35 registered candidates)
- **Profile Management**: Comprehensive candidate information with RL tracking
- **Job Search**: Browse and filter available positions (29 jobs available)
- **Application Tracking**: Submit applications and monitor status with RL insights
- **Dashboard**: Personal overview of applications and activity
- **AI Matching**: RL-enhanced job recommendations based on profile
- **Feedback System**: Contribute to ML model improvement (340% feedback rate)

## Architecture

```
candidate_portal/
├── app.py              # Job seeker interface
├── config.py           # Configuration
└── requirements.txt    # Streamlit dependencies
```

## Features

- **Real-time Updates**: Live job postings and application status
- **Resume Upload**: Multi-format file support
- **Secure Authentication**: Password hashing with bcrypt and JWT
- **Application Management**: Track application history with RL predictions
- **ML Insights**: Access to RL model predictions and match scores
- **Database Integration**: Full access to candidate and application data

## Local Development

```bash
cd services/candidate_portal
pip install -r requirements.txt
streamlit run app.py --server.port 8503
```
