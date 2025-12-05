@echo off
echo ========================================
echo 🚀 BHIV HR Platform - Start All Services
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.12.7 from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from template...
    copy ".env.example" ".env"
    echo.
    echo 📝 Please edit .env file with your credentials before running again
    echo Example: DATABASE_URL, API_KEY_SECRET, etc.
    pause
    exit /b 1
)

echo ✅ Environment file found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo ✅ Virtual environment ready
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies for all services
echo 📦 Installing dependencies...
echo.

echo Installing Gateway dependencies...
cd services\gateway
pip install -r requirements.txt --quiet
cd ..\..

echo Installing Agent dependencies...
cd services\agent
pip install -r requirements.txt --quiet
cd ..\..

echo Installing LangGraph dependencies...
cd services\langgraph
pip install -r requirements.txt --quiet
cd ..\..

echo Installing Portal dependencies...
cd services\portal
pip install -r requirements.txt --quiet
cd ..\..

echo Installing Client Portal dependencies...
cd services\client_portal
pip install -r requirements.txt --quiet
cd ..\..

echo Installing Candidate Portal dependencies...
cd services\candidate_portal
pip install -r requirements.txt --quiet
cd ..\..

echo ✅ All dependencies installed
echo.

REM Start services in background
echo 🚀 Starting all services...
echo.

REM Start Gateway Service (Port 8000)
echo Starting Gateway Service on port 8000...
start "BHIV Gateway" cmd /k "cd /d %cd%\services\gateway && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
timeout /t 3 /nobreak >nul

REM Start Agent Service (Port 9000)
echo Starting AI Agent Service on port 9000...
start "BHIV Agent" cmd /k "cd /d %cd%\services\agent && python -m uvicorn app:app --host 0.0.0.0 --port 9000"
timeout /t 3 /nobreak >nul

REM Start LangGraph Service (Port 9001)
echo Starting LangGraph Service on port 9001...
start "BHIV LangGraph" cmd /k "cd /d %cd%\services\langgraph && python -m uvicorn app.main:app --host 0.0.0.0 --port 9001"
timeout /t 3 /nobreak >nul

REM Start HR Portal (Port 8501)
echo Starting HR Portal on port 8501...
start "BHIV HR Portal" cmd /k "cd /d %cd%\services\portal && streamlit run app.py --server.port 8501 --server.address 0.0.0.0"
timeout /t 3 /nobreak >nul

REM Start Client Portal (Port 8502)
echo Starting Client Portal on port 8502...
start "BHIV Client Portal" cmd /k "cd /d %cd%\services\client_portal && streamlit run app.py --server.port 8502 --server.address 0.0.0.0"
timeout /t 3 /nobreak >nul

REM Start Candidate Portal (Port 8503)
echo Starting Candidate Portal on port 8503...
start "BHIV Candidate Portal" cmd /k "cd /d %cd%\services\candidate_portal && streamlit run app.py --server.port 8503 --server.address 0.0.0.0"
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo ✅ All Services Started Successfully!
echo ========================================
echo.
echo 🌐 Service URLs:
echo ├── Gateway API:      http://localhost:8000
echo ├── AI Agent API:     http://localhost:9000  
echo ├── LangGraph API:    http://localhost:9001
echo ├── HR Portal:        http://localhost:8501
echo ├── Client Portal:    http://localhost:8502
echo └── Candidate Portal: http://localhost:8503
echo.
echo 📚 API Documentation:
echo ├── Gateway Docs:     http://localhost:8000/docs
echo ├── Agent Docs:       http://localhost:9000/docs
echo └── LangGraph Docs:   http://localhost:9001/docs
echo.
echo 🔑 Demo Credentials:
echo ├── Client Portal:    TECH001 / demo123
echo └── API Key:          Check your .env file
echo.
echo ⏳ Please wait 30-60 seconds for all services to fully start...
echo.
echo 🔄 To stop all services: Close all command windows or run stop_all_services.bat
echo.
pause