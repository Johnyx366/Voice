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

## 🚀 Instalación Rápida

### Opción 1: Instalador Automático (Recomendado)

```bash
# Ejecuta el instalador que configura todo automáticamente
install_and_build.bat
```

### Opción 2: Instalación Manual

```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Instalar FFmpeg
install_ffmpeg.bat

# 4. Compilar ejecutable
python build_exe.py
```

## 📁 Estructura del Proyecto

```
Voice/
├── Voice_extractor.py      # 🐍 Código principal de la aplicación
├── requirements.txt        # 📦 Dependencias de Python
├── install_and_build.bat   # 🛠️ Instalador completo automático
├── build_exe.py           # 🔨 Compilador de ejecutable
├── install_ffmpeg.bat     # 🎥 Instalador de FFmpeg
├── icon.ico              # 🎨 Icono de la aplicación
├── icon.png              # 🎨 Icono alternativo
├── README.md             # 📖 Este archivo
└── MANUAL_DE_USUARIO.txt # 📚 Manual detallado de usuario
```

## 🎯 Uso

1. **Ejecutar**: `python Voice_extractor.py` o usar el ejecutable compilado
2. **Seleccionar**: Elige tu archivo de video/audio
3. **Configurar**: Selecciona modelo de IA y idioma
4. **Extraer**: Haz clic en "Extract Voice"
5. **Guardar**: Exporta el texto transcrito

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

## 📞 Soporte y Contribución

- 🐛 **Reportar bugs**: Crea un issue en GitHub
- 💡 **Sugerencias**: Comparte tus ideas de mejora
- 🔧 **Contribuir**: Los PRs son bienvenidos

## 📄 Licencia

Este proyecto es de código abierto. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Créditos

- **OpenAI Whisper**: Motor de transcripción IA
- **FFmpeg**: Procesamiento de audio/video
- **PyInstaller**: Compilación de ejecutables
- **Tkinter**: Interfaz gráfica

---

**Voice Extractor v1.0** - Convierte cualquier audio a texto con IA 🚀

- Asegúrate de que FFmpeg esté instalado y en tu PATH
- En Windows, ejecuta `install_ffmpeg.bat`

### Error de memoria:

- Usa un modelo más pequeño (tiny o base)
- Cierra otras aplicaciones que consuman memoria

### Archivo no soportado:

- Verifica que el archivo no esté corrupto
- Convierte el archivo a un formato más común (MP3, MP4)

## Estructura del Proyecto

```
voice/
├── venv/                    # Entorno virtual
├── voice_extractor.py       # Aplicación principal
├── requirements.txt         # Dependencias Python
├── install_ffmpeg.bat      # Instalador FFmpeg (Windows)
└── README.md               # Este archivo
```
