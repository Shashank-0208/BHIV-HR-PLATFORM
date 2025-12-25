@echo off
REM BHIV HR Platform - Database Restoration Script (Windows)
REM Restores data from JSON backup to PostgreSQL database running in Docker
REM Version: 1.0.0

echo [INFO] BHIV HR Platform - Database Restoration
echo ===========================================

REM Check if backup file exists
if not exist "database_backup.json" (
    echo [ERROR] Backup file not found: database_backup.json
    echo    Please run extract_database.bat first to create a backup.
    pause
    exit /b 1
)

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

REM Show backup info
echo [INFO] Backup file information:
python -c "import json,os; data=json.load(open('database_backup.json')); metadata=data.get('metadata',{}); print(f'   Date: {metadata.get(\"extraction_date\",\"Unknown\")}'); print(f'   Version: {metadata.get(\"version\",\"Unknown\")}'); print(f'   Tables: {metadata.get(\"total_tables\",0)}'); print(f'   Records: {metadata.get(\"total_records\",0)}'); file_size=os.path.getsize('database_backup.json'); print(f'   File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')"

echo.
set /p CONFIRM="[WARNING] This will REPLACE all existing data. Continue? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo [ERROR] Restoration cancelled.
    pause
    exit /b 1
)

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

REM Run restoration script
echo [INFO] Starting data restoration...
python restore_database.py

if errorlevel 1 (
    echo [ERROR] Database restoration failed!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Database restoration completed successfully!

REM Verify restoration
echo.
echo [INFO] Verifying restoration...
python -c "import psycopg2,os; db_config={'host':os.getenv('DB_HOST','localhost'),'port':os.getenv('DB_PORT','5432'),'database':os.getenv('POSTGRES_DB','bhiv_hr'),'user':os.getenv('POSTGRES_USER','bhiv_user'),'password':os.getenv('POSTGRES_PASSWORD','your_password_here')}; conn=psycopg2.connect(**db_config); cursor=conn.cursor(); [print(f'   {table}: {cursor.execute(f\"SELECT COUNT(*) FROM {table}\") or cursor.fetchone()[0]} records') for table in ['candidates','jobs','users','clients','feedback']]; cursor.close(); conn.close(); print('[OK] Verification completed')"

echo.
echo [INFO] Database restoration completed!
echo    All data has been restored from the backup file.
echo    You can now start the application services.

pause