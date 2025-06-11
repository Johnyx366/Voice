#!/usr/bin/env python3
"""
Script para firmar digitalmente el ejecutable de Voice Extractor
Requiere certificado de código válido para Windows
"""

import os
import subprocess
import sys
from pathlib import Path

def check_signtool():
    """Verifica si SignTool está disponible"""
    try:
        result = subprocess.run(['signtool'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def find_signtool():
    """Busca SignTool en ubicaciones comunes"""
    common_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe", 
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\x64\signtool.exe"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    return None

def sign_executable(exe_path, cert_path=None, cert_pass=None):
    """Firma el ejecutable con certificado digital"""
    
    signtool_path = find_signtool()
    if not signtool_path:
        print("❌ SignTool no encontrado")
        print("💡 Instala Windows SDK desde:")
        print("   https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/")
        return False
    
    print(f"🔧 Usando SignTool: {signtool_path}")
    
    if not os.path.exists(exe_path):
        print(f"❌ Ejecutable no encontrado: {exe_path}")
        return False
    
    # Comando de firma básico (sin certificado)
    cmd = [
        signtool_path,
        'sign',
        '/fd', 'SHA256',  # Algoritmo de hash
        '/t', 'http://timestamp.digicert.com',  # Servidor de timestamp
        '/d', 'Voice Extractor - Whisper AI',  # Descripción
        '/du', 'https://github.com/your-repo',  # URL (cambiar)
    ]
    
    # Si hay certificado, agregarlo
    if cert_path and os.path.exists(cert_path):
        cmd.extend(['/f', cert_path])
        if cert_pass:
            cmd.extend(['/p', cert_pass])
    else:
        print("⚠️  No se especificó certificado válido")
        print("💡 Para producción, necesitas un certificado de código válido")
        print("   Proveedores: DigiCert, Sectigo, GlobalSign, etc.")
        return False
    
    cmd.append(exe_path)
    
    try:
        print(f"✍️  Firmando: {exe_path}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable firmado exitosamente")
            return True
        else:
            print(f"❌ Error firmando ejecutable:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando SignTool: {e}")
        return False

def create_self_signed_cert():
    """Crea certificado auto-firmado para desarrollo (NO para producción)"""
    print("🔒 Creando certificado auto-firmado para desarrollo...")
    
    # Comando PowerShell para crear certificado auto-firmado
    ps_script = '''
$cert = New-SelfSignedCertificate -Subject "CN=Voice Extractor Dev" -Type CodeSigning -KeyUsage DigitalSignature -FriendlyName "Voice Extractor Development Certificate" -CertStoreLocation "Cert:\\CurrentUser\\My" -KeyExportPolicy Exportable -KeySpec Signature -KeyLength 2048 -KeyAlgorithm RSA -HashAlgorithm SHA256

$password = ConvertTo-SecureString -String "dev123456" -Force -AsPlainText
$path = "voice_extractor_dev_cert.pfx"
Export-PfxCertificate -Cert $cert -FilePath $path -Password $password

Write-Host "Certificado creado: $path"
Write-Host "Contraseña: dev123456"
'''
    
    try:
        result = subprocess.run(['powershell', '-Command', ps_script], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Certificado auto-firmado creado: voice_extractor_dev_cert.pfx")
            print("🔑 Contraseña: dev123456")
            print("⚠️  SOLO para desarrollo - Windows mostrará advertencia de seguridad")
            return "voice_extractor_dev_cert.pfx", "dev123456"
        else:
            print(f"❌ Error creando certificado: {result.stderr}")
            return None, None
            
    except Exception as e:
        print(f"❌ Error ejecutando PowerShell: {e}")
        return None, None

def main():
    """Función principal"""
    print("✍️  Voice Extractor - Firmador Digital")
    print("=" * 40)
    
    exe_path = "dist/VoiceExtractor/VoiceExtractor.exe"
    
    if not os.path.exists(exe_path):
        print(f"❌ Ejecutable no encontrado: {exe_path}")
        print("💡 Primero ejecuta build_exe.py para compilar")
        return
    
    # Verificar si ya hay certificado
    cert_path = "voice_extractor_cert.pfx"  # Certificado de producción
    dev_cert_path = "voice_extractor_dev_cert.pfx"  # Certificado de desarrollo
    
    if os.path.exists(cert_path):
        print(f"🔒 Usando certificado de producción: {cert_path}")
        cert_pass = input("🔑 Ingresa la contraseña del certificado: ")
        if sign_executable(exe_path, cert_path, cert_pass):
            print("🎉 ¡Ejecutable firmado para producción!")
        
    elif os.path.exists(dev_cert_path):
        print(f"🔒 Usando certificado de desarrollo: {dev_cert_path}")
        if sign_executable(exe_path, dev_cert_path, "dev123456"):
            print("🎉 ¡Ejecutable firmado para desarrollo!")
        
    else:
        print("🔒 No se encontró certificado")
        response = input("¿Crear certificado auto-firmado para desarrollo? (s/n): ")
        
        if response.lower() in ['s', 'si', 'y', 'yes']:
            cert_path, cert_pass = create_self_signed_cert()
            if cert_path:
                if sign_executable(exe_path, cert_path, cert_pass):
                    print("🎉 ¡Ejecutable firmado con certificado de desarrollo!")
        else:
            print("💡 Para obtener un certificado de producción:")
            print("   1. Compra certificado de código de un proveedor confiable")
            print("   2. Guárdalo como 'voice_extractor_cert.pfx'")
            print("   3. Ejecuta este script nuevamente")

if __name__ == "__main__":
    main()
