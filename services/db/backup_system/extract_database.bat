@echo off
REM BHIV HR Platform - Database Extraction Script (Windows)
REM Extracts all data from the PostgreSQL database running in Docker
REM Version: 1.0.0

echo [INFO] BHIV HR Platform - Database Extraction
echo ==========================================

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

REM Check if database container is running
for /f %%i in ('docker-compose -f ..\..\docker-compose.production.yml ps -q db') do set DB_CONTAINER=%%i
if "%DB_CONTAINER%"=="" (
    echo [ERROR] Database container is not running. Starting services...
    docker-compose -f ..\..\docker-compose.production.yml up -d db
    echo [INFO] Waiting for database to be ready...
    timeout /t 10 /nobreak >nul
)

REM Load environment variables from .env file
if exist .env (
    for /f "usebackq tokens=1,2 delims==" %%a in (.env) do (
        if not "%%a"=="" if not "%%a:~0,1%"=="#" set %%a=%%b
    )
)

REM Set default values if not in environment
if "%POSTGRES_DB%"=="" set POSTGRES_DB=bhiv_hr
if "%POSTGRES_USER%"=="" set POSTGRES_USER=bhiv_user
if "%POSTGRES_PASSWORD%"=="" set POSTGRES_PASSWORD=your_password_here
if "%DB_HOST%"=="" set DB_HOST=127.0.0.1
if "%DB_PORT%"=="" set DB_PORT=5432

echo [INFO] Database Configuration:
echo    Host: %DB_HOST%
echo    Port: %DB_PORT%
echo    Database: %POSTGRES_DB%
echo    User: %POSTGRES_USER%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

REM Install Python dependencies if needed
python -c "import psycopg2" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing required Python packages...
    pip install psycopg2-binary
)

REM Run extraction script
echo [INFO] Starting data extraction...
cd backup_system
python extract_database.py

if errorlevel 1 (
    echo [ERROR] Database extraction failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Database extraction completed successfully!
echo [INFO] Backup file: backup_system\database_backup.json

REM Show file info
if exist "database_backup.json" (
    for %%A in ("database_backup.json") do set FILE_SIZE=%%~zA
    echo [INFO] File size: !FILE_SIZE! bytes
    
    echo.
    echo [INFO] Backup metadata:
    python -c "import json; data=json.load(open('database_backup.json')); metadata=data.get('metadata',{}); print(f'   Date: {metadata.get(\"extraction_date\",\"Unknown\")}'); print(f'   Version: {metadata.get(\"version\",\"Unknown\")}'); print(f'   Tables: {metadata.get(\"total_tables\",0)}'); print(f'   Records: {metadata.get(\"total_records\",0)}')"
)

echo.
echo [INFO] Next steps:
echo    1. Backup file is ready: services\db\database_backup.json
echo    2. To restore: restore_database.bat
echo    3. To extract again: extract_database.bat

pause