# 🚀 BHIV HR Platform - BAT Scripts Guide

## **No Docker? No Problem!**

These BAT scripts let you run the entire BHIV HR Platform without Docker installation.

---

## **📁 Available Scripts**

### **1. setup_first_time.bat**
**Purpose**: First-time setup for new users
```bash
# What it does:
✅ Checks Python installation
✅ Creates .env file from template
✅ Creates virtual environment
✅ Guides you through setup process
```

### **2. start_all_services.bat**
**Purpose**: Start all 6 services at once
```bash
# What it does:
✅ Activates virtual environment
✅ Installs all dependencies
✅ Starts Gateway (Port 8000)
✅ Starts AI Agent (Port 9000)
✅ Starts LangGraph (Port 9001)
✅ Starts HR Portal (Port 8501)
✅ Starts Client Portal (Port 8502)
✅ Starts Candidate Portal (Port 8503)
```

### **3. stop_all_services.bat**
**Purpose**: Stop all running services
```bash
# What it does:
✅ Kills all service processes
✅ Frees up all ports
✅ Clean shutdown
```

### **4. check_services.bat**
**Purpose**: Check if services are running
```bash
# What it does:
✅ Tests each service health
✅ Shows running status
✅ Displays access URLs
```

---

## **🚀 Quick Start Guide**

### **Step 1: First Time Setup**
```bash
# Double-click this file:
setup_first_time.bat

# Follow the prompts to:
# - Check Python installation
# - Create .env file
# - Edit credentials
```

### **Step 2: Start All Services**
```bash
# Double-click this file:
start_all_services.bat

# Wait 60 seconds for all services to start
```

### **Step 3: Access the Platform**
```bash
# Open in browser:
HR Portal:        http://localhost:8501
Client Portal:    http://localhost:8502
Candidate Portal: http://localhost:8503

# Login with:
Username: TECH001
Password: demo123
```

### **Step 4: Stop Services (When Done)**
```bash
# Double-click this file:
stop_all_services.bat
```

---

## **📋 Prerequisites**

### **Required Software:**
- **Python 3.12.7** - Download from https://python.org
- **Windows 10/11** - BAT scripts are Windows-specific

### **Optional (for API testing):**
- **curl** - Usually pre-installed on Windows 10/11

---

## **🔧 Configuration**

### **Environment File (.env)**
The scripts will create `.env` from `.env.example`. You need to edit it with:

```bash
# Database (use local PostgreSQL or shared URL)
DATABASE_URL=postgresql://user:pass@localhost:5432/bhiv_hr

# API Keys (generate your own)
API_KEY_SECRET=your_secure_api_key_here
JWT_SECRET_KEY=your_jwt_secret_here
CANDIDATE_JWT_SECRET_KEY=your_candidate_jwt_here

# External Services (optional for basic functionality)
TWILIO_ACCOUNT_SID=your_twilio_sid
GMAIL_EMAIL=your_email@gmail.com
# ... other credentials
```

---

## **🌐 Service Details**

| Service | Port | Purpose | URL |
|---------|------|---------|-----|
| **Gateway** | 8000 | API Gateway | http://localhost:8000/docs |
| **Agent** | 9000 | AI Matching | http://localhost:9000/docs |
| **LangGraph** | 9001 | Workflows | http://localhost:9001/docs |
| **HR Portal** | 8501 | HR Dashboard | http://localhost:8501 |
| **Client Portal** | 8502 | Client Interface | http://localhost:8502 |
| **Candidate Portal** | 8503 | Job Applications | http://localhost:8503 |

---

## **🚨 Troubleshooting**

### **Problem: Python not found**
```bash
Solution:
1. Install Python 3.12.7 from https://python.org
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt
4. Run setup_first_time.bat again
```

### **Problem: Port already in use**
```bash
Solution:
1. Run stop_all_services.bat
2. Wait 10 seconds
3. Run start_all_services.bat again
```

### **Problem: Service not responding**
```bash
Solution:
1. Check .env file has correct credentials
2. Run check_services.bat to see which service failed
3. Look at the individual service window for error messages
```

### **Problem: Database connection error**
```bash
Solution:
1. Install PostgreSQL locally, OR
2. Use a shared database URL in .env file, OR
3. Use the live production system instead:
   https://bhiv-hr-portal-u670.onrender.com/
```

---

## **💡 Tips**

### **For Development:**
- Each service runs in its own Command Prompt window
- You can see real-time logs in each window
- Edit code and restart individual services as needed

### **For Production Use:**
- Use the live system: https://bhiv-hr-portal-u670.onrender.com/
- No setup required, works immediately
- Same features as local installation

### **For Team Handover:**
- Share the entire project folder
- Team member runs setup_first_time.bat
- They edit .env with their own credentials
- They run start_all_services.bat

---

## **🎯 Comparison: BAT Scripts vs Docker vs Live System**

| Method | Setup Time | Complexity | Best For |
|--------|------------|------------|----------|
| **BAT Scripts** | 10 minutes | Medium | Local development |
| **Docker** | 30 minutes | High | Production-like environment |
| **Live System** | 30 seconds | None | Immediate use |

**Recommendation**: Use live system for quick access, BAT scripts for development.

---

**Created**: January 2025  
**Compatible**: Windows 10/11  
**Python**: 3.12.7 required  
**Status**: ✅ Tested and working