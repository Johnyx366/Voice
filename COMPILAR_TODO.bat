@echo off
title Voice Extractor - Compilador Automático
color 0A

echo.
echo  ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗
echo  ██║   ██║██╔═══██╗██║██╔════╝██╔════╝
echo  ██║   ██║██║   ██║██║██║     █████╗  
echo  ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝  
echo   ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗
echo    ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝
echo.
echo  ███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗ ██████╗ ██████╗ 
echo  ██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
echo  █████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ██║   ██║██████╔╝
echo  ██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ██║   ██║██╔══██╗
echo  ███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║
echo  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
echo.
echo                              Powered by OpenAI Whisper
echo.
echo ══════════════════════════════════════════════════════════════════════════════
echo  🚀 COMPILADOR AUTOMÁTICO - Un clic para todo
echo ══════════════════════════════════════════════════════════════════════════════
echo.
echo  Este script automatiza COMPLETAMENTE el proceso:
echo.
echo    1. ✅ Instala todas las dependencias
echo    2. 🔐 Crea certificado autofirmado  
echo    3. 🔨 Compila el ejecutable
echo    4. ✍️  Firma digitalmente
echo    5. 📦 Crea paquete de distribución
echo    6. 🗜️  Genera ZIP final
echo.
echo  💡 Solo tienes que esperar y al final tendrás todo listo!
echo.
echo ══════════════════════════════════════════════════════════════════════════════

set /p confirm="🤖 ¿Continuar con la compilación automática? (S/N): "
if /i not "%confirm%"=="S" (
    echo ❌ Proceso cancelado
    pause
    exit /b 0
)

echo.
echo 🚀 Iniciando proceso automático...
echo ⏱️  Esto puede tomar varios minutos...
echo.

REM Ejecutar el script maestro de Python
python build_master.py

REM Verificar si se completó exitosamente
if exist "VoiceExtractor_v1.0_Windows.zip" (
    echo.
    echo 🎉 ¡ÉXITO TOTAL!
    echo.
    echo 📁 Archivo final creado: VoiceExtractor_v1.0_Windows.zip
    echo 📊 Tamaño: 
    for %%I in ("VoiceExtractor_v1.0_Windows.zip") do echo    %%~zI bytes
    echo.
    echo 🎯 PARA DISTRIBUIR:
    echo    1. Comparte el archivo VoiceExtractor_v1.0_Windows.zip
    echo    2. Los usuarios solo necesitan descomprimir y ejecutar INSTALAR.bat
    echo    3. ¡Todo funciona automáticamente!
    echo.
    set /p open="📂 ¿Abrir carpeta con el archivo final? (S/N): "
    if /i "%open%"=="S" (
        explorer .
    )
) else (
    echo.
    echo ❌ Algo salió mal en el proceso
    echo 💡 Revisa los mensajes de error arriba
    echo.
)

echo.
echo 🏁 Proceso finalizado
pause
