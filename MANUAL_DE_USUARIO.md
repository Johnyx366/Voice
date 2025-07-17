# 🎬 VoiceExtractor - Manual de Usuario Completo

## ✨ ¡Bienvenido a VoiceExtractor!

VoiceExtractor utiliza la avanzada tecnología de inteligencia artificial Whisper de OpenAI para extraer texto de videos y audios con precisión profesional.

## 🚀 Inicio Rápido

### Primera instalación:
1. **Descomprime** todos los archivos en una carpeta
2. **Ejecuta** `Ejecutar_VoiceExtractor.bat`
3. **Instala FFmpeg** cuando se solicite (automático)
4. **¡Listo!** Ya puedes usar la aplicación

### Uso diario:
- Ejecuta directamente `VoiceExtractor.exe`
- O usa `Ejecutar_VoiceExtractor.bat` para verificaciones automáticas

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
**Solución**: Ejecuta `Instalar_FFmpeg.bat` o `Ejecutar_VoiceExtractor.bat`

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

VoiceExtractor soporta más de 99 idiomas automáticamente:

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
- `VoiceExtractor.exe`: Aplicación principal
- `Ejecutar_VoiceExtractor.bat`: Launcher con verificaciones
- `Instalar_FFmpeg.bat`: Instalador de dependencias
- `MANUAL_DE_USUARIO.txt`: Este manual

### En Caso de Problemas:
1. Ejecuta `Ejecutar_VoiceExtractor.bat` en lugar del .exe
2. Verifica que FFmpeg esté instalado
3. Libera espacio en disco si es necesario
4. Reinicia la aplicación

---

## 🎉 ¡Gracias por usar VoiceExtractor!

**Versión**: 1.0.0  
**Motor IA**: OpenAI Whisper  
**Compatibilidad**: Windows 10/11  
**Privacidad**: 100% Offline después de configuración inicial  

💡 **Tip Final**: Para mejores resultados, usa audio/video de buena calidad y el modelo "Base" como punto de partida.

¡Disfruta extrayendo voz de tus archivos multimedia con inteligencia artificial!
