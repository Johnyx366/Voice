@echo off
echo 🔐 Creando certificado autofirmado para Voice Extractor...
echo.

REM Crear directorio para certificados
if not exist "certificates" mkdir certificates
cd certificates

REM Generar certificado autofirmado
echo 📋 Generando certificado autofirmado...
powershell -Command "& {
    $cert = New-SelfSignedCertificate -Subject 'CN=Voice Extractor Developer' -Type CodeSigning -KeyAlgorithm RSA -KeyLength 2048 -Provider 'Microsoft Enhanced RSA and AES Cryptographic Provider' -KeyExportPolicy Exportable -KeyUsage DigitalSignature -CertStoreLocation Cert:\CurrentUser\My -NotAfter (Get-Date).AddYears(3)
    $pwd = ConvertTo-SecureString -String 'VoiceExtractor2024!' -Force -AsPlainText
    $path = 'VoiceExtractor_Certificate.pfx'
    Export-PfxCertificate -Cert $cert -FilePath $path -Password $pwd
    Write-Host '✅ Certificado creado: VoiceExtractor_Certificate.pfx'
    Write-Host '🔑 Contraseña: VoiceExtractor2024!'
    Write-Host '📍 Ubicación:' (Get-Location).Path
}"

echo.
echo 🔒 Instalando certificado en el almacén de confianza...
powershell -Command "& {
    $cert = Get-ChildItem -Path 'VoiceExtractor_Certificate.pfx'
    $pwd = ConvertTo-SecureString -String 'VoiceExtractor2024!' -Force -AsPlainText
    Import-PfxCertificate -FilePath $cert.FullName -Password $pwd -CertStoreLocation Cert:\LocalMachine\TrustedPublisher
    Write-Host '✅ Certificado instalado en almacén de confianza'
}"

cd ..
echo.
echo ✅ Certificado autofirmado creado y configurado exitosamente!
echo 📁 Archivo: certificates\VoiceExtractor_Certificate.pfx
echo 🔑 Contraseña: VoiceExtractor2024!
echo.
pause
