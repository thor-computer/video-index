@echo off
echo ============================================
echo Video Index - Local Web Server
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found. Please run run.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

echo [INFO] Starting local web server...
echo [INFO] Open http://localhost:8000 in your browser
echo [INFO] Press Ctrl+C to stop
echo.

REM Start simple HTTP server in the docs directory
cd docs
python -m http.server 8000
