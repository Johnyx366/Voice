#!/usr/bin/env python3
"""
Script mejorado para firmar digitalmente el ejecutable de Voice Extractor
Usa certificado autofirmado creado automáticamente
"""

import os
import sys
import subprocess
from pathlib import Path

def find_signtool():
    """Busca signtool.exe en las ubicaciones comunes del Windows SDK"""
    common_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe",
        r"C:\Program Files (x86)\Microsoft SDKs\Windows\v7.1A\Bin\signtool.exe",
    ]
    
    # Buscar en todas las versiones disponibles
    kits_path = Path(r"C:\Program Files (x86)\Windows Kits\10\bin")
    if kits_path.exists():
        for version_dir in kits_path.iterdir():
            if version_dir.is_dir():
                signtool_path = version_dir / "x64" / "signtool.exe"
                if signtool_path.exists():
                    return str(signtool_path)
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def install_windows_sdk():
    """Instala Windows SDK automáticamente si no está disponible"""
    print("📦 Windows SDK no encontrado. Instalando automáticamente...")
    
    install_script = '''
    Write-Host "🔧 Descargando Windows SDK..."
    $url = "https://go.microsoft.com/fwlink/?linkid=2196127"
    $output = "$env:TEMP\\winsdksetup.exe"
    
    try {
        Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
        Write-Host "✅ Descarga completada"
        
        Write-Host "🔧 Instalando Windows SDK (herramientas de firma)..."
        Start-Process -FilePath $output -ArgumentList "/quiet", "/features", "OptionId.SigningTools" -Wait
        Write-Host "✅ Windows SDK instalado"
        
        Remove-Item $output -Force -ErrorAction SilentlyContinue
    } catch {
        Write-Host "❌ Error: $_"
        Write-Host "💡 Instala manualmente desde: https://developer.microsoft.com/windows/downloads/windows-sdk/"
        exit 1
    }
    '''
    
    try:
        subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-Command', install_script], 
                       check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando Windows SDK: {e}")
        return False

def sign_with_certificate():
    """Firma el ejecutable usando el certificado autofirmado"""
    exe_path = "dist/VoiceExtractor/VoiceExtractor.exe"
    cert_path = "certificates/VoiceExtractor_Certificate.pfx"
    cert_password = "VoiceExtractor2024!"
    
    # Verificar que el ejecutable existe
    if not os.path.exists(exe_path):
        print("❌ Ejecutable no encontrado. Ejecuta build_exe.py primero")
        return False
    
    # Verificar que el certificado existe
    if not os.path.exists(cert_path):
        print("❌ Certificado no encontrado. Ejecuta create_certificate.bat primero")
        return False
    
    # Buscar signtool
    signtool_path = find_signtool()
    if not signtool_path:
        print("🔍 SignTool no encontrado, intentando instalar Windows SDK...")
        if not install_windows_sdk():
            return False
        
        # Buscar de nuevo después de la instalación
        signtool_path = find_signtool()
        if not signtool_path:
            print("❌ No se pudo encontrar SignTool después de la instalación")
            return False
    
    print(f"🔧 Usando SignTool: {signtool_path}")
    
    # Comando para firmar
    cmd = [
        signtool_path,
        'sign',
        '/f', cert_path,                           # Archivo de certificado
        '/p', cert_password,                       # Contraseña del certificado
        '/fd', 'SHA256',                          # Algoritmo de hash
        '/tr', 'http://timestamp.digicert.com',   # Servidor de timestamp
        '/td', 'SHA256',                          # Algoritmo de timestamp
        '/d', 'Voice Extractor - Whisper AI',    # Descripción
        '/du', 'https://github.com/voice-extractor', # URL del proyecto
        exe_path
    ]
    
    try:
        print("✍️  Firmando ejecutable...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable firmado exitosamente!")
            print("🔒 El ejecutable ahora está firmado digitalmente")
            return True
        else:
            print(f"❌ Error firmando ejecutable:")
            print(result.stderr)
            # Intentar sin timestamp si falla
            return sign_without_timestamp(signtool_path, cert_path, cert_password, exe_path)
            
    except Exception as e:
        print(f"❌ Error ejecutando SignTool: {e}")
        return False

def sign_without_timestamp(signtool_path, cert_path, cert_password, exe_path):
    """Intenta firmar sin timestamp como respaldo"""
    print("🔄 Intentando firmar sin timestamp...")
    
    cmd = [
        signtool_path,
        'sign',
        '/f', cert_path,
        '/p', cert_password,
        '/fd', 'SHA256',
        '/d', 'Voice Extractor - Whisper AI',
        exe_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable firmado exitosamente (sin timestamp)!")
            return True
        else:
            print(f"❌ Error firmando sin timestamp:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error en firma sin timestamp: {e}")
        return False

def verify_signature():
    """Verifica que la firma sea válida"""
    exe_path = "dist/VoiceExtractor/VoiceExtractor.exe"
    
    signtool_path = find_signtool()
    if not signtool_path:
        print("⚠️  No se puede verificar firma: SignTool no disponible")
        return False
    
    cmd = [signtool_path, 'verify', '/pa', exe_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Firma verificada correctamente")
            return True
        else:
            print("⚠️  Advertencia en verificación de firma:")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Error verificando firma: {e}")
        return False

def main():
    """Función principal"""
    print("🔐 Voice Extractor - Firmado Digital")
    print("=" * 45)
    
    # Verificar prerrequisitos
    if not os.path.exists("certificates"):
        print("❌ Directorio de certificados no encontrado")
        print("💡 Ejecuta create_certificate.bat primero")
        return
    
    # Firmar ejecutable
    if sign_with_certificate():
        print("\n🎉 ¡Proceso de firmado completado exitosamente!")
        
        # Verificar firma
        print("\n🔍 Verificando firma...")
        verify_signature()
        
        print("\n📋 Resumen:")
        print("   ✅ Ejecutable firmado digitalmente")
        print("   🔒 Certificado autofirmado aplicado")
        print("   ⚠️  Windows puede mostrar advertencia de 'Editor desconocido'")
        print("   💡 Para producción, usa certificado de una CA confiable")
        
    else:
        print("\n❌ Error en el proceso de firmado")
        print("💡 Verifica que:")
        print("   - El ejecutable existe en dist/VoiceExtractor/")
        print("   - El certificado existe en certificates/")
        print("   - Windows SDK está instalado")

if __name__ == "__main__":
    main()
