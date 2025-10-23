@echo off
echo ============================================
echo Video Index - Build Static Site
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

echo [INFO] Building static site bundle...
echo.

REM Run the build script
python build_static.py

echo.
pause
