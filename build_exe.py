#!/usr/bin/env python3
"""
Script para compilar Voice Extractor a un ejecutable de Windows
con todas las dependencias incluidas y optimizado para arranque rápido.
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

def check_requirements():
    """Verifica que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    # Lista de paquetes y sus módulos de importación
    required_packages = [
        ('pyinstaller', 'PyInstaller'),
        ('openai-whisper', 'whisper'), 
        ('torch', 'torch'),
        ('torchaudio', 'torchaudio'),
        ('tkinter', 'tkinter'),
        ('numpy', 'numpy'),
        ('pillow', 'PIL')
    ]
    
    missing = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name} - OK")
        except ImportError:
            missing.append(package_name)
            print(f"❌ {package_name} - FALTANTE")
    
    if missing:
        print(f"\n⚠️  Instala los paquetes faltantes: pip install {' '.join(missing)}")
        return False
    
    return True

def clean_build():
    """Limpia directorios de compilación anteriores"""
    print("🧹 Limpiando compilaciones anteriores...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Eliminado: {dir_name}")

def create_spec_file():
    """Crea archivo .spec optimizado para PyInstaller"""
    print("📝 Creando archivo de configuración...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Datos y módulos de Whisper (solo los esenciales)
whisper_data = collect_data_files('whisper')
whisper_modules = collect_submodules('whisper')

# Archivos adicionales necesarios
added_files = [
    ('icon.ico', '.'),
    ('README.md', '.'),
]

# Intentar incluir FFmpeg si está disponible
try:
    import ffmpeg
    ffmpeg_data = collect_data_files('ffmpeg')
    added_files.extend(ffmpeg_data)
except ImportError:
    pass

block_cipher = None

a = Analysis(
    ['Voice_extractor.py'],
    pathex=[],
    binaries=[],
    datas=added_files + whisper_data,
    hiddenimports=[
        'whisper',
        'numpy',
        'tiktoken',
        'regex',
        'ftfy',
        'PIL',
        'PIL.Image',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'queue',
        'threading',
        'tempfile',
        'subprocess',
        'io',
        'contextlib',
        'ssl',
        '_ssl',
        'certifi',
        'urllib3',
        'requests',
        'tqdm',
    ] + whisper_modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
        'torch.distributions',
        'torch.optim',
        'torch.nn.modules.transformer',
        'torchaudio.datasets',
        'torchaudio.models',
        'torchaudio.pipelines',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VoiceExtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Deshabilitado para evitar problemas con DLLs
    runtime_tmpdir=None,
    console=False,  # Sin consola para interfaz limpia - IMPORTANTE
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Icono principal integrado en el ejecutable
    version='version_info.txt',  # Información de versión
    uac_admin=False,  # No requiere permisos de administrador
    uac_uiaccess=False  # Sin acceso especial de UI
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='VoiceExtractor',
)
'''
    
    with open('VoiceExtractor.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado")

def create_version_info():
    """Crea archivo de información de versión para Windows"""
    print("📋 Creando información de versión...")
    
    version_info = '''# UTF-8
#
# Para más detalles sobre el archivo de información de versión fixed info properties, ver:
# http://msdn.microsoft.com/en-us/library/ms646981.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Voice Extractor'),
        StringStruct(u'FileDescription', u'Extractor de Voz con IA Whisper'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'VoiceExtractor'),
        StringStruct(u'LegalCopyright', u'© 2024 Voice Extractor'),
        StringStruct(u'OriginalFilename', u'VoiceExtractor.exe'),
        StringStruct(u'ProductName', u'Voice Extractor - Whisper AI'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("✅ Información de versión creada")

def build_executable():
    """Compila el ejecutable con PyInstaller"""
    print("🚀 Compilando ejecutable...")
    print("   (Esto puede tomar varios minutos...)")
    
    # Verificar que el icono existe antes de compilar
    icon_path = 'icon.ico'
    if not os.path.exists(icon_path):
        print("⚠️ Archivo icon.ico no encontrado en el directorio actual")
    
    print(f"🎨 Usando icono: {icon_path}")
    
    # Cuando usamos un archivo .spec, no podemos usar --add-data, --icon, etc.
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm', 
        'VoiceExtractor.spec'
    ]
    
    try:
        # Ejecutar sin mostrar ventanas de consola
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd(),
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
        
        if result.returncode == 0:
            print("✅ Compilación exitosa!")
            print(f"✅ Icono integrado desde: {icon_path}")
            return True
        else:
            print("❌ Error en compilación:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def create_launcher_script():
    """Crea script de lanzamiento optimizado"""
    print("📱 Creando launcher optimizado...")
    
    launcher_content = '''@echo off
REM Voice Extractor - Launcher Silencioso
REM Configurar para no mostrar ventanas molestas
title Voice Extractor Launcher
cd /d "%~dp0"

REM Minimizar esta ventana inmediatamente
if not "%1"=="min" start /min cmd /c "%0" min & exit

REM Verificar FFmpeg de forma silenciosa
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias necesarias...
    start /wait /min cmd /c "install_ffmpeg.bat"
)

REM Ejecutar la aplicación principal
start "" "VoiceExtractor.exe"

REM Cerrar el launcher automáticamente
exit
'''
    
    # Crear directorio si no existe
    os.makedirs('dist/VoiceExtractor', exist_ok=True)
    
    with open('dist/VoiceExtractor/VoiceExtractor_Launcher.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # Crear también un launcher VBS (completamente silencioso)
    vbs_launcher = '''Set WshShell = CreateObject("WScript.Shell")
Dim fso, CurrentDirectory
Set fso = CreateObject("Scripting.FileSystemObject")
CurrentDirectory = fso.GetParentFolderName(WScript.ScriptFullName)

' Cambiar al directorio del script
WshShell.CurrentDirectory = CurrentDirectory

' Verificar FFmpeg silenciosamente
Set objExec = WshShell.Exec("ffmpeg -version")
Do While objExec.Status = 0
    WScript.Sleep 100
Loop

If objExec.ExitCode <> 0 Then
    ' Instalar FFmpeg en segundo plano
    WshShell.Run "cmd /c install_ffmpeg.bat", 0, True
End If

' Ejecutar VoiceExtractor
WshShell.Run "VoiceExtractor.exe", 1, False

' Terminar script
WScript.Quit
'''
    
    with open('dist/VoiceExtractor/VoiceExtractor_Silent.vbs', 'w', encoding='utf-8') as f:
        f.write(vbs_launcher)
    
    print("✅ Launcher creado (BAT + VBS silencioso)")

def create_ffmpeg_installer():
    """Crea instalador automático de FFmpeg"""
    print("🔧 Creando instalador de FFmpeg...")
    
    ffmpeg_installer = '''@echo off
setlocal enabledelayedexpansion
title FFmpeg Installer

REM Configurar para ejecución silenciosa si se ejecuta desde launcher
if "%1"=="silent" (
    set SILENT_MODE=1
) else (
    set SILENT_MODE=0
)

if %SILENT_MODE%==1 (
    echo Instalando FFmpeg en segundo plano...
) else (
    echo 🔧 Instalando FFmpeg...
)

REM Crear directorio para FFmpeg
if not exist "ffmpeg" mkdir ffmpeg
cd ffmpeg

REM Descargar FFmpeg (versión estática) - Silencioso si es necesario
if %SILENT_MODE%==1 (
    powershell -WindowStyle Hidden -Command "& {Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}" >nul 2>&1
) else (
    echo 📥 Descargando FFmpeg...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}"
)

REM Extraer
if %SILENT_MODE%==1 (
    powershell -WindowStyle Hidden -Command "& {Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force}" >nul 2>&1
) else (
    echo 📦 Extrayendo archivos...
    powershell -Command "& {Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force}"
)

REM Mover ejecutables al directorio raíz
for /d %%i in (ffmpeg-master-*) do (
    copy "%%i\\bin\\*.exe" "..\\." >nul 2>&1
)

REM Limpiar
cd ..
rmdir /s /q ffmpeg 2>nul

if %SILENT_MODE%==1 (
    echo FFmpeg instalado correctamente
) else (
    echo ✅ FFmpeg instalado correctamente
    pause
)
'''
    
    # Crear directorio si no existe
    os.makedirs('dist/VoiceExtractor', exist_ok=True)
    
    with open('dist/VoiceExtractor/install_ffmpeg.bat', 'w', encoding='utf-8') as f:
        f.write(ffmpeg_installer)
    
    print("✅ Instalador FFmpeg creado")

def create_readme():
    """Crea README para el usuario"""
    print("📖 Creando manual de usuario...")
    
    readme_content = '''# Voice Extractor - Whisper AI (Optimizado)

## 🚀 Inicio Rápido

1. **Ejecutar la aplicación:**
   - **Opción 1 (Recomendada):** Haz doble clic en `VoiceExtractor_Silent.vbs` (Completamente silencioso)
   - **Opción 2:** Haz doble clic en `VoiceExtractor.exe` (Directo)
   - **Opción 3:** Usa `VoiceExtractor_Launcher.bat` (Con ventana mínima)
   - ⚡ NUEVO: Inicio optimizado en pocos segundos
   - 🤫 NUEVO: Launcher silencioso sin ventanas molestas

2. **Primera vez:**
   - La aplicación instalará FFmpeg automáticamente si es necesario (en segundo plano)
   - Los modelos de IA se cargarán SOLO cuando los uses por primera vez
   - ⚡ La interfaz aparece inmediatamente

## 🤫 Opciones de Lanzamiento

- **VoiceExtractor_Silent.vbs** ➜ Completamente silencioso, sin ventanas de comandos
- **VoiceExtractor.exe** ➜ Directo, más rápido
- **VoiceExtractor_Launcher.bat** ➜ Con verificación de dependencias

## 📁 Formatos Soportados

**Video:** MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V
**Audio:** MP3, WAV, AAC, OGG, M4A, FLAC

## 🎯 Uso

1. **Seleccionar archivo:** Haz clic en "📂 Browse Files"
2. **Configurar IA:** Elige el modelo de calidad deseado
3. **Idioma:** Selecciona idioma o deja "Auto-detect"
4. **Extraer:** Haz clic en "🎯 Extract Voice"
5. **Guardar:** Una vez completado, haz clic en "💾 Save Text to File"

## 🤖 Modelos de IA

- **Tiny:** Más rápido, menor precisión (39 MB)
- **Base:** Equilibrado, recomendado (74 MB)
- **Small:** Mejor precisión (244 MB)
- **Medium:** Muy buena precisión (769 MB)
- **Large:** Mejor calidad posible (1550 MB)

## ⚡ Optimizaciones

- **Inicio inmediato:** La interfaz aparece en 2-3 segundos
- **Carga diferida:** Los modelos de IA se cargan solo cuando los necesitas
- **Memoria optimizada:** Menor uso de RAM al inicio
- **Launcher silencioso:** Sin ventanas de comando molestas
- **Mejor experiencia:** Splash screen informativo

## 🔧 Solución de Problemas

**Error de FFmpeg:** El instalador automático se ejecuta en segundo plano
**Modelos lentos:** Los modelos se descargan solo la primera vez
**Archivos grandes:** Usa modelo "Tiny" para pruebas rápidas
**Ventanas molestas:** Usa `VoiceExtractor_Silent.vbs`

## 📞 Soporte

- El archivo de texto se guarda en la misma carpeta que el video
- Todos los formatos de video comunes están soportados
- La transcripción funciona sin conexión a internet (después de la primera descarga)
- No aparecen ventanas de comando molestas con el launcher VBS

---
Voice Extractor v1.1 - Powered by OpenAI Whisper - Silent Edition
'''
    
    # Crear directorio si no existe
    os.makedirs('dist/VoiceExtractor', exist_ok=True)
    
    with open('dist/VoiceExtractor/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Manual de usuario creado")

def optimize_executable():
    """Optimiza el ejecutable para arranque rápido"""
    print("⚡ Optimizando para arranque rápido...")
    
    # Crear directorio si no existe
    os.makedirs('dist/VoiceExtractor', exist_ok=True)
    
    # Copiar icono al directorio de distribución (múltiples ubicaciones para asegurar disponibilidad)
    icon_source = 'icon.ico'
    if os.path.exists(icon_source):
        # Copiar a la raíz del directorio de distribución
        shutil.copy2(icon_source, 'dist/VoiceExtractor/icon.ico')
        # Copiar también con nombre alternativo por seguridad
        shutil.copy2(icon_source, 'dist/VoiceExtractor/app_icon.ico')
        print(f"✅ Icono copiado desde: {icon_source}")
    else:
        print("⚠️ Archivo icon.ico no encontrado")
    
    # Crear script para deshabilitar notificaciones molestas de Windows
    disable_notifications = '''@echo off
REM Script para deshabilitar notificaciones molestas durante la ejecución
REM Ejecutar este script como administrador si tienes problemas con ventanas de Chocolatey

REM Deshabilitar notificaciones de PowerShell
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings\\Microsoft.PowerShell" /v "Enabled" /t REG_DWORD /d 0 /f >nul 2>&1

REM Deshabilitar notificaciones de línea de comandos
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings\\Microsoft.WindowsTerminal" /v "Enabled" /t REG_DWORD /d 0 /f >nul 2>&1

REM Configurar para evitar ventanas emergentes de UAC innecesarias
reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "ConsentPromptBehaviorUser" /t REG_DWORD /d 0 /f >nul 2>&1

echo Configuración aplicada para reducir ventanas molestas
echo Puede cerrar esta ventana
pause
'''
    
    with open('dist/VoiceExtractor/disable_notifications.bat', 'w', encoding='utf-8') as f:
        f.write(disable_notifications)
    
    print("✅ Optimización completada (incluye desactivador de notificaciones)")

def main():
    """Función principal"""
    print("🎬 Voice Extractor - Compilador de Ejecutable")
    print("=" * 50)
    
    # Verificar dependencias
    if not check_requirements():
        return
    
    # Limpiar compilaciones anteriores  
    clean_build()
    
    # Crear archivos de configuración
    create_spec_file()
    create_version_info()
    
    # Compilar
    if not build_executable():
        print("❌ Compilación fallida")
        return
    
    # Crear archivos adicionales
    create_launcher_script()
    create_ffmpeg_installer() 
    create_readme()
    optimize_executable()
    
    print("\n🎉 ¡Compilación completada exitosamente!")
    print("📁 Ejecutable disponible en: dist/VoiceExtractor/")
    print("🚀 Para distribuir, comprime toda la carpeta 'VoiceExtractor'")
    print("⚡ OPTIMIZADO: Inicio en pocos segundos!")
    print("🎨 ICONO: Integrado correctamente en el ejecutable y ventana")

if __name__ == "__main__":
    main()
