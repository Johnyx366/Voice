# Voice to Text Extractor Configuration

# Default Whisper model (tiny, base, small, medium, large)
DEFAULT_MODEL = "base"

# Audio extraction settings
AUDIO_SAMPLE_RATE = 16000  # 16kHz is optimal for Whisper
AUDIO_CHANNELS = 1  # Mono

# Output settings
INCLUDE_WORD_TIMESTAMPS = True
INCLUDE_CONFIDENCE_SCORES = False

# UI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FONT_SIZE = 10

# Supported file formats
AUDIO_FORMATS = ['.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.wma']
VIDEO_FORMATS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.mpg', '.mpeg']

# FFmpeg settings
FFMPEG_TIMEOUT = 300  # 5 minutes timeout
