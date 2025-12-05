@echo off
echo ========================================
echo 🚀 BHIV HR Platform - First Time Setup
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed
    echo.
    echo Please install Python 3.12.7 from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version
echo.

REM Check if .env exists
if not exist ".env" (
    echo 📝 Creating .env file from template...
    copy ".env.example" ".env"
    echo.
    echo ⚠️  IMPORTANT: Edit .env file with your credentials
    echo.
    echo Required settings:
    echo ├── DATABASE_URL=postgresql://user:pass@localhost:5432/bhiv_hr
    echo ├── API_KEY_SECRET=your_api_key_here
    echo ├── JWT_SECRET_KEY=your_jwt_secret_here
    echo └── Other API keys for external services
    echo.
    echo 📝 Opening .env file for editing...
    notepad .env
    echo.
    echo After editing .env file, run: start_all_services.bat
    pause
    exit /b 0
) else (
    echo ✅ .env file already exists
)

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo 🚀 Next Steps:
echo 1. Make sure your .env file has correct credentials
echo 2. Run: start_all_services.bat
echo 3. Wait 60 seconds for services to start
echo 4. Open: http://localhost:8501 (HR Portal)
echo 5. Login with: TECH001 / demo123
echo.
echo 📚 Available Scripts:
echo ├── start_all_services.bat  - Start all services
echo ├── stop_all_services.bat   - Stop all services
echo ├── check_services.bat      - Check service health
echo └── setup_first_time.bat    - This setup script
echo.
pause