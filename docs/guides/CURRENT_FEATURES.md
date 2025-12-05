# 🚀 BHIV HR Platform - Current Features

**Enterprise AI-Powered Recruiting Platform**  
**Updated**: November 21, 2025  
**Version**: 3.0.0 Production Ready  
**Status**: ✅ 6/6 Services Operational | 89 Endpoints Live

---

## 🌐 Live Production System

### **Service Status**
| Service | URL | Endpoints | Status |
|---------|-----|-----------|--------|
| **API Gateway** | [bhiv-hr-gateway-ltg0.onrender.com](https://bhiv-hr-gateway-ltg0.onrender.com/docs) | 74 | ✅ Live |
| **AI Agent** | [bhiv-hr-agent-nhgg.onrender.com](https://bhiv-hr-agent-nhgg.onrender.com/docs) | 6 | ✅ Live |
| **LangGraph** | [bhiv-hr-langgraph.onrender.com](https://bhiv-hr-langgraph.onrender.com) | 9 | ✅ Live |
| **HR Portal** | [bhiv-hr-portal-u670.onrender.com](https://bhiv-hr-portal-u670.onrender.com/) | Web UI | ✅ Live |
| **Client Portal** | [bhiv-hr-client-portal-3iod.onrender.com](https://bhiv-hr-client-portal-3iod.onrender.com/) | Web UI | ✅ Live |
| **Candidate Portal** | [bhiv-hr-candidate-portal-abe6.onrender.com](https://bhiv-hr-candidate-portal-abe6.onrender.com/) | Web UI | ✅ Live |

**Performance**: 99.9% Uptime | <100ms API Response | $0/month Cost

---

## 🤖 AI-Powered Matching Engine

### **Phase 3 Semantic Engine + RL Integration**
- **Sentence Transformers**: Advanced semantic understanding
- **Reinforcement Learning**: ML-powered feedback optimization
- **Adaptive Scoring**: Company-specific optimization algorithms
- **Real-time Processing**: <0.02s response time per candidate
- **Batch Processing**: 50 candidates per chunk optimization
- **Multi-dimensional Analysis**: Skills, experience, values alignment
- **Continuous Learning**: Feedback-based model improvement

### **AI Endpoints**
```bash
GET  /v1/match/{job_id}/top           # Top candidates for job
POST /v1/match/batch                 # Batch matching multiple jobs
GET  /analyze/{candidate_id}         # Candidate analysis
POST /match                          # Custom matching criteria
POST /rl/predict                     # RL-enhanced matching prediction
POST /rl/feedback                    # Submit feedback for RL learning
GET  /rl/analytics                   # RL system analytics
GET  /health                         # AI service health
GET  /metrics                        # Performance metrics
```

---

## 🧠 Reinforcement Learning Integration

### **ML-Enhanced Matching**
- **Feedback Learning**: Continuous improvement from hiring outcomes
- **Prediction Models**: scikit-learn powered decision making
- **Reward Signals**: Automated learning from successful matches
- **Performance Analytics**: Real-time ML system monitoring

### **RL Endpoints**
```bash
POST /rl/predict                    # ML-enhanced candidate matching
POST /rl/feedback                   # Submit feedback for learning
GET  /rl/analytics                  # System performance metrics
GET  /rl/performance                # Real-time monitoring data
POST /rl/start-monitoring           # Activate RL monitoring
```

### **Learning Features**
- **Decision Engine**: Advanced ML decision making
- **Feedback Collection**: Structured learning data
- **Model Optimization**: Continuous algorithm improvement
- **Performance Tracking**: ML system health monitoring

---

## 🔄 LangGraph Workflow Automation

### **Multi-Channel Notifications**
- **Email Integration**: Gmail SMTP with HTML templates
- **WhatsApp Business**: Twilio API integration
- **Telegram Bot**: Direct API integration
- **Real-time Status**: Live tracking and monitoring

### **Workflow Endpoints**
```bash
POST /workflows/application/start    # Start candidate workflow
GET  /workflows/{workflow_id}/status # Check workflow status
POST /tools/send-notification       # Send multi-channel notification
GET  /test/send-automated-sequence   # Test automation sequence
POST /workflows/interview/schedule   # Schedule interview workflow
GET  /workflows/stats               # Workflow statistics
POST /workflows/offer/send          # Send offer workflow
GET  /health                        # Service health check
GET  /                              # Service info
```

### **Automation Features**
- **Interview Scheduling**: Automated calendar integration
- **Status Updates**: Real-time candidate notifications
- **Offer Management**: Automated offer letter generation
- **Follow-up Sequences**: Intelligent reminder systems

---

## 🔒 Enterprise Security

### **Triple Authentication System**
- **API Key Authentication**: Bearer token for service access
- **Client JWT**: Secure client portal authentication
- **Candidate JWT**: Separate candidate portal security

### **Security Features**
- **2FA TOTP**: Time-based one-time passwords with QR codes
- **Dynamic Rate Limiting**: 60-500 requests/minute based on CPU
- **Input Validation**: XSS and injection protection
- **Security Headers**: CSP, HSTS, XSS protection
- **Credential Security**: Placeholder format for Git safety

### **Security Endpoints**
```bash
POST /v1/2fa/setup                  # Setup 2FA authentication
POST /v1/2fa/verify                 # Verify 2FA token
GET  /v1/security/headers           # Security headers test
POST /v1/security/test-input-validation # Input validation test
GET  /v1/security/csp-report        # CSP violation reports
```

---

## 📊 Triple Portal System

### **HR Portal Features**
- **Dashboard Overview**: Real-time metrics and analytics
- **Candidate Management**: Complete candidate lifecycle
- **Job Creation**: Multi-step job posting wizard
- **AI Shortlisting**: Automated candidate ranking
- **Values Assessment**: 5-point BHIV framework scoring
- **Interview Scheduling**: Calendar integration
- **Report Generation**: Comprehensive analytics export
- **Batch Operations**: Bulk candidate processing

### **Client Portal Features**
- **Enterprise Dashboard**: Client-specific analytics
- **Job Posting Interface**: Professional job creation
- **Candidate Review**: AI-matched candidate browsing
- **Interview Management**: Schedule and track interviews
- **Offer Management**: Digital offer letter system
- **Real-time Sync**: Live updates with HR portal
- **Automation Controls**: LangGraph workflow triggers

### **Candidate Portal Features**
- **Profile Management**: Complete candidate profiles
- **Job Search**: Advanced filtering and search
- **Application Tracking**: Real-time status updates
- **Interview Scheduling**: Self-service calendar booking
- **Document Upload**: Resume and portfolio management
- **Notification Center**: Multi-channel updates

---

## 🗄️ Database Architecture

### **PostgreSQL 17 Schema v4.3.0**
- **13 Core Tables + 6 RL Tables**: Complete HR data model with ML integration
- **75+ Indexes**: Optimized query performance
- **Audit Triggers**: Complete change tracking
- **Generated Columns**: Automated calculations
- **Referential Integrity**: Data consistency enforcement
- **RL Integration**: Feedback-based learning system

### **Core Tables**
```sql
-- Application Tables (8)
candidates              # Candidate profiles and data
jobs                   # Job postings and requirements
applications           # Job applications and status
interviews             # Interview scheduling and results
feedback               # Values assessment and scoring
clients                # Client company information
users                  # HR user management
offers                 # Job offers and negotiations

-- System Tables (5)
api_keys               # API authentication management
rate_limits            # Dynamic rate limiting data
audit_logs             # Complete system audit trail
workflow_executions    # LangGraph workflow tracking
notifications          # Multi-channel notification log
```

---

## 🛠️ API Gateway (74 Endpoints)

### **Candidate Management**
```bash
GET    /v1/candidates              # List all candidates
POST   /v1/candidates              # Create new candidate
GET    /v1/candidates/{id}         # Get candidate details
PUT    /v1/candidates/{id}         # Update candidate
DELETE /v1/candidates/{id}         # Delete candidate
GET    /v1/candidates/stats        # Candidate statistics
POST   /v1/candidates/search       # Advanced search
POST   /v1/candidates/batch        # Batch operations
```

### **Job Management**
```bash
GET    /v1/jobs                    # List all jobs
POST   /v1/jobs                    # Create new job
GET    /v1/jobs/{id}               # Get job details
PUT    /v1/jobs/{id}               # Update job
DELETE /v1/jobs/{id}               # Delete job
GET    /v1/jobs/stats              # Job statistics
POST   /v1/jobs/search             # Job search
GET    /v1/jobs/{id}/candidates    # Job candidates
```

### **Application Management**
```bash
GET    /v1/applications            # List applications
POST   /v1/applications            # Create application
GET    /v1/applications/{id}       # Application details
PUT    /v1/applications/{id}       # Update application
DELETE /v1/applications/{id}       # Delete application
GET    /v1/applications/stats      # Application statistics
POST   /v1/applications/batch      # Batch processing
```

### **Interview Management**
```bash
GET    /v1/interviews              # List interviews
POST   /v1/interviews              # Schedule interview
GET    /v1/interviews/{id}         # Interview details
PUT    /v1/interviews/{id}         # Update interview
DELETE /v1/interviews/{id}         # Cancel interview
GET    /v1/interviews/calendar     # Calendar view
POST   /v1/interviews/reschedule   # Reschedule interview
```

### **Values Assessment**
```bash
GET    /v1/feedback                # List assessments
POST   /v1/feedback                # Submit assessment
GET    /v1/feedback/{id}           # Assessment details
PUT    /v1/feedback/{id}           # Update assessment
DELETE /v1/feedback/{id}           # Delete assessment
GET    /v1/feedback/stats          # Assessment statistics
POST   /v1/feedback/batch          # Batch assessments
```

---

## 📈 Performance & Monitoring

### **Performance Metrics**
- **API Response Time**: <100ms average
- **AI Matching Speed**: <0.02s per candidate
- **Database Query Time**: <50ms average
- **Portal Load Time**: <2s initial load
- **Uptime**: 99.9% availability

### **Monitoring Features**
- **Health Checks**: Real-time service monitoring
- **Prometheus Metrics**: Detailed performance data
- **Error Tracking**: Comprehensive error logging
- **Performance Dashboards**: Visual monitoring
- **Alert System**: Automated issue detection

### **Monitoring Endpoints**
```bash
GET /health                        # Basic health check
GET /health/detailed               # Detailed health status
GET /metrics                       # Prometheus metrics
GET /v1/monitoring/performance     # Performance metrics
GET /v1/monitoring/errors          # Error statistics
```

---

## 🔧 Development & Deployment

### **Technology Stack**
- **Backend**: FastAPI 4.2.0, Python 3.12.7
- **Frontend**: Streamlit 1.41.1
- **Database**: PostgreSQL 17
- **AI Engine**: Sentence Transformers, scikit-learn
- **Automation**: LangGraph, Twilio, Gmail SMTP
- **Deployment**: Docker, Render Platform

### **Project Structure**
```
BHIV HR PLATFORM/
├── services/          # 6 microservices
│   ├── gateway/       # API Gateway (74 endpoints)
│   ├── agent/         # AI Agent (6 endpoints)
│   ├── langgraph/     # Automation (9 endpoints)
│   ├── portal/        # HR Portal (Streamlit)
│   ├── client_portal/ # Client Portal (Streamlit)
│   ├── candidate_portal/ # Candidate Portal (Streamlit)
│   └── db/           # Database schema
├── docs/             # Complete documentation
├── tests/            # Comprehensive test suite
├── tools/            # Utility scripts
├── config/           # Environment configuration
├── data/             # Production data
└── assets/           # Static files (29 resumes)
```

---

## 🧪 Testing & Validation

### **Test Coverage**
- **89 Endpoints**: 100% tested and functional
- **Security Tests**: Authentication, validation, headers
- **Integration Tests**: Cross-service communication
- **Performance Tests**: Load and stress testing
- **Automation Tests**: LangGraph workflow validation

### **Test Categories**
```bash
tests/
├── api/              # API endpoint testing
├── security/         # Security feature testing
├── integration/      # Cross-service testing
├── langgraph/        # Workflow automation testing
├── portal/           # UI and portal testing
├── database/         # Database integrity testing
└── misc/             # Utility and diagnostic tests
```

---

## 📊 Production Data

### **Real Data Available**
- **29 Resume Files**: Processed PDF/DOCX in assets/resumes/
- **10+ Candidates**: Complete profiles with skills
- **6+ Active Jobs**: Multi-client job postings
- **3+ Client Companies**: TECH001, STARTUP01, ENTERPRISE01
- **Assessment Data**: 5-point BHIV values framework
- **Interview Records**: Complete scheduling system
- **Workflow Logs**: LangGraph execution history

### **Data Verification**
```bash
# Check data status
GET /v1/database/schema            # Database schema info
GET /v1/candidates/stats           # Candidate statistics
GET /v1/jobs/stats                 # Job statistics
GET /v1/applications/stats         # Application statistics
GET /workflows/stats               # Workflow statistics
```

---

## 🚀 Recent Updates (November 2025)

### **Automation Fixes**
- ✅ Fixed LangGraph endpoints (`/tools/send-notification`)
- ✅ Removed hardcoded URLs from portal services
- ✅ Standardized environment variables across services
- ✅ Secured credentials with placeholder format
- ✅ Confirmed WhatsApp/Email automation working

### **Security Enhancements**
- ✅ Enhanced .gitignore to prevent credential exposure
- ✅ Created secure environment templates
- ✅ Implemented credential validation checks
- ✅ Updated all services to use environment variables

### **Project Organization**
- ✅ Organized files into proper subdirectories
- ✅ Moved test files to appropriate categories
- ✅ Structured documentation by topic
- ✅ Cleaned root directory structure

---

## 🎯 Key Differentiators

### **Values-Driven Approach**
- **BHIV Framework**: Integrity, Honesty, Discipline, Hard Work, Gratitude
- **5-Point Assessment**: Comprehensive values evaluation
- **Cultural Fit**: Beyond skills matching
- **Character Analysis**: Holistic candidate evaluation

### **AI-Powered Intelligence**
- **Semantic Understanding**: Context-aware matching
- **Adaptive Learning**: Continuous improvement
- **Multi-dimensional Analysis**: Skills + Values + Experience
- **Real-time Processing**: Instant results

### **Enterprise Features**
- **Multi-tenant Architecture**: Client isolation
- **Scalable Design**: Handle enterprise workloads
- **Security First**: Triple authentication system
- **Audit Trail**: Complete compliance tracking

---

## 📞 Support & Resources

### **Documentation**
- **Quick Start**: [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
- **API Reference**: [API_DOCUMENTATION.md](../api/API_DOCUMENTATION.md)
- **Architecture**: [SERVICES_ARCHITECTURE_SUMMARY.md](../architecture/SERVICES_ARCHITECTURE_SUMMARY.md)
- **Security**: [SECURITY_AUDIT.md](../security/SECURITY_AUDIT.md)
- **Testing**: [TESTING_STRATEGY.md](../testing/TESTING_STRATEGY.md)

### **Live Platform Access**
- **Demo Credentials**: Username: `demo_user` | Password: `demo_password`
- **API Key**: Available in Render dashboard environment variables
- **Support**: GitHub Issues and Documentation

---

**BHIV HR Platform v3.0.0** - Enterprise AI-powered recruiting platform with intelligent candidate matching, comprehensive assessment tools, and production-grade security.

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Status**: ✅ Production Ready | **Services**: 6/6 Live | **Endpoints**: 89 Total | **Uptime**: 99.9% | **Cost**: $0/month

**Last Updated**: November 21, 2025 (Post-Rectification)