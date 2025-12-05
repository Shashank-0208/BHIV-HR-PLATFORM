# 🚀 BHIV HR Platform

**Enterprise AI-Powered Recruiting Platform** with intelligent candidate matching, comprehensive assessment tools, and production-grade security.

## 🌐 Live Production System

**Status**: ✅ **6/6 SERVICES OPERATIONAL** | **Cost**: $0/month | **Uptime**: 99.9% | **Total Endpoints**: 89

| Service | URL | Status |
|---------|-----|--------|
| **API Gateway** | [bhiv-hr-gateway-ltg0.onrender.com/docs](https://bhiv-hr-gateway-ltg0.onrender.com/docs) | ✅ 74 endpoints |
| **AI Engine** | [bhiv-hr-agent-nhgg.onrender.com/docs](https://bhiv-hr-agent-nhgg.onrender.com/docs) | ✅ 6 endpoints |
| **LangGraph Automation** | [bhiv-hr-langgraph.onrender.com](https://bhiv-hr-langgraph.onrender.com) | ✅ 9 endpoints |
| **HR Portal** | [bhiv-hr-portal-u670.onrender.com](https://bhiv-hr-portal-u670.onrender.com/) | ✅ Live |
| **Client Portal** | [bhiv-hr-client-portal-3iod.onrender.com](https://bhiv-hr-client-portal-3iod.onrender.com/) | ✅ Live |
| **Candidate Portal** | [bhiv-hr-candidate-portal-abe6.onrender.com](https://bhiv-hr-candidate-portal-abe6.onrender.com/) | ✅ Live |

**Demo Access**: Username: `demo_user` | Password: `demo_password` | API Key: Available in Render dashboard

## 📚 Documentation

### **🚀 Quick Start**
- **[Get Started in 5 Minutes](docs/guides/QUICK_START_GUIDE.md)** - Setup and deployment guide
- **[Current Features](docs/guides/CURRENT_FEATURES.md)** - Complete feature list and capabilities
- **[User Guide](docs/guides/USER_GUIDE.md)** - Complete user manual

### **🏗️ Architecture**
- **[Project Structure](docs/architecture/PROJECT_STRUCTURE.md)** - Complete architecture and folder organization
- **[Services Architecture](docs/architecture/SERVICES_ARCHITECTURE_SUMMARY.md)** - Microservices documentation
- **[Deployment Status](docs/architecture/DEPLOYMENT_STATUS.md)** - Current deployment status and health metrics

### **🔧 Technical Guides**
- **[API Documentation](docs/api/API_DOCUMENTATION.md)** - Complete API reference
- **[Deployment Guide](docs/deployment/RENDER_DEPLOYMENT_GUIDE.md)** - Deployment instructions
- **[Security Audit](docs/security/SECURITY_AUDIT.md)** - Security analysis and reports
- **[Testing Strategy](docs/testing/TESTING_STRATEGY.md)** - Testing approaches and guides
- **[LangGraph Integration](docs/guides/LANGGRAPH_INTEGRATION_GUIDE.md)** - Workflow automation guide

### **📊 Reports**
- **[Production Readiness](docs/reports/PRODUCTION_READINESS_REPORT.md)** - Production verification report
- **[File Organization](docs/architecture/FILE_ORGANIZATION_SUMMARY.md)** - Project organization summary

## ⚡ Quick Start

### **🌐 Use Live Platform (Recommended)**
1. Visit [HR Portal](https://bhiv-hr-portal-u670.onrender.com/) or [Client Portal](https://bhiv-hr-client-portal-3iod.onrender.com/)
2. Login with demo credentials: `TECH001` / `demo123`
3. Test API at [Gateway Docs](https://bhiv-hr-gateway-ltg0.onrender.com/docs)

### **💻 Local Development**
```bash
git clone https://github.com/Shashank-0208/BHIV-HR-PLATFORM.git
cd BHIV-HR-Platform
cp .env.example .env
docker-compose -f docker-compose.production.yml up -d
```

**📖 Detailed Setup**: [Quick Start Guide](docs/guides/QUICK_START_GUIDE.md)

## 🏗️ System Architecture

**Microservices Architecture**: 6 services + PostgreSQL database  
**Technology Stack**: FastAPI 4.2.0, Streamlit 1.41.1, Python 3.12.7, PostgreSQL 17  
**Total Endpoints**: 89 (74 Gateway + 6 Agent + 9 LangGraph)  
**Database Schema**: v4.3.0 with 13 core tables + RL integration  
**Deployment**: Docker-based microservices on Render platform  
**Organization**: Professional structure with files in proper subfolders

**📖 Complete Architecture**: [Project Structure](docs/architecture/PROJECT_STRUCTURE.md)

## 🚀 Key Features

### **🤖 AI-Powered Matching**
- **Phase 3 Semantic Engine** with sentence transformers
- **Reinforcement Learning Integration** with feedback-based optimization
- **Adaptive Scoring** with company-specific optimization
- **Real-time Processing** (<0.02s response time)
- **Batch Processing** (50 candidates/chunk)
- **ML-Enhanced Predictions** with scikit-learn models

### **🔄 LangGraph Workflows**
- **AI Workflow Automation** for candidate processing
- **Multi-Channel Notifications** (Email, WhatsApp, Telegram) - ✅ Confirmed Working
- **Real-time Status Tracking** and monitoring
- **Automated Sequences** with `/tools/send-notification` endpoint
- **Direct API Integration** (Twilio, Gmail SMTP, Telegram Bot)

### **🔒 Enterprise Security**
- **Triple Authentication** (API Key + Client JWT + Candidate JWT)
- **Unified Auth Management** with dedicated auth_manager.py per service
- **2FA TOTP** with QR code generation
- **Dynamic Rate Limiting** (60-500 requests/minute)
- **Security Headers** (CSP, XSS protection, HSTS)

### **📊 Triple Portal System**
- **HR Portal** - Dashboard and candidate management
- **Client Portal** - Enterprise job posting interface
- **Candidate Portal** - Job seeker application system

**📖 Complete Features**: [Current Features](docs/guides/CURRENT_FEATURES.md)



## 🛠️ Development & Deployment

### **Project Structure**

**Microservices Architecture**: 6 services + database  
**Technology**: FastAPI, Streamlit, PostgreSQL  
**Deployment**: Docker containers with dynamic port allocation  
**Organization**: Professional structure with proper categorization

```
BHIV HR PLATFORM/
├── services/          # 6 microservices (each with Dockerfile for Render deployment)
│   ├── gateway/       # API Gateway (app/main.py, routes/, logs/)
│   ├── agent/         # AI Agent (app.py, semantic_engine/phase3_engine.py)
│   ├── langgraph/     # LangGraph (app/ with rl_integration/, communication.py)
│   ├── portal/        # HR Portal (app.py, auth_manager.py, components/)
│   ├── client_portal/ # Client Portal (app.py, auth_manager.py)
│   ├── candidate_portal/ # Candidate Portal (app.py, auth_manager.py)
│   └── db/            # Database (consolidated_schema.sql, database/migrations/)
├── docs/             # Complete documentation suite (organized in subfolders)
├── tests/            # Comprehensive test suite (organized by service)
├── tools/            # Data processing & security utilities (organized in subfolders)
├── config/           # Environment configurations (secure templates)
├── deployment/       # Docker & deployment configurations
├── validation/       # Validation scripts (organized in subfolders)
├── utils/            # General utilities
├── assets/           # Static assets (29 resume files)
├── data/             # Production data
├── logs/             # System logs
└── reports/          # Analysis and audit reports
```

**📖 Complete Structure**: [Project Structure](docs/architecture/PROJECT_STRUCTURE.md)






### **Database Schema**

**PostgreSQL 17** with Schema v4.3.0  
**Tables**: 13 core tables + 6 RL tables (8 application + 5 security/performance + 6 RL/ML)  
**Features**: 75+ indexes, audit triggers, generated columns, referential integrity, RL feedback system

**📖 Complete Schema**: [Database Documentation](docs/database/)

### **Configuration**

**Environment Files**: `.env.example` (template), `config/` (production settings)  
**Deployment**: Docker Compose, Render platform configuration  
**Documentation**: Complete deployment guides available

**📖 Deployment Guide**: [Render Deployment](docs/deployment/RENDER_DEPLOYMENT_GUIDE.md)

### **Local Development**

**Prerequisites**: Docker, Python 3.12.7, Git  
**Setup**: Copy `.env.example`, run Docker Compose  
**Services**: All 6 services available on localhost  
**Database**: PostgreSQL with full schema

**📖 Setup Guide**: [Quick Start Guide](docs/guides/QUICK_START_GUIDE.md)

## 🧪 Testing & Validation

**Test Coverage**: 89 endpoints tested (100% pass rate)  
**Test Categories**: API, Security, Integration, LangGraph, Gateway  
**Organization**: Tests organized by service and functionality  
**Automation**: Complete test suite with reports

**📖 Testing Guide**: [Testing Strategy](docs/testing/TESTING_STRATEGY.md)

## 📊 Performance & Monitoring

**Performance**: <100ms API response, <0.02s AI matching, 99.9% uptime  
**Monitoring**: Prometheus metrics, health checks, performance dashboards  
**Rate Limiting**: Dynamic 60-500 requests/minute based on CPU usage  
**Optimization**: Connection pooling, caching, memory optimization

**📖 Monitoring**: [Production Readiness Report](docs/reports/PRODUCTION_READINESS_REPORT.md)

## 🔧 Tools & Utilities

**Data Processing**: Resume extraction (29 files), job creation (19 jobs), database sync  
**Security Tools**: API key management, security audits, configuration validation  
**Deployment**: Local deployment scripts, Docker automation, health monitoring  
**Organization**: Tools categorized by purpose in dedicated directories

**📖 Tools Documentation**: [Project Structure](docs/architecture/PROJECT_STRUCTURE.md)



## 🎯 Production Status

**System Status**: ✅ **FULLY OPERATIONAL**  
**Services**: 6/6 live with 99.9% uptime  
**Endpoints**: 89 total (100% tested and functional)  
**Database**: PostgreSQL 17 with 13 core tables + 6 RL tables  
**Cost**: $0/month (optimized free tier deployment)

**Recent Updates**: Complete RL integration with ML-powered matching, unified authentication system with auth_manager.py files, enhanced LangGraph workflows, fixed automation endpoints (/tools/send-notification), secured credentials with placeholders, project files organized into proper subfolders

**📖 Detailed Status**: [Deployment Status](docs/architecture/DEPLOYMENT_STATUS.md)

## 🚀 Getting Started

### **🌐 For Users**
1. Visit [Live Platform](https://bhiv-hr-gateway-ltg0.onrender.com/docs)
2. Access [HR Portal](https://bhiv-hr-portal-u670.onrender.com/) or [Client Portal](https://bhiv-hr-client-portal-3iod.onrender.com/)
3. Use demo credentials or API key for testing

### **💻 For Developers**
1. Clone repository and setup environment
2. Run Docker Compose for local development
3. Execute test suite for validation

**📖 Complete Setup**: [Quick Start Guide](docs/guides/QUICK_START_GUIDE.md)

## 📞 Resources

**GitHub**: [BHIV-HR-Platform Repository](https://github.com/Shashank-0208/BHIV-HR-PLATFORM)  
**Platform**: Render Cloud (Oregon, US West)  
**Documentation**: Complete guides in `docs/` directory

### **Quick Links**
- [Live API Documentation](https://bhiv-hr-gateway-ltg0.onrender.com/docs)
- [HR Dashboard](https://bhiv-hr-portal-u670.onrender.com/)
- [Client Portal](https://bhiv-hr-client-portal-3iod.onrender.com/)
- [Candidate Portal](https://bhiv-hr-candidate-portal-abe6.onrender.com/)
- [AI Agent Service](https://bhiv-hr-agent-nhgg.onrender.com/docs)

---

**BHIV HR Platform v3.0.0** - Enterprise AI-powered recruiting platform with intelligent candidate matching, comprehensive assessment tools, and production-grade security.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Status**: ✅ Production Ready | **Services**: 6/6 Live | **Endpoints**: 89 Total | **Uptime**: 99.9% | **Cost**: $0/month | **Updated**: November 21, 2025 (Post-Rectification)
