# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Datos y módulos de Whisper (solo los esenciales)
whisper_data = collect_data_files('whisper')
whisper_modules = collect_submodules('whisper')

# Archivos adicionales necesarios
added_files = [
    ('icon.ico', '.'),
    ('README.md', '.'),
]

# Intentar incluir FFmpeg si está disponible
try:
    import ffmpeg
    ffmpeg_data = collect_data_files('ffmpeg')
    added_files.extend(ffmpeg_data)
except ImportError:
    pass

block_cipher = None

a = Analysis(
    ['Voice_extractor.py'],
    pathex=[],
    binaries=[],
    datas=added_files + whisper_data,
    hiddenimports=[
        'whisper',
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
        'ssl',
        '_ssl',
        'certifi',
        'urllib3',
        'requests',
        'tqdm',
    ] + whisper_modules,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'IPython',
        'notebook',
        'torch.distributions',
        'torch.optim',
        'torch.nn.modules.transformer',
        'torchaudio.datasets',
        'torchaudio.models',
        'torchaudio.pipelines',
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
    [],
    exclude_binaries=True,
    name='VoiceExtractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Deshabilitado para evitar problemas con DLLs
    runtime_tmpdir=None,
    console=False,  # Sin consola para interfaz limpia - IMPORTANTE
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Icono principal integrado en el ejecutable
    version='version_info.txt',  # Información de versión
    uac_admin=False,  # No requiere permisos de administrador
    uac_uiaccess=False  # Sin acceso especial de UI
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='VoiceExtractor',
)
