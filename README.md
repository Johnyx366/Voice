# 🎬 Voice Extractor - Whisper AI

**Extractor de voz y texto a partir de videos y audios usando inteligencia artificial**

## 📋 Descripción

Voice Extractor es una aplicación de escritorio que utiliza la tecnología Whisper de OpenAI para extraer y transcribir el audio de archivos de video y audio a texto de manera precisa y eficiente.

## ✨ Características

- 🤖 **IA Avanzada**: Utiliza OpenAI Whisper para transcripción precisa
- 🎥 **Múltiples Formatos**: Soporta MP4, AVI, MOV, MKV, MP3, WAV y más
- 🌍 **Multi-idioma**: Detección automática o selección manual de idioma
- 🎯 **5 Niveles de Calidad**: Desde rápido hasta máxima precisión
- 📱 **Interfaz Moderna**: UI intuitiva con tema oscuro
- ⚡ **Sin Internet**: Funciona completamente offline (tras descarga inicial)
- 📁 **Fácil Instalación**: Todo incluido con instalador automático

## 🚀 Instalación Paso a Paso para Windows

### 📋 Requisitos Previos

1. **Python 3.8+** instalado desde [python.org](https://python.org)

   - ✅ Durante la instalación marca "Add Python to PATH"
   - ✅ Verificar: Abre `cmd` y ejecuta `python --version`

2. **Git** (opcional) para clonar el repositorio
   - O simplemente descarga el ZIP desde GitHub

### ⚡ Instalación Automática (Recomendado)

```bash
# 1. Descarga o clona el proyecto
git clone https://github.com/tu-usuario/voice-extractor.git
cd voice-extractor

# 2. Ejecuta el instalador automático
install_and_build.bat
```

**¡Eso es todo!** El script automático:

- ✅ Crea el entorno virtual
- ✅ Instala todas las dependencias
- ✅ Configura FFmpeg
- ✅ Compila el ejecutable
- ✅ Crea launchers optimizados

### 🔧 Instalación Manual Detallada

Si prefieres control total sobre el proceso:

#### Paso 1: Configurar Entorno Virtual

```bash
# Navegar al directorio del proyecto
cd ruta\donde\descargaste\voice-extractor

# Crear entorno virtual
python -m venv voice_env

# Activar entorno virtual (IMPORTANTE)
voice_env\Scripts\activate

# Verificar que está activo (debería mostrar (voice_env) al inicio)
```

#### Paso 2: Instalar Dependencias Python

```bash
# Actualizar pip primero
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalación de paquetes clave
pip list | findstr "openai-whisper torch"
```

#### Paso 3: Configurar FFmpeg

```bash
# Opción A: Automático (Recomendado)
install_ffmpeg.bat

# Opción B: Manual
# 1. Descarga FFmpeg desde https://ffmpeg.org/download.html
# 2. Extrae a una carpeta (ej: C:\ffmpeg)
# 3. Agrega C:\ffmpeg\bin al PATH del sistema
```

#### Paso 4: Probar la Aplicación

```bash
# Ejecutar directamente
python Voice_extractor.py

# Si funciona correctamente, compilar ejecutable
python build_exe.py
```

## 📁 Estructura del Proyecto

```
Voice/
├── 🐍 Voice_extractor.py          # Aplicación principal
├── 🔨 build_exe.py               # Script de compilación
├── 📦 requirements.txt           # Dependencias Python
├── 🛠️ install_and_build.bat      # Instalador automático completo
├── 🎥 install_ffmpeg.bat         # Instalador específico de FFmpeg
├── 🚀 start_voice_extractor.bat  # Launcher básico
├── 🎨 icon.ico                   # Icono de la aplicación
├── 🎨 icon.png                   # Icono alternativo
├── 📖 README.md                  # Esta guía
├── 📚 MANUAL_DE_USUARIO.md       # Manual detallado para usuarios
├── voice_env/                    # Entorno virtual (se crea automáticamente)
├── dist/                         # Ejecutable compilado (tras build)
└── build/                        # Archivos temporales de compilación
```

## 🎯 Guía de Uso

### Para Desarrolladores:

```bash
# Activar entorno virtual
voice_env\Scripts\activate

# Ejecutar desde código
python Voice_extractor.py

# Compilar ejecutable
python build_exe.py
```

### Para Usuarios Finales:

```bash
# Usar el ejecutable compilado
dist\VoiceExtractor\VoiceExtractor.exe

# O usar launcher silencioso
dist\VoiceExtractor\VoiceExtractor_Silent.vbs
```

## 💻 Comandos Útiles para Desarrollo

### Gestión del Entorno Virtual:

```bash
# Crear nuevo entorno
python -m venv voice_env

# Activar entorno (Windows)
voice_env\Scripts\activate

# Desactivar entorno
deactivate

# Ver paquetes instalados
pip list

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### Debugging y Desarrollo:

```bash
# Ejecutar con logs detallados
python Voice_extractor.py --verbose

# Limpiar archivos de compilación
rmdir /s build dist

# Reinstalar dependencias limpias
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 🤖 Modelos de IA Disponibles

| Modelo | Tamaño  | Velocidad  | Precisión  | Recomendado para |
| ------ | ------- | ---------- | ---------- | ---------------- |
| Tiny   | 39 MB   | ⚡⚡⚡⚡⚡ | ⭐⭐       | Pruebas rápidas  |
| Base   | 74 MB   | ⚡⚡⚡⚡   | ⭐⭐⭐     | Uso general      |
| Small  | 244 MB  | ⚡⚡⚡     | ⭐⭐⭐⭐   | Calidad buena    |
| Medium | 769 MB  | ⚡⚡       | ⭐⭐⭐⭐⭐ | Alta precisión   |
| Large  | 1550 MB | ⚡         | ⭐⭐⭐⭐⭐ | Máxima calidad   |

## 📋 Requisitos del Sistema

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 o superior
- **RAM**: 4GB mínimo (8GB recomendado para modelos grandes)
- **Espacio**: 2-5GB para modelos y dependencias
- **GPU**: Opcional (CUDA para aceleración)

## 🔧 Compilación a Ejecutable

El proyecto incluye un sistema completo de compilación:

```bash
# Compilar ejecutable standalone
python build_exe.py

# El ejecutable se genera en: dist/VoiceExtractor/
```

## 🌍 Idiomas Soportados

- **Auto-detección** (recomendado)
- Español, Inglés, Francés, Alemán, Italiano
- Portugués, Ruso, Japonés, Chino, Árabe
- Y muchos más...

## ⚡ Optimizaciones

- **Arranque rápido**: Optimizado para iniciar en segundos
- **Uso eficiente de memoria**: Procesamiento por chunks
- **Cache inteligente**: Los modelos se descargan solo una vez
- **Interfaz responsiva**: No se congela durante el procesamiento

## 🔒 Privacidad

- **100% Local**: Todo el procesamiento es offline
- **Sin envío de datos**: Tus archivos no salen de tu computadora
- **Sin telemetría**: No recopilamos información de uso

## � Solución de Problemas Comunes

### ❌ Error: "Python no encontrado"

```bash
# Verificar instalación
python --version

# Si no funciona, reinstalar Python desde python.org
# ✅ IMPORTANTE: Marcar "Add Python to PATH" durante instalación
```

### ❌ Error: "pip no encontrado"

```bash
# Verificar pip
pip --version

# Si falla, reparar instalación
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### ❌ Error: "No se puede crear entorno virtual"

```bash
# Instalar venv si no está disponible
python -m pip install virtualenv

# Crear con virtualenv alternativo
virtualenv voice_env
```

### ❌ Error: "FFmpeg no encontrado"

```bash
# Ejecutar instalador automático
install_ffmpeg.bat

# Verificar instalación
ffmpeg -version

# Instalación manual si falla:
# 1. Descargar desde https://ffmpeg.org/download.html#build-windows
# 2. Extraer a C:\ffmpeg
# 3. Agregar C:\ffmpeg\bin al PATH del sistema
```

### ❌ Error: "Módulo whisper no encontrado"

```bash
# Activar entorno virtual primero
voice_env\Scripts\activate

# Reinstalar whisper
pip uninstall openai-whisper
pip install openai-whisper

# Verificar instalación
python -c "import whisper; print('Whisper OK')"
```

### ❌ Error: "DLL load failed" o "python311.dll"

```bash
# Reinstalar Visual C++ Redistributable
# Descargar desde: https://aka.ms/vs/17/release/vc_redist.x64.exe

# O reinstalar Python completamente
# Asegurar versión 64-bit desde python.org
```

### ❌ Error: "Memoria insuficiente"

```bash
# Usar modelo más pequeño
# tiny (39MB) o base (74MB) en lugar de large (1550MB)

# Cerrar aplicaciones pesadas
# Chrome, juegos, etc.

# Verificar RAM disponible
wmic OS get TotalVisibleMemorySize,FreePhysicalMemory /value
```

### ❌ Error de permisos o archivos bloqueados

```bash
# Ejecutar como administrador
# Click derecho en cmd -> "Ejecutar como administrador"

# O mover proyecto a carpeta sin restricciones
# Documentos, Escritorio, etc.
```

## � Distribución y Empaquetado

### Crear Ejecutable para Distribución:

```bash
# Compilar ejecutable optimizado
python build_exe.py

# El ejecutable estará en: dist/VoiceExtractor/
# Archivos incluidos:
# - VoiceExtractor.exe (aplicación principal)
# - VoiceExtractor_Silent.vbs (launcher silencioso)
# - VoiceExtractor_Launcher.bat (launcher con verificaciones)
# - install_ffmpeg.bat (instalador FFmpeg)
# - README.txt (manual de usuario)
# - icon.ico (icono de la aplicación)
```

### Comprimir para Distribución:

```bash
# Crear ZIP para distribución
# Incluye toda la carpeta dist/VoiceExtractor/
# Tamaño aproximado: 300-400 MB (incluye modelos IA básicos)
```

## 🔒 Privacidad y Seguridad

- **100% Local**: Todo el procesamiento es offline después de la descarga inicial
- **Sin envío de datos**: Tus archivos NUNCA salen de tu computadora
- **Sin telemetría**: No recopilamos información de uso
- **Código abierto**: Puedes auditar todo el código fuente
- **Sin cuentas**: No requiere registro ni login

## 📊 Rendimiento y Optimizaciones

### Tiempos de Procesamiento Aproximados (archivo de 10 minutos):

- **Tiny**: 1-2 minutos
- **Base**: 3-5 minutos
- **Small**: 8-12 minutos
- **Medium**: 15-25 minutos
- **Large**: 30-45 minutos

### Consumo de Memoria:

- **Tiny/Base**: 2-4 GB RAM
- **Small**: 4-6 GB RAM
- **Medium/Large**: 6-8 GB RAM

### Optimizaciones Incluidas:

- ⚡ Arranque rápido (interfaz en 2-3 segundos)
- 🧠 Carga diferida de modelos IA
- 💾 Cache inteligente de modelos
- 🔄 Procesamiento por chunks para archivos grandes
- 🤫 Launchers silenciosos sin ventanas molestas

## 📞 Soporte y Contribución

### 🆘 Obtener Ayuda:

1. **Consulta este README** para problemas comunes
2. **Revisa el Manual de Usuario** (`MANUAL_DE_USUARIO.md`)
3. **Ejecuta diagnósticos** con los comandos de la sección de solución de problemas
4. **Reporta bugs** creando un issue en GitHub con detalles completos

### 🤝 Contribuir al Proyecto:

- 🐛 **Reportar bugs**: Crea un issue detallado en GitHub
- 💡 **Sugerencias**: Comparte ideas de mejora
- 🔧 **Código**: Los Pull Requests son bienvenidos
- 📖 **Documentación**: Ayuda a mejorar este README o el manual

### 📧 Información de Contacto:

- **GitHub**: [Tu usuario/voice-extractor](https://github.com/tu-usuario/voice-extractor)
- **Issues**: Usa GitHub Issues para reportes técnicos
- **Documentación**: Contribuye mejorando esta guía

## 📄 Licencia

Este proyecto es de **código abierto**. Ver archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Créditos y Agradecimientos

### Tecnologías Utilizadas:

- **[OpenAI Whisper](https://openai.com/research/whisper)**: Motor de transcripción IA de vanguardia
- **[FFmpeg](https://ffmpeg.org/)**: Procesamiento multimedia profesional
- **[PyInstaller](https://pyinstaller.org/)**: Compilación de ejecutables Python
- **[tkinter](https://docs.python.org/3/library/tkinter.html)**: Interfaz gráfica nativa
- **[PyTorch](https://pytorch.org/)**: Framework de aprendizaje automático

### Inspiración y Referencias:

- Comunidad de OpenAI por democratizar la IA
- Desarrolladores de software libre y open source
- Usuarios que han probado y mejorado la aplicación

---

## 🎉 ¡Comienza a Usar Voice Extractor!

**Voice Extractor v1.1** - Convierte cualquier audio a texto con IA 🚀

### ⚡ Inicio Rápido:

1. **Descargar**: Clona o descarga este repositorio
2. **Instalar**: Ejecuta `install_and_build.bat`
3. **Usar**: Ejecuta `dist/VoiceExtractor/VoiceExtractor.exe`

### 💡 Tip Pro:

Para mejores resultados, usa archivos de audio claro y el modelo **Base** como punto de partida. ¡Es el equilibrio perfecto entre velocidad y calidad!

**¡Disfruta extrayendo voz de tus archivos multimedia con inteligencia artificial! 🎬✨**
