@echo off
echo Installing FFmpeg...
echo This script will download and install FFmpeg for Windows

REM Create ffmpeg directory
if not exist "ffmpeg" mkdir ffmpeg
cd ffmpeg

REM Download FFmpeg (you may need to update this URL to the latest version)
echo Downloading FFmpeg...
powershell -Command "Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip'"

REM Extract FFmpeg
echo Extracting FFmpeg...
powershell -Command "Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.'"

REM Move ffmpeg.exe to a more accessible location
for /d %%i in (ffmpeg-*) do (
    move "%%i\bin\ffmpeg.exe" ".\"
    move "%%i\bin\ffprobe.exe" ".\"
    rmdir /s /q "%%i"
)

REM Clean up
del ffmpeg.zip

echo FFmpeg installed successfully!
echo Please add %CD% to your PATH environment variable or use the full path to ffmpeg.exe

pause
