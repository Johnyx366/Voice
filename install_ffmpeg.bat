@echo off
echo 🎥 Instalando FFmpeg para Windows...
echo ===================================

REM Verificar si FFmpeg ya esta instalado
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ FFmpeg ya esta instalado en el sistema
    goto :end
)

REM Verificar si existe en directorio local
if exist "ffmpeg\ffmpeg.exe" (
    echo ✅ FFmpeg encontrado en directorio local
    goto :end
)

echo 📥 Descargando e instalando FFmpeg...

REM Crear directorio ffmpeg
if not exist "ffmpeg" mkdir ffmpeg
cd ffmpeg

REM Descargar FFmpeg usando PowerShell
echo Descargando FFmpeg essentials...
powershell -Command "try { Invoke-WebRequest -Uri 'https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip' -OutFile 'ffmpeg.zip' -UserAgent 'Mozilla/5.0' } catch { Write-Host 'Error al descargar FFmpeg'; exit 1 }"

if not exist "ffmpeg.zip" (
    echo ❌ Error al descargar FFmpeg
    echo Intentando URL alternativa...
    powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip' -UserAgent 'Mozilla/5.0' } catch { Write-Host 'Error con URL alternativa'; exit 1 }"
)

if not exist "ffmpeg.zip" (
    echo ❌ No se pudo descargar FFmpeg
    echo Por favor descarga manualmente desde: https://ffmpeg.org/download.html
    pause
    exit /b 1
)

REM Extraer FFmpeg
echo 📂 Extrayendo FFmpeg...
powershell -Command "try { Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force } catch { Write-Host 'Error al extraer'; exit 1 }"

REM Mover ejecutables a directorio accesible
echo 🔧 Configurando FFmpeg...
for /d %%i in (ffmpeg-*) do (
    if exist "%%i\bin\ffmpeg.exe" (
        copy "%%i\bin\ffmpeg.exe" ".\" >nul
        copy "%%i\bin\ffprobe.exe" ".\" >nul
        echo ✅ FFmpeg copiado exitosamente
        rmdir /s /q "%%i" >nul 2>&1
        goto :cleanup
    )
)

:cleanup
REM Limpiar archivos temporales
if exist "ffmpeg.zip" del "ffmpeg.zip" >nul

REM Verificar instalacion
if exist "ffmpeg.exe" (
    echo ✅ FFmpeg instalado correctamente en: %CD%
    echo 📝 Agregando al PATH del sistema...
    
    REM Agregar al PATH de la sesion actual
    set "PATH=%CD%;%PATH%"
    
    echo ✅ FFmpeg listo para usar
) else (
    echo ❌ Error en la instalacion de FFmpeg
    pause
    exit /b 1
)

cd ..

:end
echo ✅ FFmpeg configurado correctamente

pause
