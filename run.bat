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
echo Processing Videos (Download + Transcribe)
echo ============================================
echo.
echo [INFO] Using Whisper 'base' model (good balance of speed and accuracy)
echo [INFO] Edit run.bat to change model: tiny, base, small, medium, or large
echo [INFO] Processing one video at a time (download then transcribe)
echo.
python process_videos.py %2 %1 base

if errorlevel 1 (
    echo [ERROR] Processing failed
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
