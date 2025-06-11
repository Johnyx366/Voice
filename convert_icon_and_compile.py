"""
Alternative compiler that converts PNG to ICO first, then compiles
"""
import PyInstaller.__main__
import sys
import os
from PIL import Image

def convert_png_to_ico():
    """Convert PNG icon to ICO format"""
    try:
        if os.path.exists('icon.png'):
            # Open and convert the image
            img = Image.open('icon.png')
            # Resize to standard icon sizes and save as ICO
            img.save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (256,256)])
            print("Successfully converted icon.png to icon.ico")
            return 'icon.ico'
        else:
            print("icon.png not found, proceeding without icon")
            return None
    except Exception as e:
        print(f"Error converting icon: {e}")
        return None

def main():
    # Convert icon
    icon_file = convert_png_to_ico()
    
    # Build arguments
    args = [
        'voice_extractor.py',
        '--name=VoiceToTextExtractor',
        '--onefile',
        '--windowed',
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
        '--collect-data=whisper',
        '--collect-data=torch',
        '--collect-data=torchaudio',
        '--collect-data=tiktoken',
        '--exclude-module=tensorboard',
        '--exclude-module=tensorflow',
        '--exclude-module=matplotlib',
        '--exclude-module=pytest',
        '--exclude-module=test',
        '--exclude-module=tests',
        '--clean',
        '--noconfirm',
        '--log-level=INFO',
    ]
    
    # Add icon if conversion successful
    if icon_file:
        args.append(f'--icon={icon_file}')
    
    # Run PyInstaller
    print("Starting PyInstaller compilation...")
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    main()
