@echo off
echo 🎬 Voice Extractor - Instalador Completo
echo =========================================

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no esta instalado
    echo Por favor instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 🔧 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔋 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo 📦 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📚 Instalando dependencias de Python...
pip install -r requirements.txt

REM Instalar PyInstaller si no esta
pip install pyinstaller

REM Instalar FFmpeg
echo 🎥 Instalando FFmpeg...
call install_ffmpeg.bat

echo ✅ Instalacion completada

REM Ejecutar compilador
echo 🚀 Iniciando compilacion del ejecutable...
python build_exe.py

pause
