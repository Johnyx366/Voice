import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import subprocess
import tempfile
import queue
import time

# Variables globales para carga diferida
whisper_module = None
torch_module = None

def load_whisper():
    """Carga el módulo whisper de forma diferida"""
    global whisper_module
    if whisper_module is None:
        try:
            import whisper
            whisper_module = whisper
        except ImportError as e:
            print(f"Error cargando Whisper: {e}")
            return None
    return whisper_module

def load_torch():
    """Carga el módulo torch de forma diferida"""
    global torch_module
    if torch_module is None:
        try:
            import torch
            torch_module = torch
        except ImportError as e:
            print(f"Error cargando PyTorch: {e}")
            return None
    return torch_module

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
        self.whisper_model = None
        
        # Setup scrollable UI
        self.setup_scrollable_ui()
        
        # Start progress checking
        self.check_progress()
        
        # Add fade-in animation
        self.animate_fade_in()
        
        # Mostrar splash mientras se cargan las dependencias pesadas
        self.show_loading_splash()
    
    def show_loading_splash(self):
        """Muestra una pantalla de carga inicial"""
        self.loading_label = tk.Label(
            self.main_frame,
            text="🚀 Voice Extractor cargado!\n\n💡 Los modelos de IA se cargarán al usarlos por primera vez",
            font=("Segoe UI", 12),
            bg='#1a1a1a',
            fg='#00ff88',
            justify='center'
        )
        self.loading_label.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Ocultar después de 2 segundos
        self.root.after(2000, self.hide_loading_splash)
    
    def hide_loading_splash(self):
        """Oculta la pantalla de carga"""
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
    
    def set_application_icon(self):
        """Configura el icono de la aplicación de manera robusta"""
        # Rutas específicas del icono con prioridad
        icon_paths = [
            # Ruta absoluta especificada por el usuario
            r"C:\Users\Johny\Documents\Developer\Python\Voice\icon.ico",
            # Desarrollo local
            "icon.ico",
            # PyInstaller bundle
            os.path.join(os.path.dirname(sys.executable), "icon.ico"),
            # Relativo al script actual
            os.path.join(os.path.dirname(__file__), "icon.ico"),
            # PyInstaller temporary directory
            os.path.join(sys._MEIPASS, "icon.ico") if hasattr(sys, '_MEIPASS') else None,
            # En el directorio actual de trabajo
            os.path.join(os.getcwd(), "icon.ico"),
        ]
        
        icon_set = False
        for icon_path in icon_paths:
            if icon_path and os.path.exists(icon_path):
                try:
                    self.root.iconbitmap(icon_path)
                    print(f"✅ Icono configurado desde: {icon_path}")
                    icon_set = True
                    break
                except Exception as e:
                    print(f"⚠️ Error al cargar icono desde {icon_path}: {e}")
                    continue
        
        if not icon_set:
            print("⚠️ No se pudo configurar el icono personalizado")
        
        # Configurar también el icono de la ventana para asegurar que aparezca en la barra de tareas
        try:
            self.root.wm_iconbitmap(icon_paths[0] if os.path.exists(icon_paths[0]) else "icon.ico")
        except:
            pass

    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores base
        bg_color = '#1a1a1a'
        fg_color = '#ffffff'
        accent_color = '#00ff88'
        button_color = '#2d2d2d'
        
        try:
            # Configurar estilos de forma segura
            style.configure('Modern.TFrame', background=bg_color)
            style.configure('Modern.TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
            style.configure('Title.TLabel', background=bg_color, foreground=accent_color, font=('Segoe UI', 16, 'bold'))
            style.configure('Modern.TButton', background=button_color, foreground=fg_color, borderwidth=0, focuscolor='none')
            style.map('Modern.TButton', background=[('active', accent_color), ('pressed', '#00cc6a')])
            style.configure('Modern.TCombobox', background=button_color, foreground=fg_color, borderwidth=0)
            
        except Exception as e:
            print(f"⚠️ Error configurando estilos: {e}")
            # Continuar con estilos por defecto
            pass

    def setup_scrollable_ui(self):
        """Configura la interfaz con scroll"""
        # Canvas principal para scroll
        self.canvas = tk.Canvas(self.root, bg='#1a1a1a', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Modern.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Vincular eventos de scroll
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Frame principal dentro del scrollable
        self.main_frame = ttk.Frame(self.scrollable_frame, style='Modern.TFrame')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Crear la interfaz
        self.create_ui()

    def _on_mousewheel(self, event):
        """Maneja el scroll con la rueda del mouse"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_ui(self):
        """Crea la interfaz de usuario"""
        # Título principal
        title_label = ttk.Label(self.main_frame, text="🎬 Voice Extractor", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(self.main_frame, text="Extrae texto de videos y audios usando IA Whisper", style='Modern.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # Frame para selección de archivo
        file_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        file_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(file_frame, text="📂 Archivo de Video/Audio:", style='Modern.TLabel').pack(anchor="w", pady=(0, 5))
        
        file_select_frame = ttk.Frame(file_frame, style='Modern.TFrame')
        file_select_frame.pack(fill="x")
        
        self.file_label = ttk.Label(file_select_frame, text="Ningún archivo seleccionado", style='Modern.TLabel', foreground='#888888')
        self.file_label.pack(side="left", fill="x", expand=True)
        
        self.browse_button = ttk.Button(file_select_frame, text="📂 Browse Files", command=self.browse_file, style='Modern.TButton')
        self.browse_button.pack(side="right", padx=(10, 0))
        
        # Frame para configuraciones
        config_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        config_frame.pack(fill="x", pady=(0, 20))
        
        # Modelo de IA
        model_frame = ttk.Frame(config_frame, style='Modern.TFrame')
        model_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(model_frame, text="🤖 Modelo de IA:", style='Modern.TLabel').pack(anchor="w", pady=(0, 5))
        
        self.model_var = tk.StringVar(value="base")
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, values=[
            "tiny", "base", "small", "medium", "large"
        ], state="readonly", style='Modern.TCombobox', width=15)
        model_combo.pack(anchor="w")
        
        # Info de modelos
        model_info = ttk.Label(model_frame, 
                              text="💡 tiny=rápido/menor calidad, base=equilibrado, large=mejor calidad/más lento", 
                              style='Modern.TLabel', foreground='#888888', font=('Segoe UI', 8))
        model_info.pack(anchor="w", pady=(5, 0))
        
        # Idioma
        lang_frame = ttk.Frame(config_frame, style='Modern.TFrame')
        lang_frame.pack(fill="x", pady=(0, 15))
        
        ttk.Label(lang_frame, text="🌍 Idioma:", style='Modern.TLabel').pack(anchor="w", pady=(0, 5))
        
        self.language_var = tk.StringVar(value="auto")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language_var, values=[
            "auto", "es", "en", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"
        ], state="readonly", style='Modern.TCombobox', width=15)
        lang_combo.pack(anchor="w")
        
        # Botón de extracción
        self.extract_button = ttk.Button(self.main_frame, text="🎯 Extract Voice", command=self.start_extraction, style='Modern.TButton')
        self.extract_button.pack(pady=20)
        
        # Barra de progreso
        self.progress_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        self.progress_frame.pack(fill="x", pady=(0, 20))
        
        self.progress_label = ttk.Label(self.progress_frame, text="Listo para procesar", style='Modern.TLabel')
        self.progress_label.pack(anchor="w", pady=(0, 5))
        
        # Usar progressbar sin estilo personalizado para evitar errores
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(fill="x")
        
        # Área de texto extraído
        text_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        text_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        ttk.Label(text_frame, text="📝 Texto Extraído:", style='Modern.TLabel').pack(anchor="w", pady=(0, 5))
        
        # Frame para texto con scrollbar
        text_container = ttk.Frame(text_frame, style='Modern.TFrame')
        text_container.pack(fill="both", expand=True)
        
        self.text_area = scrolledtext.ScrolledText(text_container, 
                                                  wrap=tk.WORD, 
                                                  height=15, 
                                                  bg='#2d2d2d', 
                                                  fg='#ffffff', 
                                                  insertbackground='#ffffff',
                                                  font=('Segoe UI', 10),
                                                  relief=tk.FLAT,
                                                  borderwidth=0)
        self.text_area.pack(fill="both", expand=True)
        
        # Frame para botones de acción
        action_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        action_frame.pack(fill="x", pady=(10, 0))
        
        self.save_button = ttk.Button(action_frame, text="💾 Save Text to File", command=self.save_text, style='Modern.TButton', state="disabled")
        self.save_button.pack(side="left", padx=(0, 10))
        
        self.copy_button = ttk.Button(action_frame, text="📋 Copy to Clipboard", command=self.copy_text, style='Modern.TButton', state="disabled")
        self.copy_button.pack(side="left", padx=(0, 10))
        
        self.clear_button = ttk.Button(action_frame, text="🗑️ Clear Text", command=self.clear_text, style='Modern.TButton', state="disabled")
        self.clear_button.pack(side="left")

    def animate_fade_in(self):
        """Animación de fade-in para la ventana"""
        self.root.attributes('-alpha', 0.0)
        self.fade_in_step(0.0)

    def fade_in_step(self, alpha):
        """Paso de animación fade-in"""
        if alpha < 1.0:
            alpha += 0.05
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self.fade_in_step(alpha))
        else:
            self.root.attributes('-alpha', 1.0)

    def browse_file(self):
        """Abre el diálogo para seleccionar archivo"""
        file_types = [
            ("Archivos de Video", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("Archivos de Audio", "*.mp3 *.wav *.aac *.ogg *.m4a *.flac"),
            ("Todos los archivos", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de video o audio",
            filetypes=file_types
        )
        
        if filename:
            self.video_file = filename
            self.file_label.config(text=os.path.basename(filename), foreground='#00ff88')
            self.extract_button.config(state="normal")

    def start_extraction(self):
        """Inicia el proceso de extracción en un hilo separado"""
        if not self.video_file:
            messagebox.showerror("Error", "Por favor selecciona un archivo primero")
            return
        
        if self.is_processing:
            messagebox.showwarning("Aviso", "Ya hay un proceso en curso")
            return
        
        self.is_processing = True
        self.extract_button.config(text="⏸️ Procesando...", state="disabled")
        self.save_button.config(state="disabled")
        self.copy_button.config(state="disabled")
        self.clear_button.config(state="disabled")
        self.text_area.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        
        # Limpiar colas
        while not self.progress_queue.empty():
            self.progress_queue.get()
        while not self.text_queue.empty():
            self.text_queue.get()
        
        # Iniciar hilo de extracción
        extraction_thread = threading.Thread(target=self.extract_voice_thread)
        extraction_thread.daemon = True
        extraction_thread.start()

    def extract_voice_thread(self):
        """Hilo principal de extracción de voz"""
        try:
            self.progress_queue.put(("status", "🔄 Cargando modelo de IA..."))
            self.progress_queue.put(("progress", 10))
            
            # Cargar Whisper de forma diferida
            whisper = load_whisper()
            if whisper is None:
                raise Exception("No se pudo cargar el módulo Whisper")
            
            # Cargar el modelo de Whisper
            model_name = self.model_var.get()
            if self.whisper_model is None or getattr(self.whisper_model, 'name', '') != model_name:
                self.whisper_model = whisper.load_model(model_name)
            
            self.progress_queue.put(("status", "🎬 Preparando archivo de audio..."))
            self.progress_queue.put(("progress", 30))
            
            # Extraer audio si es video
            audio_file = self.prepare_audio_file()
            
            self.progress_queue.put(("status", "🧠 Procesando con IA Whisper..."))
            self.progress_queue.put(("progress", 50))
            
            # Transcribir
            language = None if self.language_var.get() == "auto" else self.language_var.get()
            result = self.whisper_model.transcribe(audio_file, language=language)
            
            self.progress_queue.put(("progress", 90))
            
            # Limpiar archivo temporal si se creó
            if audio_file != self.video_file:
                try:
                    os.remove(audio_file)
                except:
                    pass
            
            # Enviar resultado
            self.text_queue.put(result["text"])
            self.progress_queue.put(("status", "✅ ¡Extracción completada!"))
            self.progress_queue.put(("progress", 100))
            self.progress_queue.put(("complete", True))
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.progress_queue.put(("status", error_msg))
            self.progress_queue.put(("error", str(e)))

    def prepare_audio_file(self):
        """Prepara el archivo de audio para el procesamiento"""
        file_ext = os.path.splitext(self.video_file)[1].lower()
        
        # Si ya es un archivo de audio compatible, usarlo directamente
        if file_ext in ['.wav', '.mp3', '.m4a', '.flac']:
            return self.video_file
        
        # Convertir video a audio temporal
        temp_audio = tempfile.mktemp(suffix='.wav')
        
        cmd = [
            'ffmpeg', '-i', self.video_file,
            '-vn', '-acodec', 'pcm_s16le',
            '-ar', '16000', '-ac', '1',
            '-y', temp_audio
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return temp_audio
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error al convertir audio: {e.stderr}")
        except FileNotFoundError:
            raise Exception("FFmpeg no encontrado. Por favor instálalo.")

    def check_progress(self):
        """Verifica el progreso de la extracción"""
        try:
            while not self.progress_queue.empty():
                msg_type, msg_data = self.progress_queue.get_nowait()
                
                if msg_type == "status":
                    self.progress_label.config(text=msg_data)
                elif msg_type == "progress":
                    self.progress_bar['value'] = msg_data
                elif msg_type == "complete":
                    self.extraction_complete()
                elif msg_type == "error":
                    self.extraction_error(msg_data)
            
            # Verificar texto extraído
            while not self.text_queue.empty():
                text = self.text_queue.get_nowait()
                self.extracted_text = text
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, text)
                
        except queue.Empty:
            pass
        
        # Programar siguiente verificación
        self.root.after(100, self.check_progress)

    def extraction_complete(self):
        """Maneja la finalización exitosa de la extracción"""
        self.is_processing = False
        self.extract_button.config(text="🎯 Extract Voice", state="normal")
        self.save_button.config(state="normal")
        self.copy_button.config(state="normal")
        self.clear_button.config(state="normal")

    def extraction_error(self, error_msg):
        """Maneja errores durante la extracción"""
        self.is_processing = False
        self.extract_button.config(text="🎯 Extract Voice", state="normal")
        messagebox.showerror("Error de Extracción", f"Error durante la extracción:\n\n{error_msg}")

    def save_text(self):
        """Guarda el texto extraído en un archivo"""
        if not self.extracted_text:
            messagebox.showwarning("Aviso", "No hay texto para guardar")
            return
        
        # Sugerir nombre basado en el archivo original
        if self.video_file:
            base_name = os.path.splitext(os.path.basename(self.video_file))[0]
            default_name = f"{base_name}_transcription.txt"
            initial_dir = os.path.dirname(self.video_file)
        else:
            default_name = "transcription.txt"
            initial_dir = os.path.expanduser("~")
        
        filename = filedialog.asksaveasfilename(
            title="Guardar transcripción",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfilename=default_name,
            initialdir=initial_dir
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.extracted_text)
                messagebox.showinfo("Éxito", f"Texto guardado en:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar archivo:\n{str(e)}")

    def copy_text(self):
        """Copia el texto al portapapeles"""
        if not self.extracted_text:
            messagebox.showwarning("Aviso", "No hay texto para copiar")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(self.extracted_text)
        messagebox.showinfo("Éxito", "Texto copiado al portapapeles")

    def clear_text(self):
        """Limpia el área de texto"""
        self.text_area.delete(1.0, tk.END)
        self.extracted_text = ""
        self.save_button.config(state="disabled")
        self.copy_button.config(state="disabled")
        self.clear_button.config(state="disabled")
        self.progress_label.config(text="Listo para procesar")
        self.progress_bar['value'] = 0

def main():
    """Función principal"""
    root = tk.Tk()
    app = VoiceExtractor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
