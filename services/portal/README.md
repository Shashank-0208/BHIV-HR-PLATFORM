# HR Portal Service

**Streamlit 1.41.1 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-portal-u670.onrender.com  
**Status**: ✅ Operational with RL Integration  
**Database**: PostgreSQL 17 Schema v4.3.1 (19 tables + RL integration)  
**Data**: 35 candidates, 29 jobs, 5 RL predictions, 17 RL feedback records  

## Overview

Internal HR dashboard for candidate management, job posting, and AI-powered matching.

## Key Features

- **Dashboard**: Real-time metrics and analytics with RL insights
- **Candidate Search**: Advanced filtering with AI + RL matching
- **Job Management**: Create and manage job postings
- **Values Assessment**: 5-point BHIV values evaluation with RL feedback
- **Batch Upload**: Secure candidate data import
- **RL Analytics**: Model performance tracking (80% accuracy, 340% feedback rate)
- **Database Integration**: Full access to 19 tables including RL system

## Architecture

```
portal/
├── app.py              # Streamlit interface (1500+ lines)
├── batch_upload.py     # Batch processing
├── config.py           # Configuration
├── file_security.py    # File security
├── components/         # UI components
└── requirements.txt    # Streamlit 1.41.1 dependencies
```

## Features

- **Real-time Data**: Live updates from Gateway API (119 endpoints)
- **Security**: File validation and path traversal protection
- **2FA Integration**: QR code generation with function-level imports
- **Performance**: Optimized Streamlit components
- **RL Integration**: Access to ML predictions and feedback system
- **Advanced Analytics**: RL model performance and training metrics

## Local Development

```bash
cd services/portal
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```
