# Voice to Text Extractor

Este proyecto utiliza OpenAI Whisper para extraer texto de archivos de audio y video con timestamps precisos.

## Características

- Interfaz gráfica intuitiva con Tkinter
- Soporte para múltiples formatos de audio y video
- Extracción automática de audio de archivos de video usando FFmpeg
- Transcripción con timestamps usando modelos Whisper
- Múltiples modelos disponibles (tiny, base, small, medium, large)
- Guardado automático con nombre del archivo original
- Barra de progreso durante el procesamiento

## Instalación

### 1. Crear y activar entorno virtual

```bash
cd voice
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar FFmpeg

#### Windows:

Ejecuta el archivo `install_ffmpeg.bat` incluido o descarga FFmpeg desde https://ffmpeg.org/

#### Linux:

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Mac:

```bash
brew install ffmpeg
```

## Uso

1. Ejecuta la aplicación:

```bash
python voice_extractor.py
```

2. Selecciona el modelo Whisper (recomendado: "base" para uso general)

3. Haz clic en "Load Model" para precargar el modelo (opcional pero recomendado)

4. Selecciona un archivo de audio o video usando "Browse"

5. Haz clic en "Extract Text" para iniciar la transcripción

6. El texto extraído aparecerá con timestamps en el área de texto

7. Usa "Save Text to File" para guardar el resultado

## Modelos Whisper

- **tiny**: Más rápido, menor precisión (~39 MB)
- **base**: Buen equilibrio velocidad/precisión (~74 MB)
- **small**: Mayor precisión (~244 MB)
- **medium**: Muy buena precisión (~769 MB)
- **large**: Máxima precisión (~1550 MB)

## Formatos Soportados

### Audio:

MP3, WAV, M4A, FLAC, AAC, OGG, WMA

### Video:

MP4, AVI, MKV, MOV, WMV, FLV, WebM, M4V, 3GP, MPG, MPEG

## Requisitos del Sistema

- Python 3.8+
- FFmpeg instalado y en PATH
- Al menos 4GB RAM (recomendado 8GB para modelos grandes)
- Conexión a internet para la primera descarga de modelos

## Solución de Problemas

### Error "FFmpeg not found":

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
