@echo off
echo ========================================
echo 🛑 BHIV HR Platform - Stop All Services
echo ========================================
echo.

echo Stopping all BHIV HR Platform services...
echo.

REM Kill processes by port
echo Stopping Gateway Service (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1

echo Stopping AI Agent Service (Port 9000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9000') do taskkill /f /pid %%a >nul 2>&1

echo Stopping LangGraph Service (Port 9001)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9001') do taskkill /f /pid %%a >nul 2>&1

echo Stopping HR Portal (Port 8501)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do taskkill /f /pid %%a >nul 2>&1

echo Stopping Client Portal (Port 8502)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8502') do taskkill /f /pid %%a >nul 2>&1

echo Stopping Candidate Portal (Port 8503)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8503') do taskkill /f /pid %%a >nul 2>&1

REM Kill any remaining Python/Streamlit processes related to BHIV
echo Cleaning up remaining processes...
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq BHIV*" >nul 2>&1
taskkill /f /im "streamlit.exe" /fi "WINDOWTITLE eq BHIV*" >nul 2>&1

echo.
echo ✅ All BHIV HR Platform services stopped
echo.
echo 🔄 To start services again, run: start_all_services.bat
echo.
pause