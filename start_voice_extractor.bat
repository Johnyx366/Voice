@echo off
echo 🎬 Voice Extractor - Inicio Rapido
echo =================================

REM Verificar si existe el entorno virtual
if not exist "venv\Scripts\python.exe" (
    echo ⚠️  Entorno virtual no encontrado
    echo 🛠️  Ejecuta primero: install_and_build.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔋 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar dependencias principales
echo 🔍 Verificando dependencias...
python -c "import whisper, torch, tkinter" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Dependencias no instaladas correctamente
    echo 🛠️  Ejecuta: install_and_build.bat
    pause
    exit /b 1
)

REM Verificar FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  FFmpeg no encontrado en PATH
    echo 🔧 Verificando instalacion local...
    if exist "ffmpeg\ffmpeg.exe" (
        echo ✅ FFmpeg encontrado localmente
        set "PATH=%CD%\ffmpeg;%PATH%"
    ) else (
        echo ❌ FFmpeg no instalado
        echo 🛠️  Ejecuta: install_ffmpeg.bat
        pause
        exit /b 1
    )
)

echo ✅ Todo listo!
echo 🚀 Iniciando Voice Extractor...

REM Ejecutar la aplicacion
python Voice_extractor.py

REM Pausa solo si hay error
if %errorlevel% neq 0 (
    echo ❌ Error al ejecutar la aplicacion
    pause
)
