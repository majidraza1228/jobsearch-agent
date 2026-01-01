@echo off
REM Job Search AI Agent - Quick Start Script (Windows)

echo ==================================
echo Job Search AI Agent - Quick Start
echo ==================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys
    echo.
    echo copy .env.example .env
    echo.
    pause
)

REM Initialize database if it doesn't exist
if not exist "jobs.db" (
    echo Initializing database...
    python src\database\init_db.py
)

echo.
echo ==================================
echo Setup complete!
echo ==================================
echo.
echo Choose an option:
echo 1. Run API Server (for n8n integration)
echo 2. Search for jobs (CLI)
echo 3. List jobs from database
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting API server...
    echo API will be available at http://localhost:5000
    echo Press Ctrl+C to stop
    echo.
    python src\api\server.py
) else if "%choice%"=="2" (
    echo.
    set /p keywords="Enter job keywords (e.g., 'Python Developer'): "
    set /p location="Enter location (e.g., 'Remote'): "
    echo.
    echo Searching for jobs...
    python -m src.main --search "%keywords%" --location "%location%" --limit 10
) else if "%choice%"=="3" (
    echo.
    python -m src.main --list --limit 20
) else if "%choice%"=="4" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice!
    exit /b 1
)
