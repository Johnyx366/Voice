@echo off
echo Voice to Text Extractor - Starting...
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Voice to Text Extractor...
python voice_extractor.py

pause
