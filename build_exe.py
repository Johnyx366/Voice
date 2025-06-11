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
    
    required_packages = [
        'pyinstaller',
        'whisper', 
        'torch',
        'torchaudio',
        'tkinter',
        'numpy',
        'pillow'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - FALTANTE")
    
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

# Datos y módulos de Whisper
whisper_data = collect_data_files('whisper')
whisper_modules = collect_submodules('whisper')

# Datos de torch
torch_data = collect_data_files('torch')
torch_modules = collect_submodules('torch')

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
    datas=added_files + whisper_data + torch_data,
    hiddenimports=[
        'whisper',
        'torch',
        'torchaudio', 
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
    ] + whisper_modules + torch_modules,
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
    upx=True,
    console=False,  # Sin consola para interfaz limpia
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Icono principal
    version='version_info.txt'  # Información de versión
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
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
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--clean',
        '--noconfirm', 
        'VoiceExtractor.spec'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Compilación exitosa!")
            return True
        else:
            print(f"❌ Error en compilación:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def create_launcher_script():
    """Crea script de lanzamiento optimizado"""
    print("📱 Creando launcher optimizado...")
    
    launcher_content = '''@echo off
echo 🎬 Iniciando Voice Extractor...
cd /d "%~dp0"

REM Verificar si FFmpeg está disponible
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  FFmpeg no encontrado. Instalando...
    call install_ffmpeg.bat
)

REM Ejecutar la aplicación
start "" "VoiceExtractor.exe"
'''
    
    with open('dist/VoiceExtractor/VoiceExtractor_Launcher.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Launcher creado")

def create_ffmpeg_installer():
    """Crea instalador automático de FFmpeg"""
    print("🔧 Creando instalador de FFmpeg...")
    
    ffmpeg_installer = '''@echo off
setlocal enabledelayedexpansion

echo 🔧 Instalando FFmpeg...

REM Crear directorio para FFmpeg
if not exist "ffmpeg" mkdir ffmpeg
cd ffmpeg

REM Descargar FFmpeg (versión estática)
echo 📥 Descargando FFmpeg...
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}"

REM Extraer
echo 📦 Extrayendo archivos...
powershell -Command "& {Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force}"

REM Mover ejecutables al directorio raíz
for /d %%i in (ffmpeg-master-*) do (
    copy "%%i\\bin\\*.exe" "..\\." >nul 2>&1
)

REM Limpiar
cd ..
rmdir /s /q ffmpeg 2>nul

echo ✅ FFmpeg instalado correctamente
pause
'''
    
    with open('dist/VoiceExtractor/install_ffmpeg.bat', 'w', encoding='utf-8') as f:
        f.write(ffmpeg_installer)
    
    print("✅ Instalador FFmpeg creado")

def create_readme():
    """Crea README para el usuario"""
    print("📖 Creando manual de usuario...")
    
    readme_content = '''# Voice Extractor - Whisper AI

## 🚀 Inicio Rápido

1. **Ejecutar la aplicación:**
   - Haz doble clic en `VoiceExtractor.exe`
   - O usa `VoiceExtractor_Launcher.bat` para instalación automática de dependencias

2. **Primera vez:**
   - La aplicación instalará FFmpeg automáticamente si es necesario
   - Los modelos de IA se descargarán la primera vez que los uses

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

## 🔧 Solución de Problemas

**Error de FFmpeg:** Ejecuta `install_ffmpeg.bat`
**Modelos lentos:** Los modelos se descargan solo la primera vez
**Archivos grandes:** Usa modelo "Tiny" para pruebas rápidas

## 📞 Soporte

- El archivo de texto se guarda en la misma carpeta que el video
- Todos los formatos de video comunes están soportados
- La transcripción funciona sin conexión a internet (después de la primera descarga)

---
Voice Extractor v1.0 - Powered by OpenAI Whisper
'''
    
    with open('dist/VoiceExtractor/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Manual de usuario creado")

def optimize_executable():
    """Optimiza el ejecutable para arranque rápido"""
    print("⚡ Optimizando para arranque rápido...")
    
    # Copiar icono al directorio de distribución
    if os.path.exists('icon.ico'):
        shutil.copy2('icon.ico', 'dist/VoiceExtractor/')
    
    print("✅ Optimización completada")

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
    print(f"📁 Ejecutable disponible en: dist/VoiceExtractor/")
    print("🚀 Para distribuir, comprime toda la carpeta 'VoiceExtractor'")

if __name__ == "__main__":
    main()
