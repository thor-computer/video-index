@echo off
echo ============================================
echo Video Index - Download and Transcribe
echo ============================================
echo.
echo Usage: run.bat [max_videos] [channel_url]
echo Example: run.bat 3 https://www.youtube.com/@channelname
echo.

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
python downloader.py %2 %1

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
