@echo off
echo ============================================
echo Video Index - Web Interface
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

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Flask not found. Installing...
    pip install flask>=3.0.0
)

echo [INFO] Starting web server...
echo [INFO] Open http://localhost:5000 in your browser
echo.

REM Run the web server
python web_server.py
