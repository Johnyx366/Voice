import PyInstaller.__main__
import sys
import os

# Configuración mejorada para crear el ejecutable
PyInstaller.__main__.run([
    'voice_extractor.py',
    '--name=VoiceToTextExtractor',
    '--onefile',
    '--windowed',
    '--icon=icon.png',  # Pillow now installed for automatic conversion
    '--hidden-import=whisper',
    '--hidden-import=torch',
    '--hidden-import=torchaudio',
    '--hidden-import=tiktoken',
    '--hidden-import=numpy',
    '--hidden-import=ffmpeg',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.filedialog',
    '--hidden-import=tkinter.messagebox',
    '--hidden-import=tkinter.scrolledtext',
    '--hidden-import=pathlib',
    '--hidden-import=threading',
    '--hidden-import=json',
    '--hidden-import=datetime',
    '--hidden-import=subprocess',
    '--hidden-import=whisper.model',
    '--hidden-import=whisper.audio',
    '--hidden-import=whisper.decoding',
    '--hidden-import=whisper.normalizers',
    '--hidden-import=whisper.timing',
    '--hidden-import=whisper.transcribe',
    '--hidden-import=whisper.utils',
    '--collect-all=whisper',
    '--collect-all=torch',
    '--collect-all=torchaudio',
    '--collect-all=tiktoken',
    '--collect-submodules=whisper',
    '--collect-submodules=torch',
    '--collect-submodules=torchaudio',
    '--collect-data=whisper',
    '--collect-data=torch',
    '--collect-data=torchaudio',
    '--collect-data=tiktoken',
    '--add-data=*.py;.',
    '--exclude-module=tensorboard',  # Exclude problematic module
    '--exclude-module=tensorflow',   # Exclude if not needed
    '--exclude-module=matplotlib',   # Exclude if not needed
    '--exclude-module=pytest',       # Exclude test modules
    '--exclude-module=test',
    '--exclude-module=tests',
    '--clean',
    '--noconfirm',
    '--log-level=INFO',
])