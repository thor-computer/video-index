@echo off
echo ============================================
echo Video Index - Search Transcripts
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

REM Prompt for search query
set /p SEARCH_QUERY="Enter search query: "

if "%SEARCH_QUERY%"=="" (
    echo [ERROR] No search query provided
    pause
    exit /b 1
)

echo.
echo [SEARCH] Searching for: "%SEARCH_QUERY%"
echo.

REM Run the search
python searcher.py %SEARCH_QUERY%

echo.
pause
