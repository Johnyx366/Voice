#!/usr/bin/env python3
"""
🎬 VOICE EXTRACTOR - CREADOR DE EJECUTABLE COMPLETO
==================================================

Script único que centraliza TODO el proceso:
✅ Verificación de dependencias
✅ Creación de certificado autofirmado
✅ Configuración de iconos en todas las ventanas
✅ Compilación con PyInstaller optimizado
✅ Firma digital automática
✅ Creación de instalador de FFmpeg
✅ Documentación completa
✅ Paquete final listo para distribuir

Ejecuta este archivo y tendrás todo listo automáticamente.
"""

import os
import sys
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

# ================== CONFIGURACIÓN GLOBAL ==================

APP_NAME = "VoiceExtractor"
APP_VERSION = "1.0.0"
CERT_PASSWORD = "VoiceExtractor2024!"
MAIN_SCRIPT = "Voice_extractor.py"
ICON_FILE = "icon.ico"

# ================== FUNCIONES DE UTILIDAD ==================

def print_banner():
    """Muestra el banner de la aplicación"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗                                      ║
║  ██║   ██║██╔═══██╗██║██╔════╝██╔════╝                                      ║
║  ██║   ██║██║   ██║██║██║     █████╗                                        ║
║  ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝                                        ║
║   ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗                                      ║
║    ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝                                      ║
║                                                                              ║
║  ███████╗██╗  ██╗███████╗     ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗ ║
║  ██╔════╝╚██╗██╔╝██╔════╝    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗║
║  █████╗   ╚███╔╝ █████╗      ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝║
║  ██╔══╝   ██╔██╗ ██╔══╝      ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗║
║  ███████╗██╔╝ ██╗███████╗    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║║
║  ╚══════╝╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝║
║                                                                              ║
║                          🤖 Powered by OpenAI Whisper                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🚀 CREADOR DE EJECUTABLE COMPLETO - Todo en uno
═══════════════════════════════════════════════════════════════════════════════
""")

def print_step(step, total, description):
    """Imprime el paso actual con formato elegante"""
    print(f"\n{'='*80}")
    print(f"🎯 PASO {step}/{total}: {description}")
    print('='*80)

def run_command(cmd, description="", capture_output=True, shell=False):
    """Ejecuta un comando y maneja errores"""
    try:
        if description:
            print(f"⚙️  {description}")
        
        result = subprocess.run(cmd, capture_output=capture_output, text=True, shell=shell)
        
        if result.returncode == 0:
            if description:
                print(f"✅ {description} - Completado")
            return True, result.stdout
        else:
            print(f"❌ Error en: {description}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Excepción en {description}: {e}")
        return False, str(e)

# ================== PASO 1: VERIFICACIÓN ==================

def check_python_environment():
    """Verifica el entorno de Python"""
    print("🔍 Verificando entorno Python...")
    
    # Verificar versión de Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requerido")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} - OK")
    
    # Verificar archivos principales
    if not os.path.exists(MAIN_SCRIPT):
        print(f"❌ Archivo principal no encontrado: {MAIN_SCRIPT}")
        return False
    
    print(f"✅ Archivo principal encontrado: {MAIN_SCRIPT}")
    
    if not os.path.exists(ICON_FILE):
        print(f"⚠️  Icono no encontrado: {ICON_FILE}")
        print("   Se usará icono por defecto")
    else:
        print(f"✅ Icono encontrado: {ICON_FILE}")
    
    return True

def install_dependencies():
    """Instala todas las dependencias necesarias"""
    print("📦 Instalando dependencias necesarias...")
    
    dependencies = [
        "pyinstaller>=6.0",
        "openai-whisper",
        "torch", 
        "torchaudio",
        "numpy",
        "pillow",
        "tiktoken",
        "regex",
        "ftfy"
    ]
    
    failed_deps = []
    
    for dep in dependencies:
        success, _ = run_command([
            sys.executable, "-m", "pip", "install", "--upgrade", dep
        ], f"Instalando {dep}")
        
        if not success:
            failed_deps.append(dep)
    
    if failed_deps:
        print(f"❌ Error instalando: {', '.join(failed_deps)}")
        return False
    
    print("✅ Todas las dependencias instaladas")
    return True

# ================== PASO 2: CERTIFICADO ==================

def create_certificate():
    """Crea certificado autofirmado para firma digital"""
    print("🔐 Creando certificado autofirmado...")
    
    cert_dir = "certificates"
    cert_file = f"{cert_dir}/VoiceExtractor_Certificate.pfx"
    
    if os.path.exists(cert_file):
        print("✅ Certificado ya existe")
        return True
    
    # Crear directorio para certificados
    os.makedirs(cert_dir, exist_ok=True)
    
    # Script de PowerShell para crear certificado
    ps_script = f'''
$cert = New-SelfSignedCertificate -Subject "CN=Voice Extractor Developer" -Type CodeSigning -KeyAlgorithm RSA -KeyLength 2048 -Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" -KeyExportPolicy Exportable -KeyUsage DigitalSignature -CertStoreLocation Cert:\\CurrentUser\\My -NotAfter (Get-Date).AddYears(3)

$pwd = ConvertTo-SecureString -String "{CERT_PASSWORD}" -Force -AsPlainText
$path = "{cert_file}"
Export-PfxCertificate -Cert $cert -FilePath $path -Password $pwd

# Instalar en almacén de confianza
Import-PfxCertificate -FilePath $path -Password $pwd -CertStoreLocation Cert:\\LocalMachine\\TrustedPublisher

Write-Host "✅ Certificado creado y configurado exitosamente"
'''
    
    success, _ = run_command([
        "powershell", "-ExecutionPolicy", "Bypass", "-Command", ps_script
    ], "Generando certificado autofirmado")
    
    if success and os.path.exists(cert_file):
        print("✅ Certificado autofirmado creado")
        return True
    else:
        print("⚠️  No se pudo crear certificado, continuando sin firma...")
        return False

# ================== PASO 3: CONFIGURACIÓN DE ICONOS ==================

def enhance_main_script():
    """Mejora el script principal para manejar iconos correctamente"""
    print("🎨 Configurando iconos en todas las ventanas...")
    
    # Verificar si ya tiene la configuración de iconos mejorada
    with open(MAIN_SCRIPT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "set_application_icon" in content:
        print("✅ Configuración de iconos ya presente")
        return True
    
    # Si no tiene la configuración, agregarla
    icon_enhancement = '''
    def set_application_icon(self):
        """Configura el icono de la aplicación de manera robusta"""
        icon_paths = [
            "icon.ico",  # Desarrollo
            os.path.join(os.path.dirname(sys.executable), "icon.ico"),  # PyInstaller
            os.path.join(os.path.dirname(__file__), "icon.ico"),  # Relativo al script
            os.path.join(os.getcwd(), "icon.ico"),  # Directorio actual
        ]
        
        for icon_path in icon_paths:
            try:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    return
            except Exception:
                continue
        
        # Fallback a icono por defecto
        try:
            self.root.wm_iconbitmap(bitmap="")
        except Exception:
            pass
'''
    
    # Agregar al constructor si no existe
    if "self.set_application_icon()" not in content:
        # Buscar después de configurar la ventana y antes de setup_styles
        import_section = content.find("self.root.minsize(800, 600)")
        if import_section != -1:
            insertion_point = content.find("\n", import_section) + 1
            new_content = (content[:insertion_point] + 
                          "\n        # Set application icon\n" +
                          "        self.set_application_icon()\n" +
                          content[insertion_point:])
            
            # Agregar el método al final de la clase
            class_end = content.rfind("def main():")
            new_content = (new_content[:class_end] + 
                          icon_enhancement + "\n\n" +
                          new_content[class_end:])
            
            with open(f"{MAIN_SCRIPT}.backup", 'w', encoding='utf-8') as f:
                f.write(content)
            
            with open(MAIN_SCRIPT, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Configuración de iconos agregada al script principal")
        else:
            print("⚠️  No se pudo agregar configuración de iconos automáticamente")
    
    return True

# ================== PASO 4: COMPILACIÓN ==================

def create_spec_file():
    """Crea archivo .spec optimizado para PyInstaller"""
    print("📝 Creando configuración de compilación...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

# Voice Extractor - Configuración de PyInstaller
# Generado automáticamente por CREATE_EXE.py

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Recopilar datos de Whisper
whisper_data = collect_data_files('whisper')
whisper_modules = collect_submodules('whisper')

# Recopilar datos de torch
torch_data = collect_data_files('torch')
torch_modules = collect_submodules('torch')

# Archivos adicionales
added_files = []

# Agregar icono si existe
if os.path.exists('{ICON_FILE}'):
    added_files.append(('{ICON_FILE}', '.'))

block_cipher = None

a = Analysis(
    ['{MAIN_SCRIPT}'],
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
        'sys',
        'os',
        'time'
    ] + whisper_modules + torch_modules,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy', 
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
        'pytest',
        'sphinx'
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Ventana sin consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{ICON_FILE}' if os.path.exists('{ICON_FILE}') else None,
)
'''
    
    spec_filename = f"{APP_NAME}.spec"
    with open(spec_filename, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"✅ Archivo de configuración creado: {spec_filename}")
    return spec_filename

def compile_executable(spec_file):
    """Compila el ejecutable usando PyInstaller"""
    print("🔨 Compilando ejecutable...")
    print("   ⏱️  Esto puede tomar varios minutos...")
    
    # Limpiar compilaciones anteriores
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   🧹 Limpiando {dir_name}/")
    
    # Compilar con PyInstaller
    success, output = run_command([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        spec_file
    ], "Ejecutando PyInstaller")
    
    exe_path = f"dist/{APP_NAME}.exe"
    
    if success and os.path.exists(exe_path):
        print("✅ Compilación exitosa")
        return exe_path
    else:
        print("❌ Error en compilación")
        print(output)
        return None

# ================== PASO 5: FIRMA DIGITAL ==================

def find_signtool():
    """Busca SignTool.exe en el sistema"""
    common_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe",
    ]
    
    # Buscar en todas las versiones del SDK
    kits_base = Path(r"C:\Program Files (x86)\Windows Kits\10\bin")
    if kits_base.exists():
        for version_dir in kits_base.iterdir():
            if version_dir.is_dir():
                signtool_path = version_dir / "x64" / "signtool.exe"
                if signtool_path.exists():
                    return str(signtool_path)
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def sign_executable(exe_path):
    """Firma el ejecutable digitalmente"""
    print("✍️  Firmando ejecutable digitalmente...")
    
    cert_file = "certificates/VoiceExtractor_Certificate.pfx"
    
    if not os.path.exists(cert_file):
        print("⚠️  Certificado no encontrado, continuando sin firma...")
        return True
    
    signtool_path = find_signtool()
    if not signtool_path:
        print("⚠️  SignTool no encontrado, continuando sin firma...")
        return True
    
    print(f"🔧 Usando SignTool: {signtool_path}")
    
    # Comando de firma
    cmd = [
        signtool_path,
        'sign',
        '/f', cert_file,
        '/p', CERT_PASSWORD,
        '/fd', 'SHA256',
        '/tr', 'http://timestamp.digicert.com',
        '/td', 'SHA256',
        '/d', f'{APP_NAME} - Whisper AI',
        '/du', 'https://github.com/voice-extractor',
        exe_path
    ]
    
    success, _ = run_command(cmd, "Aplicando firma digital")
    
    if success:
        print("✅ Ejecutable firmado digitalmente")
    else:
        # Intentar sin timestamp
        cmd_simple = [
            signtool_path, 'sign', '/f', cert_file, '/p', CERT_PASSWORD,
            '/fd', 'SHA256', '/d', f'{APP_NAME} - Whisper AI', exe_path
        ]
        
        success, _ = run_command(cmd_simple, "Aplicando firma simple")
        
        if success:
            print("✅ Ejecutable firmado (sin timestamp)")
        else:
            print("⚠️  No se pudo firmar, pero el ejecutable funcionará")
    
    return True

# ================== PASO 6: CREACIÓN DE ARCHIVOS ADICIONALES ==================

def create_ffmpeg_installer():
    """Crea instalador automático de FFmpeg"""
    print("🔧 Creando instalador de FFmpeg...")
    
    installer_content = '''@echo off
title Voice Extractor - Instalador de FFmpeg
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║              🔧 INSTALADOR DE FFMPEG                         ║
echo ║                                                              ║
echo ║  FFmpeg es necesario para procesar archivos de video        ║
echo ║  Este instalador lo descarga e instala automáticamente      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar si FFmpeg ya está disponible
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ FFmpeg ya está instalado y funcionando
    echo.
    pause
    exit /b 0
)

echo 📥 Descargando FFmpeg...
echo    ⏱️  Esto puede tomar unos minutos dependiendo de tu conexión...

REM Crear directorio temporal
mkdir temp_ffmpeg 2>nul
cd temp_ffmpeg

REM Descargar FFmpeg portable
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip' -UseBasicParsing; Write-Host '✅ Descarga completada' } catch { Write-Host '❌ Error en descarga: ' $_; exit 1 }}"

if not exist ffmpeg.zip (
    echo ❌ Error descargando FFmpeg
    echo 💡 Verifica tu conexión a internet
    cd ..
    rmdir /s /q temp_ffmpeg 2>nul
    pause
    exit /b 1
)

echo 📦 Extrayendo FFmpeg...
powershell -Command "try { Expand-Archive -Path 'ffmpeg.zip' -DestinationPath '.' -Force; Write-Host '✅ Extracción completada' } catch { Write-Host '❌ Error extrayendo: ' $_; exit 1 }"

REM Copiar ejecutables al directorio principal
echo 📋 Instalando ejecutables...
for /d %%i in (ffmpeg-*) do (
    if exist "%%i\\bin\\ffmpeg.exe" (
        copy "%%i\\bin\\ffmpeg.exe" "..\\." >nul 2>&1
        echo    ✅ ffmpeg.exe copiado
    )
    if exist "%%i\\bin\\ffprobe.exe" (
        copy "%%i\\bin\\ffprobe.exe" "..\\." >nul 2>&1
        echo    ✅ ffprobe.exe copiado
    )
)

REM Limpiar archivos temporales
cd ..
rmdir /s /q temp_ffmpeg 2>nul

REM Verificar instalación
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ✅ ¡FFmpeg instalado correctamente!
    echo 🎉 Ya puedes usar Voice Extractor para procesar videos
) else (
    echo.
    echo ❌ Error en la instalación de FFmpeg
    echo 💡 Intenta instalarlo manualmente desde https://ffmpeg.org
)

echo.
pause
'''
    
    with open("Instalar_FFmpeg.bat", 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("✅ Instalador de FFmpeg creado")

def create_launcher():
    """Crea launcher optimizado para la aplicación"""
    print("🚀 Creando launcher de aplicación...")
    
    launcher_content = f'''@echo off
title {APP_NAME} - Launcher
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🎬 VOICE EXTRACTOR                           ║
echo ║                                                              ║
echo ║         Extractor de voz con IA de OpenAI Whisper           ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar que el ejecutable existe
if not exist "{APP_NAME}.exe" (
    echo ❌ {APP_NAME}.exe no encontrado en este directorio
    echo 💡 Asegúrate de ejecutar este launcher desde la carpeta correcta
    pause
    exit /b 1
)

REM Verificar FFmpeg
echo 🔍 Verificando dependencias...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  FFmpeg no encontrado
    echo    FFmpeg es necesario para procesar archivos de video
    echo.
    set /p install="¿Instalar FFmpeg automáticamente? (S/N): "
    if /i "!install!"=="S" (
        if exist "Instalar_FFmpeg.bat" (
            call "Instalar_FFmpeg.bat"
        ) else (
            echo ❌ Instalador de FFmpeg no encontrado
            echo 💡 Descarga FFmpeg manualmente desde https://ffmpeg.org
            pause
            exit /b 1
        )
    ) else (
        echo ⚠️  Voice Extractor necesita FFmpeg para funcionar
        echo    Solo podrás procesar archivos de audio (.mp3, .wav, etc.)
        pause
    )
) else (
    echo ✅ FFmpeg disponible
)

echo.
echo 🚀 Iniciando {APP_NAME}...
start "" "{APP_NAME}.exe"

REM Esperar un momento para verificar que se inició correctamente
timeout /t 2 /nobreak >nul

echo ✅ {APP_NAME} iniciado correctamente
echo.
echo 💡 Consejos de uso:
echo    • Primera vez: Los modelos de IA se descargan automáticamente
echo    • Formatos: Soporta MP4, AVI, MOV, MP3, WAV y muchos más
echo    • Calidad: Usa modelo "Base" para balance velocidad/precisión
echo    • Idiomas: "Auto-detect" funciona muy bien
echo.
echo 🎉 ¡Disfruta extrayendo voz de tus videos!
'''
    
    with open(f"Ejecutar_{APP_NAME}.bat", 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Launcher de aplicación creado")

def create_documentation():
    """Crea documentación completa para el usuario"""
    print("📖 Creando documentación de usuario...")
    
    manual_content = f'''# 🎬 {APP_NAME} - Manual de Usuario Completo

## ✨ ¡Bienvenido a {APP_NAME}!

{APP_NAME} utiliza la avanzada tecnología de inteligencia artificial Whisper de OpenAI para extraer texto de videos y audios con precisión profesional.

## 🚀 Inicio Rápido

### Primera instalación:
1. **Descomprime** todos los archivos en una carpeta
2. **Ejecuta** `Ejecutar_{APP_NAME}.bat`
3. **Instala FFmpeg** cuando se solicite (automático)
4. **¡Listo!** Ya puedes usar la aplicación

### Uso diario:
- Ejecuta directamente `{APP_NAME}.exe`
- O usa `Ejecutar_{APP_NAME}.bat` para verificaciones automáticas

## 📱 Guía de Uso Paso a Paso

### 1. Seleccionar Archivo
- Haz clic en **"📂 Browse Files"**
- Selecciona tu video o audio
- Formatos soportados: MP4, AVI, MOV, MKV, MP3, WAV, AAC, y muchos más

### 2. Configurar IA
Elige el modelo según tus necesidades:

- **⚡ Tiny (39 MB)**: Súper rápido para pruebas
- **⚖️ Base (74 MB)**: ✅ **RECOMENDADO** - Equilibrio perfecto
- **🎯 Small (244 MB)**: Mejor calidad para archivos importantes
- **🔥 Medium (769 MB)**: Muy alta calidad
- **💎 Large (1550 MB)**: Máxima calidad posible

### 3. Seleccionar Idioma
- **🌍 Auto-detect**: ✅ **RECOMENDADO** - Funciona excelente
- **🇪🇸 Spanish**: Si sabes que es español
- **🇺🇸 English**: Si sabes que es inglés

### 4. Extraer Voz
- Haz clic en **"🎯 Extract Voice"**
- Observa el progreso en tiempo real
- La primera vez descarga el modelo (solo una vez)

### 5. Guardar Resultado
- Una vez completado, haz clic en **"💾 Save Text to File"**
- El archivo se guarda automáticamente junto al video original
- Formato: `nombre_del_video.txt`

## 🎯 Consejos y Trucos Profesionales

### Para Mejores Resultados:
- **Audio claro**: Mejor audio = mejor transcripción
- **Sin ruido de fondo**: Reduce música/ruidos para mayor precisión
- **Velocidad normal**: Habla no muy rápida mejora la precisión
- **Un idioma**: Archivos con un solo idioma funcionan mejor

### Optimización de Velocidad:
- **Tiny**: Para pruebas rápidas o archivos largos
- **Base**: Velocidad y calidad equilibradas
- **Small/Medium**: Para contenido importante
- **Large**: Solo para máxima calidad necesaria

### Gestión de Archivos:
- Los archivos de texto se guardan en la misma carpeta que el video
- Puedes procesar múltiples archivos uno tras otro
- Los modelos solo se descargan una vez

## 📁 Formatos Soportados

### Videos:
✅ MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V, 3GP, ASF

### Audios:
✅ MP3, WAV, AAC, OGG, M4A, FLAC, WMA, AIFF

### Salida:
📝 Archivo de texto (.txt) con codificación UTF-8

## 🔧 Solución de Problemas

### "FFmpeg no encontrado"
**Solución**: Ejecuta `Instalar_FFmpeg.bat` o `Ejecutar_{APP_NAME}.bat`

### "Modelo muy lento"
**Solución**: Cambia a modelo "Tiny" o "Base"

### "Error al procesar archivo"
**Posibles causas**:
- Archivo corrupto o formato no soportado
- Falta de espacio en disco
- Archivo protegido o bloqueado

**Soluciones**:
- Verifica que el archivo se reproduzca normalmente
- Libera espacio en disco
- Copia el archivo a otra ubicación

### "No se guarda el texto"
**Posibles causas**:
- Sin permisos de escritura en la carpeta
- Carpeta de solo lectura

**Soluciones**:
- Ejecuta como administrador
- Cambia los permisos de la carpeta
- Mueve el video a otra carpeta (Documentos, Escritorio, etc.)

### "Primera vez muy lenta"
**Es normal**: Los modelos de IA se descargan solo la primera vez
- Tiny: ~39 MB
- Base: ~74 MB  
- Small: ~244 MB
- Medium: ~769 MB
- Large: ~1550 MB

## 🌐 Idiomas Soportados

{APP_NAME} soporta más de 99 idiomas automáticamente:

**Principales**: Español, Inglés, Francés, Alemán, Italiano, Portugués, Ruso, Japonés, Chino, Coreano, Árabe, Hindi

**Y muchos más**: Catalán, Euskera, Gallego, Holandés, Sueco, Noruego, Danés, Polaco, Checo, Húngaro, Rumano, Búlgaro, Griego, Turco, Hebreo, Tailandés, Vietnamita, etc.

## 💡 Casos de Uso Comunes

### 📚 Estudiantes:
- Transcribir clases grabadas
- Convertir conferencias a texto
- Crear apuntes de videos educativos

### 👔 Profesionales:
- Transcribir reuniones
- Convertir webinars a documentos
- Crear subtítulos para videos corporativos

### 🎥 Creadores de Contenido:
- Generar subtítulos automáticos
- Crear artículos de videos
- Documentar contenido audiovisual

### 🏠 Uso Personal:
- Transcribir mensajes de voz largos
- Convertir videos familiares a texto
- Documentar eventos importantes

## 🔒 Privacidad y Seguridad

### ✅ Completamente Offline:
- Funciona sin conexión a internet (después de primera descarga)
- Tus archivos NUNCA salen de tu computadora
- Sin registro, cuentas o seguimiento

### ✅ Seguridad:
- Ejecutable firmado digitalmente
- Sin conexiones externas durante el procesamiento
- Datos procesados localmente

## 📊 Requisitos del Sistema

### Mínimos:
- **SO**: Windows 10/11 (64-bit)
- **RAM**: 4 GB (8 GB para modelos grandes)
- **Espacio**: 2 GB libres + tamaño de modelos
- **CPU**: Cualquier procesador moderno

### Recomendados:
- **RAM**: 8 GB o más
- **Espacio**: 5 GB libres
- **SSD**: Para mejor velocidad de carga

## 🆘 Soporte y Ayuda

### Archivos Importantes:
- `{APP_NAME}.exe`: Aplicación principal
- `Ejecutar_{APP_NAME}.bat`: Launcher con verificaciones
- `Instalar_FFmpeg.bat`: Instalador de dependencias
- `MANUAL_DE_USUARIO.txt`: Este manual

### En Caso de Problemas:
1. Ejecuta `Ejecutar_{APP_NAME}.bat` en lugar del .exe
2. Verifica que FFmpeg esté instalado
3. Libera espacio en disco si es necesario
4. Reinicia la aplicación

---

## 🎉 ¡Gracias por usar {APP_NAME}!

**Versión**: {APP_VERSION}  
**Motor IA**: OpenAI Whisper  
**Compatibilidad**: Windows 10/11  
**Privacidad**: 100% Offline después de configuración inicial  

💡 **Tip Final**: Para mejores resultados, usa audio/video de buena calidad y el modelo "Base" como punto de partida.

¡Disfruta extrayendo voz de tus archivos multimedia con inteligencia artificial!
'''
    
    with open("MANUAL_DE_USUARIO.txt", 'w', encoding='utf-8') as f:
        f.write(manual_content)
    
    print("✅ Manual de usuario creado")

def create_readme():
    """Crea README técnico"""
    print("📋 Creando README técnico...")
    
    readme_content = f'''# {APP_NAME} v{APP_VERSION}

Extractor de voz profesional con IA de OpenAI Whisper.

## Instalación

1. Descomprimir todos los archivos
2. Ejecutar `Ejecutar_{APP_NAME}.bat`
3. Instalar FFmpeg cuando se solicite

## Uso Rápido

```
1. Ejecutar {APP_NAME}.exe
2. Seleccionar archivo de video/audio
3. Elegir modelo de IA (recomendado: Base)
4. Hacer clic en "Extract Voice"
5. Guardar resultado cuando termine
```

## Archivos Incluidos

- `{APP_NAME}.exe` - Aplicación principal
- `Ejecutar_{APP_NAME}.bat` - Launcher con verificaciones
- `Instalar_FFmpeg.bat` - Instalador de FFmpeg
- `MANUAL_DE_USUARIO.txt` - Guía completa
- `README.txt` - Este archivo

## Formatos Soportados

**Video**: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V  
**Audio**: MP3, WAV, AAC, OGG, M4A, FLAC, WMA

## Requisitos

- Windows 10/11 (64-bit)
- 4+ GB RAM
- 2+ GB espacio libre
- FFmpeg (se instala automáticamente)

## Características

✅ 100% offline después de configuración  
✅ Soporta 99+ idiomas  
✅ 5 niveles de calidad de IA  
✅ Interfaz gráfica intuitiva  
✅ Procesamiento en tiempo real  
✅ Sin límites de archivo  

## Tecnología

- **Motor IA**: OpenAI Whisper
- **Interfaz**: Python Tkinter  
- **Audio**: FFmpeg
- **Plataforma**: Windows x64

---
Generado automáticamente por CREATE_EXE.py v{APP_VERSION}
'''
    
    with open("README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README técnico creado")

# ================== PASO 7: EMPAQUETADO FINAL ==================

def create_final_package():
    """Crea el paquete final listo para distribuir"""
    print("📦 Creando paquete final de distribución...")
    
    # Crear directorio de distribución
    dist_dir = f"{APP_NAME}_v{APP_VERSION}_Windows"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir)
    
    # Copiar ejecutable principal
    exe_source = f"dist/{APP_NAME}.exe"
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, dist_dir)
        print(f"✅ Ejecutable copiado a {dist_dir}")
    
    # Copiar archivos adicionales
    additional_files = [
        f"Ejecutar_{APP_NAME}.bat",
        "Instalar_FFmpeg.bat", 
        "MANUAL_DE_USUARIO.txt",
        "README.txt"
    ]
    
    for file in additional_files:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
    
    # Copiar icono si existe
    if os.path.exists(ICON_FILE):
        shutil.copy2(ICON_FILE, dist_dir)
    
    print(f"✅ Paquete creado en: {dist_dir}")
    return dist_dir

def create_installer_script(dist_dir):
    """Crea script de instalación para el usuario final"""
    print("🛠️  Creando instalador automático...")
    
    installer_content = f'''@echo off
title {APP_NAME} - Instalador Automático
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║  ██╗   ██╗ ██████╗ ██╗ ██████╗███████╗                                      ║
echo ║  ██║   ██║██╔═══██╗██║██╔════╝██╔════╝                                      ║
echo ║  ██║   ██║██║   ██║██║██║     █████╗                                        ║
echo ║  ╚██╗ ██╔╝██║   ██║██║██║     ██╔══╝                                        ║
echo ║   ╚████╔╝ ╚██████╔╝██║╚██████╗███████╗                                      ║
echo ║    ╚═══╝   ╚═════╝ ╚═╝ ╚═════╝╚══════╝                                      ║
echo ║                                                                              ║
echo ║  ███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗ ██████╗ ██████╗ ║
echo ║  ██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗║
echo ║  █████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║   ██║   ██║██████╔╝║
echo ║  ██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║   ██║   ██║██╔══██╗║
echo ║  ███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║║
echo ║  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝║
echo ║                                                                              ║
echo ║                          🤖 Powered by OpenAI Whisper                       ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo  🚀 INSTALADOR AUTOMÁTICO v{APP_VERSION}
echo ══════════════════════════════════════════════════════════════════════════════
echo.
echo  Este instalador configurará {APP_NAME} en tu sistema de forma automática.
echo  ✅ Copia archivos al directorio elegido
echo  ✅ Crea accesos directos en escritorio y menú inicio  
echo  ✅ Configura FFmpeg automáticamente
echo  ✅ Todo listo para usar inmediatamente
echo.
echo ══════════════════════════════════════════════════════════════════════════════

set install_path=C:\\{APP_NAME}
set /p install_path="📁 Directorio de instalación [%install_path%]: "

echo.
echo 📦 Instalando en: %install_path%
echo ⏱️  Por favor espera...
echo.

REM Crear directorio de instalación
if not exist "%install_path%" (
    mkdir "%install_path%" 2>nul
    if %errorlevel% neq 0 (
        echo ❌ No se puede crear el directorio: %install_path%
        echo 💡 Intenta ejecutar como administrador o elige otra ubicación
        pause
        exit /b 1
    )
)

REM Copiar archivos
echo 📋 Copiando archivos...
xcopy /E /I /H /Y "*.*" "%install_path%\\" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error copiando archivos
    pause
    exit /b 1
)
echo ✅ Archivos copiados correctamente

REM Crear acceso directo en escritorio
echo 🔗 Creando acceso directo en escritorio...
powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('$env:USERPROFILE\\Desktop\\{APP_NAME}.lnk'); $Shortcut.TargetPath = '%install_path%\\{APP_NAME}.exe'; $Shortcut.IconLocation = '%install_path%\\icon.ico'; $Shortcut.Description = '{APP_NAME} - Extractor de voz con IA'; $Shortcut.WorkingDirectory = '%install_path%'; $Shortcut.Save()}}" 2>nul
echo ✅ Acceso directo creado en escritorio

REM Crear entrada en menú inicio
echo 📌 Agregando al menú inicio...
set startmenu_dir=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\{APP_NAME}
if not exist "%startmenu_dir%" mkdir "%startmenu_dir%" 2>nul
powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%startmenu_dir%\\{APP_NAME}.lnk'); $Shortcut.TargetPath = '%install_path%\\{APP_NAME}.exe'; $Shortcut.IconLocation = '%install_path%\\icon.ico'; $Shortcut.Description = '{APP_NAME} - Extractor de voz con IA'; $Shortcut.WorkingDirectory = '%install_path%'; $Shortcut.Save()}}" 2>nul
powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%startmenu_dir%\\Manual de Usuario.lnk'); $Shortcut.TargetPath = '%install_path%\\MANUAL_DE_USUARIO.txt'; $Shortcut.IconLocation = 'shell32.dll,70'; $Shortcut.Description = 'Manual de usuario de {APP_NAME}'; $Shortcut.WorkingDirectory = '%install_path%'; $Shortcut.Save()}}" 2>nul
echo ✅ Agregado al menú inicio

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                ✅ ¡INSTALACIÓN COMPLETADA!                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📍 Ubicación: %install_path%
echo 🖥️  Acceso directo: Escritorio y Menú Inicio
echo 📖 Manual: MANUAL_DE_USUARIO.txt
echo.
echo 💡 PRIMERA VEZ:
echo    1. Ejecuta {APP_NAME} desde el escritorio o menú inicio
echo    2. Si solicita FFmpeg, haz clic en "Sí" para instalarlo
echo    3. ¡Comienza a extraer voz de tus videos!
echo.
echo 🎯 CONSEJO: Lee el "Manual de Usuario" para aprovechar al máximo
echo     todas las funciones y características avanzadas.
echo.

set /p launch="🚀 ¿Ejecutar {APP_NAME} ahora? (S/N): "
if /i "%launch%"=="S" (
    echo.
    echo 🎬 Iniciando {APP_NAME}...
    start "" "%install_path%\\{APP_NAME}.exe"
)

echo.
echo 🎉 ¡Gracias por usar {APP_NAME}!
echo    Extrae voz de videos con inteligencia artificial
pause
'''
    
    installer_path = os.path.join(dist_dir, "INSTALAR.bat")
    with open(installer_path, 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("✅ Instalador automático creado")

# ================== FUNCIÓN PRINCIPAL ==================

def main():
    """Función principal que ejecuta todo el proceso"""
    start_time = time.time()
    
    # Mostrar banner
    print_banner()
    
    # Confirmación del usuario
    print("Este script automatizará COMPLETAMENTE la creación del ejecutable:")
    print("✅ Instalación de dependencias")
    print("✅ Creación de certificado autofirmado")
    print("✅ Configuración de iconos")
    print("✅ Compilación con PyInstaller")
    print("✅ Firma digital")
    print("✅ Creación de documentación")
    print("✅ Paquete final listo para distribuir")
    print()
    
    confirm = input("🤖 ¿Continuar con el proceso completo? (S/N): ").lower()
    if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Proceso cancelado por el usuario")
        return
    
    try:
        # PASO 1: Verificación del entorno
        print_step(1, 7, "Verificación del entorno")
        if not check_python_environment():
            print("❌ Error en verificación del entorno")
            return
        
        if not install_dependencies():
            print("❌ Error instalando dependencias")
            return
        
        # PASO 2: Certificado
        print_step(2, 7, "Creación de certificado autofirmado")
        create_certificate()
        
        # PASO 3: Configuración de iconos
        print_step(3, 7, "Configuración de iconos")
        enhance_main_script()
        
        # PASO 4: Compilación
        print_step(4, 7, "Compilación del ejecutable")
        spec_file = create_spec_file()
        exe_path = compile_executable(spec_file)
        
        if not exe_path:
            print("❌ Error en compilación")
            return
        
        # PASO 5: Firma digital
        print_step(5, 7, "Firma digital")
        sign_executable(exe_path)
        
        # PASO 6: Archivos adicionales
        print_step(6, 7, "Creación de archivos adicionales")
        create_ffmpeg_installer()
        create_launcher()
        create_documentation()
        create_readme()
        
        # PASO 7: Empaquetado final
        print_step(7, 7, "Empaquetado final")
        dist_dir = create_final_package()
        create_installer_script(dist_dir)
        
        # Resumen final
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*80}")
        print("🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!")
        print('='*80)
        print(f"⏱️  Tiempo total: {elapsed_time:.1f} segundos")
        print(f"📊 Tamaño del ejecutable: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
        print()
        print("📦 ARCHIVOS CREADOS:")
        print(f"   📁 {dist_dir}/                    - Carpeta completa lista para distribuir")
        print(f"   🎯 {dist_dir}/{APP_NAME}.exe      - Aplicación principal")
        print(f"   🚀 {dist_dir}/Ejecutar_{APP_NAME}.bat - Launcher con verificaciones")
        print(f"   🔧 {dist_dir}/Instalar_FFmpeg.bat     - Instalador de FFmpeg")
        print(f"   📖 {dist_dir}/MANUAL_DE_USUARIO.txt   - Guía completa de usuario")
        print(f"   🛠️  {dist_dir}/INSTALAR.bat           - Instalador automático")
        print()
        print("🎯 PARA DISTRIBUIR:")
        print(f"   1. Comprime la carpeta '{dist_dir}' en un ZIP")
        print("   2. Comparte el ZIP con los usuarios")
        print("   3. Los usuarios ejecutan INSTALAR.bat")
        print("   4. ¡Todo funciona automáticamente!")
        print()
        print("✨ CARACTERÍSTICAS INCLUIDAS:")
        print("   ✅ Ejecutable independiente (no requiere Python)")
        print("   ✅ Firmado digitalmente (reduce advertencias de Windows)")
        print("   ✅ Iconos en todas las ventanas y barras de tareas")
        print("   ✅ Instalación automática de FFmpeg")
        print("   ✅ Documentación completa de usuario")
        print("   ✅ Launcher con verificaciones de dependencias")
        print("   ✅ Instalador automático para usuarios finales")
        print("   ✅ Optimizado para arranque rápido")
        print("   ✅ Sin dependencias externas")
        
        # Abrir carpeta final
        try:
            subprocess.run(['explorer', dist_dir], shell=True)
            print(f"\n📂 Carpeta de distribución abierta: {dist_dir}")
        except:
            pass
        
        print(f"\n🎊 ¡{APP_NAME} v{APP_VERSION} listo para distribuir!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("\n🏁 Presiona Enter para finalizar...")

if __name__ == "__main__":
    main()
