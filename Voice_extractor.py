import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import subprocess
import tempfile
import whisper
import queue
import time
import sys

class VoiceExtractor:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Extractor - Whisper AI")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1a1a1a')
        self.root.minsize(800, 600)
          # Set icon
        self.set_application_icon()
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.video_file = None
        self.extracted_text = ""
        self.is_processing = False
        self.progress_queue = queue.Queue()
        self.text_queue = queue.Queue()
        self.metadata_info = {}
        self.current_progress = 0
        
        # Setup scrollable UI
        self.setup_scrollable_ui()
        
        # Start progress checking
        self.check_progress()
        
        # Add fade-in animation
        self.animate_fade_in()
    
    def set_application_icon(self):
        """Configura el icono de la aplicación de manera robusta"""
        # Posibles rutas del icono
        icon_paths = [
            "icon.ico",  # Desarrollo
            os.path.join(os.path.dirname(sys.executable), "icon.ico"),  # PyInstaller
            os.path.join(os.path.dirname(__file__), "icon.ico"),  # Relativo al script
            os.path.join(os.getcwd(), "icon.ico"),  # Directorio actual
        ]
        
        # Intentar cargar el icono desde diferentes rutas
        for icon_path in icon_paths:
            try:
                if os.path.exists(icon_path):
                    self.root.iconbitmap(icon_path)
                    break
            except Exception:
                continue
        
        # Si no se puede cargar icono, usar uno por defecto del sistema
        try:
            # En Windows, esto establece el icono estándar de Python
            self.root.wm_iconbitmap(bitmap="")
        except Exception:
            pass
    
    def setup_styles(self):
        style = ttk.Style()
        
        # Configure dark theme
        style.configure('TFrame', background='#1a1a1a')
        style.configure('TLabel', background='#1a1a1a', foreground='#ffffff')
        style.configure('TButton', background='#2d2d2d', foreground='#ffffff', borderwidth=0, focuscolor='none')
        style.configure('TRadiobutton', background='#1a1a1a', foreground='#ffffff', focuscolor='none')
        
        # Custom styles with improved fonts and sizing
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 28, 'bold'), 
                       foreground='#00ff88', 
                       background='#1a1a1a')
        
        style.configure('Heading.TLabel', 
                       font=('Segoe UI', 16, 'bold'), 
                       foreground='#ffffff', 
                       background='#2d2d2d')
        
        style.configure('SubHeading.TLabel', 
                       font=('Segoe UI', 13, 'bold'), 
                       foreground='#cccccc', 
                       background='#2d2d2d')
        
        style.configure('Info.TLabel', 
                       font=('Segoe UI', 12), 
                       foreground='#aaaaaa', 
                       background='#2d2d2d')
        
        style.configure('Success.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground='#00ff88', 
                       background='#2d2d2d')
        
        style.configure('Error.TLabel', 
                       font=('Segoe UI', 12, 'bold'), 
                       foreground='#ff4757', 
                       background='#2d2d2d')
        
        # Button styles with borders
        style.configure('Action.TButton', 
                       font=('Segoe UI', 14, 'bold'),
                       background='#00ff88',
                       foreground='#000000',
                       borderwidth=2,
                       focuscolor='none',
                       relief='solid')
        
        style.configure('Secondary.TButton', 
                       font=('Segoe UI', 12, 'bold'),
                       background='#ffffff',
                       foreground='#000000',
                       borderwidth=2,
                       focuscolor='none',
                       relief='solid')
        
        style.configure('Card.TFrame', 
                       background='#2d2d2d', 
                       relief='solid', 
                       borderwidth=2)
        
        style.configure('Radio.TRadiobutton',
                       font=('Segoe UI', 12),
                       background='#2d2d2d',
                       foreground='#cccccc',
                       focuscolor='none')
        
        # Enhanced button hover effects
        style.map('Action.TButton', 
                 background=[('active', '#00cc6a'), ('pressed', '#008c4a')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')],
                 borderwidth=[('active', 3), ('pressed', 3)])
        style.map('Secondary.TButton', 
                 background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')],
                 foreground=[('active', '#000000'), ('pressed', '#000000')],
                 borderwidth=[('active', 3), ('pressed', 3)])
    
    def setup_scrollable_ui(self):
        # Create main canvas and scrollbar
        self.canvas = tk.Canvas(self.root, bg='#1a1a1a', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Center content horizontally
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind canvas resize to center content
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Setup UI content
        self.setup_ui_content()
    
    def _on_canvas_configure(self, event):
        # Center the content horizontally
        canvas_width = event.width
        frame_width = self.scrollable_frame.winfo_reqwidth()
        if frame_width < canvas_width:
            x = (canvas_width - frame_width) // 2
        else:
            x = 0
        self.canvas.coords(self.canvas_window, x, 0)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def on_text_area_enter(self, event):
        """When mouse enters text area, bind scroll to text widget"""
        self.canvas.unbind_all("<MouseWheel>")
        def text_scroll(event):
            self.text_output.yview_scroll(int(-1*(event.delta/120)), "units")
        self.text_output.bind_all("<MouseWheel>", text_scroll)
    
    def on_text_area_leave(self, event):
        """When mouse leaves text area, bind scroll back to canvas"""
        self.text_output.unbind_all("<MouseWheel>")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def setup_ui_content(self):
        # Main container with padding and fixed width for centering
        main_container = ttk.Frame(self.scrollable_frame, padding="40")
        main_container.pack(anchor="n")
        
        # Set a fixed width for consistent centering
        main_container.configure(width=850)
        
        # Title with improved styling
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill="x", pady=(0, 40))
        
        title_label = ttk.Label(title_frame, text="🎬 Voice Extractor", style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Powered by OpenAI Whisper", 
                                  font=('Segoe UI', 14, 'italic'), 
                                  foreground='#888888', 
                                  background='#1a1a1a')
        subtitle_label.pack(pady=(8, 0))
        
        # File selection card with better spacing
        self.file_card = ttk.Frame(main_container, style='Card.TFrame', padding="30")
        self.file_card.pack(fill="x", pady=(0, 25))
        
        file_header = ttk.Label(self.file_card, text="📁 Select Media File", style='Heading.TLabel')
        file_header.pack(anchor="w", pady=(0, 20))
        
        file_content = ttk.Frame(self.file_card)
        file_content.pack(fill="x")
        
        self.file_label = ttk.Label(file_content, text="No file selected", style='Info.TLabel')
        self.file_label.pack(side="left", fill="x", expand=True, pady=5)
        
        browse_btn = ttk.Button(file_content, text="📂 Browse Files", 
                               command=self.browse_file, style='Secondary.TButton')
        browse_btn.pack(side="right", padx=(20, 0), ipadx=20, ipady=8)
        
        # Model selection card with improved layout
        self.model_card = ttk.Frame(main_container, style='Card.TFrame', padding="30")
        self.model_card.pack(fill="x", pady=(0, 25))
        
        model_header = ttk.Label(self.model_card, text="🤖 AI Configuration", style='Heading.TLabel')
        model_header.pack(anchor="w", pady=(0, 20))
        
        # Model selection with better spacing
        model_section = ttk.Frame(self.model_card)
        model_section.pack(fill="x", pady=(0, 25))
        
        ttk.Label(model_section, text="Model Quality:", style='SubHeading.TLabel').pack(anchor="w", pady=(0, 15))
        
        self.model_var = tk.StringVar(value="base")
        model_grid = ttk.Frame(model_section)
        model_grid.pack(fill="x")
        
        models = [
            ("⚡ Tiny (fastest, 39 MB)", "tiny"),
            ("⚖️ Base (balanced, 74 MB)", "base"),
            ("🎯 Small (better, 244 MB)", "small"),
            ("🔥 Medium (good, 769 MB)", "medium"),
            ("💎 Large (best, 1550 MB)", "large")
        ]
        
        for i, (text, value) in enumerate(models):
            radio = ttk.Radiobutton(model_grid, text=text, variable=self.model_var, 
                                   value=value, style='Radio.TRadiobutton')
            radio.grid(row=i//2, column=i%2, sticky="w", padx=(0, 40), pady=5)
        
        # Language selection with auto-detect as default
        lang_section = ttk.Frame(self.model_card)
        lang_section.pack(fill="x")
        
        ttk.Label(lang_section, text="Language:", style='SubHeading.TLabel').pack(anchor="w", pady=(0, 15))
        
        self.language_var = tk.StringVar(value="auto")
        lang_frame = ttk.Frame(lang_section)
        lang_frame.pack(fill="x")
        
        languages = [
            ("🌍 Auto-detect (recommended)", "auto"),
            ("🇪🇸 Spanish", "es"),
            ("🇺🇸 English", "en")
        ]
        
        for i, (text, value) in enumerate(languages):
            radio = ttk.Radiobutton(lang_frame, text=text, variable=self.language_var, 
                                   value=value, style='Radio.TRadiobutton')
            radio.grid(row=0, column=i, sticky="w", padx=(0, 50), pady=5)
        
        # Extract button with larger size and borders
        button_frame = ttk.Frame(main_container)
        button_frame.pack(pady=40)
        
        self.extract_button = ttk.Button(button_frame, text="🎯 Extract Voice", 
                                        command=self.start_extraction, 
                                        style='Action.TButton', state="disabled")
        self.extract_button.pack(ipadx=40, ipady=15)
        
        # Progress section with improved design
        self.progress_card = ttk.Frame(main_container, style='Card.TFrame', padding="30")
        self.progress_card.pack(fill="both", expand=True, pady=(0, 25))
        
        progress_header = ttk.Label(self.progress_card, text="📊 Progress", style='Heading.TLabel')
        progress_header.pack(anchor="w", pady=(0, 20))
        
        # Terminal-style progress bar only
        progress_container = ttk.Frame(self.progress_card)
        progress_container.pack(fill="x", pady=(0, 20))
          # Detailed progress label (like terminal output)
        self.detailed_progress_label = ttk.Label(progress_container, 
                                               text="", 
                                               font=('Consolas', 10), 
                                               foreground='#888888', 
                                               background='#2d2d2d',
                                               anchor='w')
        self.detailed_progress_label.pack(pady=5, fill='x')
        
        # Status with better positioning
        self.status_label = ttk.Label(self.progress_card, text="Ready to extract voice", style='Info.TLabel')
        self.status_label.pack(anchor="w", pady=(0, 25))
        
        # Text output section
        text_header = ttk.Label(self.progress_card, text="📝 Extracted Text", style='Heading.TLabel')
        text_header.pack(anchor="w", pady=(15, 20))
        
        # Enhanced text output
        text_container = ttk.Frame(self.progress_card)
        text_container.pack(fill="both", expand=True, pady=(0, 25))
        
        self.text_output = scrolledtext.ScrolledText(
            text_container,
            height=18,
            width=85,
            font=('Consolas', 11),
            wrap=tk.WORD,
            bg='#1e1e1e',
            fg='#ffffff',
            selectbackground='#00ff88',
            selectforeground='#000000',
            insertbackground='#00ff88',
            relief='solid',
            borderwidth=3,
            highlightthickness=2,
            highlightcolor='#00ff88',
            highlightbackground='#444444'
        )
        self.text_output.pack(fill="both", expand=True)
        
        # Bind mouse enter/leave events for scroll behavior
        self.text_output.bind("<Enter>", self.on_text_area_enter)
        self.text_output.bind("<Leave>", self.on_text_area_leave)
        
        # Save button with borders
        save_frame = ttk.Frame(self.progress_card)
        save_frame.pack()
        
        self.save_button = ttk.Button(save_frame, text="💾 Save Text to File", 
                                     command=self.save_text, style='Secondary.TButton', 
                                     state="disabled")
        self.save_button.pack(ipadx=25, ipady=12)
    
    def animate_fade_in(self):
        """Fade-in animation for the main window"""
        self.root.attributes('-alpha', 0)
        self.fade_in_step(0)
    
    def fade_in_step(self, alpha):
        if alpha < 1:
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self.fade_in_step(alpha + 0.05))
        else:
            self.root.attributes('-alpha', 1)
    
    def animate_button_pulse(self, button):
        """Pulse animation for buttons"""
        original_style = button.cget('style')
        button.configure(style='Action.TButton')
        self.root.after(100, lambda: button.configure(style=original_style))
    
    def browse_file(self):
        file_types = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("Audio files", "*.mp3 *.wav *.aac *.ogg *.m4a *.flac"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select video or audio file",
            filetypes=file_types        )
        
        if filename:
            self.video_file = filename
            display_name = os.path.basename(filename)
            if len(display_name) > 60:
                display_name = display_name[:57] + "..."
            self.file_label.config(text=f"✅ {display_name}", style='Success.TLabel')
            self.extract_button.config(state="normal")
            self.animate_card_highlight(self.file_card)
    
    def animate_card_highlight(self, card):
        """Highlight animation for cards"""
        # Simple highlight effect by updating the label
        for widget in card.winfo_children():
            if isinstance(widget, ttk.Label):
                original_color = widget.cget('foreground')
                widget.configure(foreground='#00ff88')
                self.root.after(200, lambda w=widget, c=original_color: w.configure(foreground=c))
                break
    
    def start_extraction(self):
        if not self.video_file:
            messagebox.showerror("Error", "Please select a video file first.")
            return
        
        if self.is_processing:
            messagebox.showinfo("Info", "Extraction is already in progress.")
            return
        
        # Animate button
        self.animate_button_pulse(self.extract_button)
        
        # Reset UI
        self.text_output.delete(1.0, tk.END)
        self.current_progress = 0
        self.extract_button.config(state="disabled")
        self.save_button.config(state="disabled")
        self.is_processing = True
        
        # Start extraction in a separate thread
        thread = threading.Thread(target=self.extract_voice)
        thread.daemon = True
        thread.start()
    
    def get_video_duration(self, video_file):
        """Get video duration using ffprobe"""
        try:
            cmd = [
                "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", video_file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            duration = float(result.stdout.strip())
              # Format duration as HH:MM:SS
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except Exception:
            return "Unknown"
    
    def extract_voice(self):
        try:
            self.update_status("🔄 Extracting audio from video...")
            self.update_progress(10)
            
            # Extract audio from video
            audio_file = self.extract_audio()
            
            self.update_progress(30)
            self.update_status("🧠 Loading Whisper model...")
            
            # Extract text with Whisper
            text = self.extract_with_whisper(audio_file)
            
            self.update_progress(100)
            self.update_status("✅ Extraction completed successfully!")
            
            # Update UI in main thread
            self.root.after(0, self.extraction_complete, text)
            
            # Clean up temporary file
            if os.path.exists(audio_file):
                os.remove(audio_file)
                
        except Exception as e:
            error_msg = f"❌ Error during extraction: {str(e)}"
            self.root.after(0, self.extraction_error, error_msg)
        finally:
            self.is_processing = False
    
    def extract_audio(self):
        # Create temporary audio file
        temp_audio = tempfile.mktemp(suffix=".wav")
        
        # Use ffmpeg to extract audio
        cmd = [
            "ffmpeg", "-i", self.video_file,
            "-ac", "1",  # mono
            "-ar", "16000",  # 16kHz sample rate
            "-y",  # overwrite output file
            temp_audio        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return temp_audio
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to extract audio: {e}")
        except FileNotFoundError:
            raise Exception("FFmpeg not found. Please install FFmpeg and add it to your PATH.")
    
    def extract_with_whisper(self, audio_file):
        try:
            # Strictly enforce model selection
            model_name = self.model_var.get()
            language = self.language_var.get()
            
            # Validate model selection
            valid_models = ["tiny", "base", "small", "medium", "large"]
            if model_name not in valid_models:
                model_name = "base"  # Fallback to base if invalid
            
            # Handle language selection properly
            if language == "auto":
                language = None  # Let Whisper auto-detect
            elif language not in ["es", "en", None]:
                language = None  # Fallback to auto-detect
            
            self.update_status(f"🤖 Loading Whisper model ({model_name})...")
            
            # Get video duration for metadata
            duration = self.get_video_duration(self.video_file)
            
            # Initialize text output with processing info
            self.root.after(0, self.init_realtime_display, model_name, duration)
            
            # Show initial loading message like terminal
            loading_msg = f"Loading model '{model_name}'...\n"
            self.root.after(0, self.append_text_realtime, loading_msg)
            
            # Load model with progress indication
            model = whisper.load_model(model_name)
            
            model_loaded_msg = f"Model '{model_name}' loaded successfully.\n\n"
            self.root.after(0, self.append_text_realtime, model_loaded_msg)
            
            self.update_progress(50)
            self.update_status("🎯 Transcribing audio...")
            
            # Show language detection message exactly like terminal
            if language is None:
                detect_msg = "Detecting language using up to the first 30 seconds. Use `--language` to specify the language\n"
                self.root.after(0, self.append_text_realtime, detect_msg)
            
            # Transcribe with options and capture verbose output
            transcribe_options = {
                "verbose": True,  # Enable verbose for terminal-like output
                "fp16": False,
                "word_timestamps": True
            }
            
            if language:
                transcribe_options["language"] = language
            
            # Custom transcription with real-time output capture
            result = self.transcribe_with_realtime_output(model, audio_file, transcribe_options)
            
            # Store metadata
            detected_language = result.get("language", "unknown")
            language_names = {
                "en": "English", "es": "Spanish", "fr": "French", "de": "German",
                "it": "Italian", "pt": "Portuguese", "ru": "Russian", "ja": "Japanese",
                "ko": "Korean", "zh": "Chinese", "ar": "Arabic", "hi": "Hindi"
            }
            detected_lang_name = language_names.get(detected_language, detected_language.upper())
            
            self.metadata_info = {
                "model": model_name,
                "language": detected_lang_name,
                "duration": duration
            }
            self.update_progress(90)
            return result["text"]
            
        except Exception as e:
            raise Exception(f"Whisper transcription failed: {e}")
    
    def transcribe_with_realtime_output(self, model, audio_file, options):
        """Custom transcription method that mimics terminal output"""
        import io
        import sys
        from contextlib import redirect_stdout, redirect_stderr
        
        try:
            # Simulate terminal output step by step
            self.root.after(0, self.append_text_realtime, "Processing audio file...\n")
            time.sleep(0.3)
            
            # Load audio and show file info like terminal
            audio_info = f"Input file: {os.path.basename(audio_file)}\n"
            self.root.after(0, self.append_text_realtime, audio_info)
            
            # Perform transcription
            result = model.transcribe(audio_file, **options)
            
            # Show detected language like terminal
            detected_language = result.get("language", "unknown")
            language_names = {
                "en": "English", "es": "Spanish", "fr": "French", "de": "German",
                "it": "Italian", "pt": "Portuguese", "ru": "Russian", "ja": "Japanese",
                "ko": "Korean", "zh": "Chinese", "ar": "Arabic", "hi": "Hindi"
            }
            detected_lang_name = language_names.get(detected_language, detected_language.upper())
            
            lang_detection_msg = f"Detected language: {detected_lang_name}\n\n"
            self.root.after(0, self.append_text_realtime, lang_detection_msg)
            
            # Process segments with terminal-like timestamps
            segments = result.get("segments", [])
            total_segments = len(segments)
            
            if segments:
                self.root.after(0, self.append_text_realtime, "Transcription segments:\n")
                self.root.after(0, self.append_text_realtime, "-" * 60 + "\n")
                
                for i, segment in enumerate(segments):
                    start = segment.get("start", 0)
                    end = segment.get("end", 0)
                    text = segment.get("text", "").strip()
                    
                    if text:
                        # Format exactly like Whisper terminal output
                        start_time = f"{int(start//60):02d}:{start%60:06.3f}"
                        end_time = f"{int(end//60):02d}:{end%60:06.3f}"
                        segment_line = f"[{start_time} --> {end_time}] {text}\n"
                        
                        # Update UI in main thread
                        self.root.after(0, self.append_text_realtime, segment_line)
                        
                        # Update progress in real time
                        segment_progress = 50 + (40 * (i + 1) / total_segments)
                        self.root.after(0, self.update_progress, segment_progress)
                        
                        # Update detailed progress
                        progress_text = f"segment {i+1}/{total_segments}"
                        self.root.after(0, self.update_detailed_progress, progress_text)
                        
                        # Small delay for visual effect like terminal
                        time.sleep(0.05)
            
            # Show completion message like terminal
            completion_msg = f"\n" + "=" * 60 + "\n"
            completion_msg += f"Transcription completed!\n"
            completion_msg += f"Segments processed: {total_segments}\n"
            completion_msg += f"Language: {detected_lang_name}\n"
            completion_msg += f"Model: {options.get('model', 'base')}\n"
            completion_msg += "=" * 60 + "\n\n"
            
            self.root.after(0, self.append_text_realtime, completion_msg)
              # Show final clean text
            final_text_header = "FINAL TRANSCRIPTION:\n" + "-" * 30 + "\n\n"
            self.root.after(0, self.append_text_realtime, final_text_header)
            self.root.after(0, self.append_text_realtime, result["text"])
            
            return result
            
        except Exception as e:
            error_msg = f"Error during transcription: {str(e)}\n"
            self.root.after(0, self.append_text_realtime, error_msg)
            raise
    
    def init_realtime_display(self, model_name, duration):
        """Initialize the real-time display with metadata like terminal"""
        # Clear text output
        self.text_output.delete(1.0, tk.END)
        
        # Add terminal-like header
        header_text = f"{'='*70}\n"
        header_text += f"  WHISPER AI VOICE EXTRACTION - TERMINAL OUTPUT\n"
        header_text += f"{'='*70}\n\n"
        header_text += f"📊 Configuration:\n"
        header_text += f"   • Model: {model_name.upper()}\n"
        header_text += f"   • Duration: {duration}\n"
        header_text += f"   • Language: {self.language_var.get() if self.language_var.get() != 'auto' else 'Auto-detect'}\n\n"
        header_text += f"🚀 Starting transcription process...\n"
        header_text += f"{'-'*70}\n\n"
        
        self.text_output.insert(tk.END, header_text)
        self.text_output.see(tk.END)
    
    def process_segments_realtime(self, result):
        """Process and display segments in real-time like Whisper terminal output"""
        def stream_segments():
            segments = result.get("segments", [])
            total_segments = len(segments)
            
            for i, segment in enumerate(segments):
                start = segment.get("start", 0)
                end = segment.get("end", 0)
                text = segment.get("text", "").strip()
                
                if text:
                    # Format exactly like Whisper terminal output
                    start_time = f"{int(start//60):02d}:{start%60:06.3f}"
                    end_time = f"{int(end//60):02d}:{end%60:06.3f}"
                    segment_line = f"[{start_time} --> {end_time}] {text}\n"
                    
                    # Update UI in main thread
                    self.root.after(0, self.append_text_realtime, segment_line)
                    
                    # Update progress in real time
                    segment_progress = 50 + (40 * (i + 1) / total_segments)
                    self.root.after(0, self.update_progress, segment_progress)
                    
                    # Update detailed progress
                    progress_text = f"{i+1}/{total_segments} segments processed"
                    self.root.after(0, self.update_detailed_progress, progress_text)
                    
                    # Small delay for visual effect
                    time.sleep(0.08)
            
            # After streaming all segments, add final summary
            time.sleep(0.5)
            summary_text = f"\n\n{'='*50}\n"
            summary_text += f"✅ TRANSCRIPTION COMPLETED\n"
            summary_text += f"📝 Total segments processed: {total_segments}\n"
            summary_text += f"🌍 Language: {self.metadata_info['language']}\n"
            summary_text += f"{'='*50}\n\n"
            summary_text += f"📋 COMPLETE TRANSCRIPTION (Clean Text)\n"
            summary_text += f"{'-'*40}\n\n"
            summary_text += result["text"]
            
            self.root.after(0, self.append_text_realtime, summary_text)
            
            # Final progress update
            self.root.after(0, self.update_progress, 100)
          # Start streaming in background thread
        stream_thread = threading.Thread(target=stream_segments)
        stream_thread.daemon = True
        stream_thread.start()
    
    def append_text_realtime(self, text):
        """Append text to output in real-time"""
        self.text_output.insert(tk.END, text)
        self.text_output.see(tk.END)
        self.root.update_idletasks()
    
    def update_detailed_progress(self, progress_text):
        """Update detailed progress label"""
        # Create terminal-like progress bar justified to the left
        bar_length = 40
        filled_length = int(bar_length * self.current_progress / 100)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        # Show processing speed like terminal, justified to the left
        detailed_text = f"{self.current_progress:3.0f}%|{bar}| {progress_text}"
        
        self.detailed_progress_label.config(text=detailed_text, anchor='w')
    
    def update_progress(self, value):
        self.current_progress = value
        self.progress_queue.put(("progress", value))
    
    def update_status(self, message):
        self.progress_queue.put(("status", message))
    
    def check_progress(self):
        try:
            while True:
                item_type, value = self.progress_queue.get_nowait()
                if item_type == "progress":
                    self.current_progress = value
                    # Update detailed progress bar
                    self.update_detailed_progress("processing...")
                elif item_type == "status":
                    self.status_label.config(text=value)
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_progress)
    
    def extraction_complete(self, text):
        self.extracted_text = text
        # Don't overwrite the streamed text, just ensure final state
        self.extract_button.config(state="normal")
        self.save_button.config(state="normal")
        self.status_label.config(text="✅ Extraction completed! Ready to save.", style='Success.TLabel')
        
        # Update final progress
        self.update_detailed_progress("✅ Completed!")
        
        # Animate completion
        self.animate_card_highlight(self.progress_card)
    
    def extraction_error(self, error_msg):
        messagebox.showerror("Error", error_msg)
        self.extract_button.config(state="normal")
        self.status_label.config(text="❌ Error occurred during extraction", style='Error.TLabel')
        self.current_progress = 0
    
    def save_text(self):
        if not self.extracted_text:
            messagebox.showwarning("Warning", "No text to save.")
            return
        
        if not self.video_file:
            messagebox.showerror("Error", "No video file selected.")
            return
        
        # Create filename in the same directory as the video file
        video_dir = os.path.dirname(self.video_file)
        video_name = os.path.splitext(os.path.basename(self.video_file))[0]
        txt_filename = os.path.join(video_dir, f"{video_name}.txt")
        
        try:
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(self.extracted_text)
            messagebox.showinfo("Success", f"✅ Text saved successfully!\n\nLocation: {txt_filename}")
            self.status_label.config(text=f"💾 Text saved as: {os.path.basename(txt_filename)}", style='Success.TLabel')
            
            # Animate save completion
            self.animate_button_pulse(self.save_button)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

def main():
    root = tk.Tk()
    VoiceExtractor(root)
    root.mainloop()

if __name__ == "__main__":
    main()