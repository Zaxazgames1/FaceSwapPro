#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de la interfaz gráfica para FaceSwapPro.

Este módulo contiene la clase AppWindow que implementa la interfaz
gráfica de usuario utilizando Tkinter con un diseño moderno y atractivo.
"""

import logging
import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
import subprocess

class AppWindow:
    """
    Clase que implementa la interfaz gráfica de FaceSwapPro.
    
    Proporciona una interfaz gráfica moderna y amigable para utilizar
    las funcionalidades de intercambio de rostros.
    """
    
    def __init__(self, app):
        """
        Inicializa la ventana de la aplicación.
        
        Args:
            app: Instancia de la clase FaceSwapApp.
        """
        self.logger = logging.getLogger('FaceSwapPro.AppWindow')
        self.logger.info("Inicializando interfaz gráfica...")
        
        self.app = app
        self.source_img_path = None
        self.target_img_path = None
        self.result_img_path = None
        
        # Variables para mostrar imágenes
        self.source_img = None
        self.target_img = None
        self.result_img = None
        
        # Variables para controlar procesamiento
        self.processing = False
        
        # Crear ventana principal primero
        self.root = tk.Tk()
        self.root.title("FaceSwapPro 🎭 - Intercambio de Rostros Ultra Realista")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Definir colores de la aplicación
        self.colors = {
            "primary": "#4a6baf",      # Azul principal
            "secondary": "#7986CB",    # Azul secundario
            "accent": "#FF5252",       # Acento rojo
            "success": "#66BB6A",      # Verde para éxito
            "warning": "#FFA726",      # Naranja para advertencias
            "background": "#F5F7FA",   # Fondo principal
            "text": "#212121",         # Texto principal
            "text_light": "#FFFFFF",   # Texto sobre fondos oscuros
            "gray_light": "#E0E0E0",   # Gris claro para bordes
            "gray_dark": "#9E9E9E"     # Gris oscuro para texto secundario
        }
        
        # Configurar colores de la ventana principal
        self.root.configure(bg=self.colors["background"])
        
        # Ahora es seguro crear las variables de Tkinter
        self.quality_level = tk.IntVar(value=2)  # Nivel de calidad: 1=Básico, 2=HD, 3=Ultra HD
    
    def run(self):
        """
        Ejecuta la ventana principal de la aplicación.
        """
        self.setup_ui()
        self.root.mainloop()
    
    def setup_ui(self):
        """
        Configura la interfaz de usuario.
        """
        # Configurar estilo
        self.setup_style()
        
        # Marco principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Marco de control (izquierda)
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Marco de imágenes (derecha)
        images_frame = ttk.Frame(main_frame)
        images_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Configurar secciones
        self.setup_control_panel(control_frame)
        self.setup_images_panel(images_frame)
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo para transformar rostros ✨")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.GROOVE, 
                             anchor=tk.W, padding=(10, 5))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Cargar imágenes disponibles
        self.load_available_images()
    
    def setup_style(self):
        """
        Configura el estilo visual moderno de la aplicación.
        """
        style = ttk.Style()
        
        # Configurar tema
        try:
            style.theme_use("clam")  # Tema más moderno
        except tk.TclError:
            pass  # Si el tema no está disponible, usar el predeterminado
        
        # Estilos personalizados
        style.configure("TFrame", background=self.colors["background"])
        style.configure("TLabelframe", background=self.colors["background"])
        style.configure("TLabelframe.Label", 
                       font=("Segoe UI", 11, "bold"), 
                       foreground=self.colors["primary"])
        
        # Etiquetas
        style.configure("TLabel", 
                       font=("Segoe UI", 10),
                       background=self.colors["background"],
                       foreground=self.colors["text"])
        
        style.configure("Header.TLabel", 
                       font=("Segoe UI", 12, "bold"),
                       foreground=self.colors["primary"])
        
        style.configure("Title.TLabel", 
                       font=("Segoe UI", 16, "bold"),
                       foreground=self.colors["primary"])
        
        style.configure("Info.TLabel", 
                       font=("Segoe UI", 9),
                       foreground=self.colors["gray_dark"])
        
        # Botones
        style.configure("TButton", 
                       font=("Segoe UI", 10),
                       padding=6)
        
        style.configure("Primary.TButton", 
                       background=self.colors["primary"],
                       foreground=self.colors["text_light"])
        
        style.map("Primary.TButton",
                 background=[('active', self.colors["secondary"])],
                 foreground=[('active', self.colors["text_light"])])
        
        style.configure("Accent.TButton", 
                       background=self.colors["accent"],
                       foreground=self.colors["text_light"])
        
        style.map("Accent.TButton",
                 background=[('active', '#FF7575')],
                 foreground=[('active', self.colors["text_light"])])
        
        style.configure("Success.TButton", 
                       background=self.colors["success"],
                       foreground=self.colors["text_light"])
        
        style.map("Success.TButton",
                 background=[('active', '#88CC8C')],
                 foreground=[('active', self.colors["text_light"])])
        
        # Botón grande para procesar
        style.configure("Big.TButton", 
                       font=("Segoe UI", 12, "bold"),
                       padding=12)
        
        # Combobox
        style.configure("TCombobox", 
                       padding=5,
                       foreground=self.colors["text"])
        
        # Radiobuttons
        style.configure("TRadiobutton", 
                       font=("Segoe UI", 10),
                       background=self.colors["background"],
                       foreground=self.colors["text"])
        
        # Barra de progreso
        style.configure("TProgressbar", 
                       background=self.colors["success"],
                       troughcolor=self.colors["gray_light"])
    
    def setup_control_panel(self, parent):
        """
        Configura el panel de control moderno.
        
        Args:
            parent: Widget padre donde se colocará el panel de control.
        """
        # Título con logo
        title_frame = ttk.Frame(parent, padding=(0, 0, 0, 10))
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="FaceSwapPro", style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        slogan_label = ttk.Label(title_frame, text="Transformación facial avanzada", 
                               style="Info.TLabel")
        slogan_label.pack()
        
        # Separador
        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 15))
        
        # Sección de imágenes
        images_section = ttk.LabelFrame(parent, text="📷 Selección de Imágenes", padding="10")
        images_section.pack(fill=tk.X, pady=(0, 15))
        
        # Combobox para imagen fuente
        ttk.Label(images_section, text="Imagen Fuente (rostro a usar):", 
                 style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        self.source_combo = ttk.Combobox(images_section, state="readonly", width=30)
        self.source_combo.pack(fill=tk.X, pady=(0, 10))
        self.source_combo.bind("<<ComboboxSelected>>", self.on_source_selected)
        
        # Combobox para imagen objetivo
        ttk.Label(images_section, text="Imagen Objetivo (donde poner el rostro):", 
                 style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        self.target_combo = ttk.Combobox(images_section, state="readonly", width=30)
        self.target_combo.pack(fill=tk.X, pady=(0, 10))
        self.target_combo.bind("<<ComboboxSelected>>", self.on_target_selected)
        
        # Botones para cargar imágenes
        btn_frame = ttk.Frame(images_section)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(btn_frame, text="Cargar Imagen...", style="Primary.TButton",
                  command=self.on_load_image).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Actualizar Lista", 
                  command=self.load_available_images).pack(side=tk.LEFT)
        
        # Sección de calidad
        quality_section = ttk.LabelFrame(parent, text="✨ Nivel de Calidad", padding="10")
        quality_section.pack(fill=tk.X, pady=(0, 15))
        
        # Opciones de calidad
        qual_frame = ttk.Frame(quality_section)
        qual_frame.pack(fill=tk.X, pady=(5, 5))
        
        # Radiobuttons con mejor aspecto
        ttk.Radiobutton(qual_frame, text="Básico", variable=self.quality_level, 
                       value=1).grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Label(qual_frame, text="Más rápido", style="Info.TLabel").grid(row=0, column=1, sticky=tk.W)
        
        ttk.Radiobutton(qual_frame, text="HD", variable=self.quality_level, 
                       value=2).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Label(qual_frame, text="Recomendado", style="Info.TLabel").grid(row=1, column=1, sticky=tk.W)
        
        ttk.Radiobutton(qual_frame, text="Ultra HD", variable=self.quality_level, 
                       value=3).grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        ttk.Label(qual_frame, text="Más lento, mejor calidad", style="Info.TLabel").grid(row=2, column=1, sticky=tk.W)
        
        # Sección de acciones
        actions_section = ttk.LabelFrame(parent, text="🚀 Acciones", padding="10")
        actions_section.pack(fill=tk.X, pady=(0, 15))
        
        # Botón de procesar (con más estilo)
        self.process_btn = ttk.Button(actions_section, text="¡Intercambiar Rostros!", 
                                    style="Big.TButton", command=self.on_process)
        self.process_btn.pack(fill=tk.X, pady=(5, 15))
        
        # Más acciones con mejores estilos
        action_btns_frame = ttk.Frame(actions_section)
        action_btns_frame.pack(fill=tk.X)
        
        ttk.Button(action_btns_frame, text="Ver Resultado", style="Success.TButton",
                  command=self.on_view_result).pack(fill=tk.X, pady=(0, 8))
        ttk.Button(action_btns_frame, text="Guardar Como...", style="Primary.TButton",
                  command=self.on_save_as).pack(fill=tk.X, pady=(0, 8))
        ttk.Button(action_btns_frame, text="Abrir Carpeta de Salida", 
                  command=self.on_open_output_folder).pack(fill=tk.X)
        
        # Indicador de progreso
        progress_section = ttk.LabelFrame(parent, text="📊 Progreso", padding="10")
        progress_section.pack(fill=tk.X, pady=(0, 15))
        
        self.progress = ttk.Progressbar(progress_section, orient=tk.HORIZONTAL, 
                                      length=100, mode='determinate', style="TProgressbar")
        self.progress.pack(fill=tk.X, pady=(5, 8))
        
        self.progress_label = ttk.Label(progress_section, text="Listo", style="Info.TLabel")
        self.progress_label.pack(anchor=tk.W)
        
        # Sección de información
        info_section = ttk.LabelFrame(parent, text="ℹ️ Información", padding="10")
        info_section.pack(fill=tk.X)
        
        ttk.Label(info_section, text="Desarrollado por FaceSwapPro Team", 
                 wraplength=250).pack(pady=(0, 5))
        ttk.Label(info_section, text="Versión 1.0.0", 
                 foreground=self.colors["gray_dark"]).pack()
    
    def setup_images_panel(self, parent):
        """
        Configura el panel de imágenes moderno.
        
        Args:
            parent: Widget padre donde se colocará el panel de imágenes.
        """
        # Marco para las imágenes
        images_label_frame = ttk.LabelFrame(parent, text="📸 Vista Previa de Imágenes", padding="10")
        images_label_frame.pack(fill=tk.BOTH, expand=True)
        
        # Paneles para las imágenes
        images_panel = ttk.Frame(images_label_frame)
        images_panel.pack(fill=tk.BOTH, expand=True)
        
        # Panel para imagen fuente
        source_frame = ttk.LabelFrame(images_panel, text="Imagen Fuente", padding="8")
        source_frame.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")
        
        self.source_canvas = tk.Canvas(source_frame, bg=self.colors["gray_light"], 
                                     highlightthickness=0)
        self.source_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Panel para imagen objetivo
        target_frame = ttk.LabelFrame(images_panel, text="Imagen Objetivo", padding="8")
        target_frame.grid(row=0, column=1, padx=8, pady=8, sticky="nsew")
        
        self.target_canvas = tk.Canvas(target_frame, bg=self.colors["gray_light"], 
                                     highlightthickness=0)
        self.target_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Panel para resultado (más grande)
        result_frame = ttk.LabelFrame(images_panel, text="Resultado Final", padding="8")
        result_frame.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="nsew")
        
        self.result_canvas = tk.Canvas(result_frame, bg=self.colors["gray_light"], 
                                     highlightthickness=0)
        self.result_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Configurar proporciones de la cuadrícula
        images_panel.grid_rowconfigure(0, weight=1)
        images_panel.grid_rowconfigure(1, weight=2)  # Dar más espacio al resultado
        images_panel.grid_columnconfigure(0, weight=1)
        images_panel.grid_columnconfigure(1, weight=1)
    
    def load_available_images(self):
        """
        Carga las imágenes disponibles en los combobox.
        """
        self.logger.info("Cargando imágenes disponibles...")
        
        # Obtener lista de imágenes
        images = self.app.get_available_images()
        
        # Configurar comboboxes
        self.source_combo['values'] = images
        self.target_combo['values'] = images
        
        # Mostrar mensaje según número de imágenes
        if not images:
            self.status_var.set("No hay imágenes disponibles. Por favor, cargue algunas.")
            messagebox.showinfo("Sin imágenes", 
                             "No hay imágenes disponibles en la carpeta de datos.\n"
                             "Por favor, cargue algunas imágenes usando 'Cargar Imagen'.")
        else:
            self.status_var.set(f"Se encontraron {len(images)} imágenes. ¡Listo para comenzar!")
            
            # Seleccionar las primeras imágenes si hay más de una
            if len(images) >= 2:
                self.source_combo.current(0)
                self.target_combo.current(1)
                self.on_source_selected(None)
                self.on_target_selected(None)
            elif len(images) == 1:
                self.source_combo.current(0)
                self.target_combo.current(0)
                self.on_source_selected(None)
                self.on_target_selected(None)
    
    def on_source_selected(self, event):
        """
        Maneja la selección de la imagen fuente.
        
        Args:
            event: Evento de selección.
        """
        selected = self.source_combo.get()
        if not selected:
            return
        
        self.source_img_path = os.path.join(self.app.data_dir, selected)
        self.logger.info(f"Imagen fuente seleccionada: {self.source_img_path}")
        
        # Mostrar imagen
        self.show_image_on_canvas(self.source_img_path, self.source_canvas)
        
        # Actualizar estado
        self.status_var.set(f"Imagen fuente seleccionada: {selected}")
    
    def on_target_selected(self, event):
        """
        Maneja la selección de la imagen objetivo.
        
        Args:
            event: Evento de selección.
        """
        selected = self.target_combo.get()
        if not selected:
            return
        
        self.target_img_path = os.path.join(self.app.data_dir, selected)
        self.logger.info(f"Imagen objetivo seleccionada: {self.target_img_path}")
        
        # Mostrar imagen
        self.show_image_on_canvas(self.target_img_path, self.target_canvas)
        
        # Actualizar estado
        self.status_var.set(f"Imagen objetivo seleccionada: {selected}")
    
    def on_load_image(self):
        """
        Maneja la acción de cargar una nueva imagen.
        """
        file_paths = filedialog.askopenfilenames(
            title="Seleccionar Imagen(es)",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png"), ("Todos los archivos", "*.*")]
        )
        
        if not file_paths:
            return
        
        # Copiar archivos seleccionados a la carpeta de datos
        copied_files = []
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.app.data_dir, file_name)
            
            try:
                import shutil
                shutil.copy2(file_path, dest_path)
                self.logger.info(f"Imagen copiada a: {dest_path}")
                copied_files.append(file_name)
            except Exception as e:
                self.logger.error(f"Error al copiar imagen: {e}")
                messagebox.showerror("Error", f"No se pudo copiar la imagen: {e}")
        
        # Actualizar lista de imágenes
        self.load_available_images()
        
        # Mostrar mensaje de éxito
        if copied_files:
            self.status_var.set(f"Se cargaron {len(copied_files)} imágenes nuevas.")
            messagebox.showinfo("Imágenes Cargadas", 
                             f"Se cargaron {len(copied_files)} imágenes correctamente!")
    
    def on_process(self):
        """
        Maneja la acción de procesar el intercambio de rostros.
        """
        if self.processing:
            messagebox.showinfo("En Proceso", "Ya hay un proceso en curso. Por favor, espere.")
            return
        
        if not self.source_img_path or not self.target_img_path:
            messagebox.showwarning("Faltan Imágenes", 
                               "Por favor, seleccione tanto la imagen fuente como la objetivo.")
            return
        
        # Iniciar procesamiento en un hilo separado
        self.processing = True
        self.process_btn.state(['disabled'])
        self.progress['value'] = 0
        self.progress_label.config(text="Iniciando procesamiento...")
        self.status_var.set("⏳ Procesando intercambio de rostros...")
        
        threading.Thread(target=self.process_face_swap, daemon=True).start()
    
    def process_face_swap(self):
        """
        Realiza el proceso de intercambio de rostros en un hilo separado.
        """
        try:
            # Actualizar interfaz
            self.update_progress(10, "Preparando imágenes...")
            
            # Obtener nivel de calidad
            quality = self.quality_level.get()
            quality_text = ["Básico", "HD", "Ultra HD"][quality - 1]
            
            # Procesar intercambio de rostros
            self.update_progress(30, f"Realizando intercambio en calidad {quality_text}...")
            
            # Llamar al método de procesamiento de la aplicación principal
            self.result_img_path = self.app.process_face_swap(
                self.source_img_path, 
                self.target_img_path, 
                quality
            )
            
            # Verificar resultado
            if not self.result_img_path:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                              "No se pudo completar el intercambio de rostros.\n"
                              "Por favor, intente con otras imágenes."))
                self.update_progress(0, "Error en el procesamiento.")
                return
            
            # Mostrar resultado
            self.update_progress(80, "Cargando el resultado final...")
            self.root.after(0, lambda: self.show_image_on_canvas(self.result_img_path, self.result_canvas))
            
            # Completado
            self.update_progress(100, "¡Procesamiento completado con éxito!")
            self.root.after(0, lambda: messagebox.showinfo("¡Éxito!", 
                                                "¡Intercambio de rostros completado con éxito!\n"
                                                "El resultado se guardó en la carpeta de salida."))
        
        except Exception as e:
            self.logger.error(f"Error durante el procesamiento: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", 
                                                    f"Error durante el procesamiento: {e}"))
            self.update_progress(0, "Error en el procesamiento.")
        
        finally:
            # Restaurar estado
            self.processing = False
            self.root.after(0, lambda: self.process_btn.state(['!disabled']))
            self.root.after(0, lambda: self.status_var.set("Listo para el próximo intercambio ✨"))
    
    def update_progress(self, value, text):
        """
        Actualiza la barra y el texto de progreso.
        
        Args:
            value (int): Valor del progreso (0-100).
            text (str): Texto descriptivo del progreso.
        """
        self.root.after(0, lambda: self.progress.config(value=value))
        self.root.after(0, lambda: self.progress_label.config(text=text))
        self.root.after(0, lambda: self.status_var.set(text))
    
    def show_image_on_canvas(self, image_path, canvas):
        """
        Muestra una imagen en un canvas, ajustando su tamaño.
        
        Args:
            image_path (str): Ruta de la imagen a mostrar.
            canvas: Canvas donde mostrar la imagen.
        """
        try:
            # Cargar imagen
            img = Image.open(image_path)
            
            # Obtener dimensiones del canvas
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            
            # Si el canvas aún no tiene tamaño definido, usar tamaño predeterminado
            if canvas_width <= 1:
                canvas_width = 300
            if canvas_height <= 1:
                canvas_height = 300
            
            # Calcular tamaño para ajustar al canvas manteniendo proporción
            img_width, img_height = img.size
            ratio = min(canvas_width / img_width, canvas_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            
            # Redimensionar imagen
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convertir a formato para Tkinter
            photo_img = ImageTk.PhotoImage(img)
            
            # Mostrar en canvas
            canvas.delete("all")
            
            # Crear un fondo para la imagen (mejora visual)
            canvas.create_rectangle(0, 0, canvas_width, canvas_height, 
                                   fill=self.colors["gray_light"], outline="")
            
            # Añadir un borde a la imagen
            border_width = 2
            canvas.create_rectangle(
                canvas_width//2 - new_width//2 - border_width,
                canvas_height//2 - new_height//2 - border_width,
                canvas_width//2 + new_width//2 + border_width,
                canvas_height//2 + new_height//2 + border_width,
                outline=self.colors["primary"], width=border_width
            )
            
            # Mostrar imagen
            canvas.create_image(canvas_width // 2, canvas_height // 2, 
                              anchor=tk.CENTER, image=photo_img)
            
            # Guardar referencia para evitar que sea eliminada por el recolector de basura
            if canvas == self.source_canvas:
                self.source_img = photo_img
            elif canvas == self.target_canvas:
                self.target_img = photo_img
            elif canvas == self.result_canvas:
                self.result_img = photo_img
        
        except Exception as e:
            self.logger.error(f"Error al mostrar imagen: {e}")
            canvas.delete("all")
            canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(), 
                                   fill=self.colors["gray_light"], outline="")
            canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2, 
                              text="Error al cargar imagen", fill=self.colors["accent"], 
                              font=("Segoe UI", 11, "bold"))
    
    def on_view_result(self):
        """
        Maneja la acción de ver el resultado en una aplicación externa.
        """
        if not self.result_img_path or not os.path.exists(self.result_img_path):
            messagebox.showinfo("Sin Resultado", 
                             "No hay resultado para mostrar.\n"
                             "Primero debe realizar un intercambio de rostros.")
            return
        
        try:
            # Abrir imagen con la aplicación predeterminada del sistema
            if os.name == 'nt':  # Windows
                os.startfile(self.result_img_path)
            elif os.name == 'posix':  # macOS, Linux
                subprocess.call(('xdg-open', self.result_img_path))
            
            self.status_var.set("Visualizando resultado en visor de imágenes.")
        except Exception as e:
            self.logger.error(f"Error al abrir imagen resultante: {e}")
            messagebox.showerror("Error", f"No se pudo abrir la imagen: {e}")
    
    def on_save_as(self):
        """
        Maneja la acción de guardar el resultado con otro nombre/ubicación.
        """
        if not self.result_img_path or not os.path.exists(self.result_img_path):
            messagebox.showinfo("Sin Resultado", 
                             "No hay resultado para guardar.\n"
                             "Primero debe realizar un intercambio de rostros.")
            return
        
        # Mostrar diálogo de guardar
        file_path = filedialog.asksaveasfilename(
            title="Guardar Resultado Como",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"), ("Todos los archivos", "*.*")],
            initialfile=os.path.basename(self.result_img_path)
        )
        
        if not file_path:
            return
        
        try:
            # Copiar archivo
            import shutil
            shutil.copy2(self.result_img_path, file_path)
            self.logger.info(f"Resultado guardado como: {file_path}")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Guardado Exitoso", 
                             f"Imagen guardada exitosamente como:\n{file_path}")
            
            self.status_var.set(f"Imagen guardada como: {os.path.basename(file_path)}")
        except Exception as e:
            self.logger.error(f"Error al guardar imagen: {e}")
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")
    
    def on_open_output_folder(self):
        """
        Maneja la acción de abrir la carpeta de salida.
        """
        try:
            # Verificar que la carpeta existe
            if not os.path.exists(self.app.output_dir):
                os.makedirs(self.app.output_dir)
            
            # Abrir carpeta de salida
            if os.name == 'nt':  # Windows
                os.startfile(self.app.output_dir)
            elif os.name == 'posix':  # macOS, Linux
                subprocess.call(('xdg-open', self.app.output_dir))
            
            self.status_var.set("Abriendo carpeta de resultados...")
        except Exception as e:
            self.logger.error(f"Error al abrir carpeta de salida: {e}")
            messagebox.showerror("Error", f"No se pudo abrir la carpeta: {e}")