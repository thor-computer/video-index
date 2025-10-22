@echo off
echo ============================================
echo Video Index - Download and Transcribe
echo ============================================
echo.

REM Check if parameter was provided
if not "%~1"=="" (
    set MAX_VIDEOS=%~1
    echo [INFO] Limiting to %MAX_VIDEOS% most recent videos
    echo.
) else (
    set MAX_VIDEOS=
)

REM Prompt for YouTube channel URL
set /p CHANNEL_URL="Enter YouTube channel/profile URL: "

if "%CHANNEL_URL%"=="" (
    echo [ERROR] No URL provided
    pause
    exit /b 1
)

REM Optionally prompt for max videos if not provided as parameter
if "%MAX_VIDEOS%"=="" (
    echo.
    echo [OPTIONAL] Enter max number of videos to download (leave empty for all):
    set /p MAX_VIDEOS="Max videos (or press Enter for all): "
)

echo.
echo [SETUP] Creating virtual environment...
python -m venv venv

echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo [SETUP] Upgrading pip...
python -m pip install --upgrade pip

echo [SETUP] Installing dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo STEP 1: Downloading Videos
echo ============================================
echo.
if "%MAX_VIDEOS%"=="" (
    python downloader.py "%CHANNEL_URL%"
) else (
    echo [INFO] Downloading %MAX_VIDEOS% most recent videos
    python downloader.py "%CHANNEL_URL%" %MAX_VIDEOS%
)

if errorlevel 1 (
    echo [ERROR] Download failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo STEP 2: Transcribing Videos
echo ============================================
echo.
echo [INFO] Using Whisper 'base' model (good balance of speed and accuracy)
echo [INFO] You can edit run.bat to use: tiny, base, small, medium, or large
echo.
python transcriber.py base

if errorlevel 1 (
    echo [ERROR] Transcription failed
    pause
    exit /b 1
)

echo.
echo ============================================
echo COMPLETE!
echo ============================================
echo.
echo Videos saved to: videos\
echo Transcripts saved to: transcripts\
echo.
echo Use search.bat to search the transcripts
echo.
pause
