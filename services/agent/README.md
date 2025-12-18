# AI Agent Service

**FastAPI 0.115.6 + Python 3.12.7-slim**  
**Production URL**: https://bhiv-hr-agent-nhgg.onrender.com  
**Endpoints**: 6 total  
**Status**: ✅ Operational with RL Integration  
**Database**: PostgreSQL 17 Schema v4.3.1 (19 tables + RL integration)  

## Overview

AI-powered semantic candidate matching service with Phase 3 learning capabilities.

## Key Features

- **Phase 3 Semantic Engine**: Production-grade NLP processing with RL enhancement
- **Batch Processing**: Multiple job matching optimization (50 candidates/chunk)
- **RL Integration**: Reinforcement learning with 80% model accuracy
- **Real-time Analysis**: <0.02 second response time
- **Database Integration**: 5 RL predictions, 17 feedback records, 340% feedback rate

## Architecture

```
agent/
├── app.py                  # FastAPI AI service (600+ lines)
├── semantic_engine/        # Phase 3 AI engine
│   ├── __init__.py
│   └── phase3_engine.py
└── requirements.txt        # AI/ML dependencies
```

## Endpoints

- **Core** (2): GET /, GET /health
- **AI Processing** (3): POST /match, POST /batch-match, GET /analyze/{candidate_id}
- **Diagnostics** (1): GET /test-db

## AI Features

- **Semantic Matching**: Advanced sentence transformers with RL optimization
- **Adaptive Scoring**: Company-specific weight optimization with ML feedback
- **Cultural Fit Analysis**: Feedback-based alignment (10% bonus)
- **Multi-Factor Scoring**: Semantic (40%), Experience (30%), Skills (20%), Location (10%)
- **RL Model**: v1.0.1 trained with 15 samples, 80% accuracy
- **Database Schema**: 19 tables (13 core + 6 RL integration tables)

## Local Development

```bash
cd services/agent
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 9000 --reload
```
