#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo principal de la aplicación FaceSwapPro.

Este módulo contiene la clase principal que coordina todas las funcionalidades
de la aplicación, incluyendo la detección de rostros, el intercambio de caras
y la mejora de imágenes.
"""

import os
import cv2
import time
import logging
from .core import FaceDetector, FaceSwapper, ImageEnhancer
from .gui import AppWindow
from .utils import ImageUtils

class FaceSwapApp:
    """
    Clase principal que coordina todas las funcionalidades de FaceSwapPro.
    
    Esta clase integra los diferentes componentes de la aplicación como
    detección de rostros, intercambio de caras, mejora de imágenes y la
    interfaz gráfica.
    """
    
    def __init__(self, model_path, data_dir, output_dir):
        """
        Inicializa la aplicación FaceSwapPro.
        
        Args:
            model_path (str): Ruta al modelo de intercambio de rostros.
            data_dir (str): Directorio donde se encuentran las imágenes.
            output_dir (str): Directorio donde se guardarán los resultados.
        """
        self.model_path = model_path
        self.data_dir = data_dir
        self.output_dir = output_dir
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('FaceSwapPro')
        
        # Inicializar componentes
        self.initialize_components()
        
        # Crear ventana de la aplicación
        self.app_window = AppWindow(self)
    
    def initialize_components(self):
        """
        Inicializa los componentes principales de la aplicación.
        """
        self.logger.info("Inicializando componentes de la aplicación...")
        
        # Verificar si el modelo existe
        if not os.path.exists(self.model_path):
            self.logger.error(f"No se encontró el modelo en: {self.model_path}")
            raise FileNotFoundError(f"No se encontró el modelo en: {self.model_path}")
        
        try:
            # Inicializar detector de rostros
            self.face_detector = FaceDetector()
            
            # Inicializar intercambiador de rostros
            self.face_swapper = FaceSwapper(self.model_path)
            
            # Inicializar mejorador de imágenes
            self.image_enhancer = ImageEnhancer()
            
            # Inicializar utilidades de imagen
            self.image_utils = ImageUtils()
            
            self.logger.info("Componentes inicializados correctamente")
        except Exception as e:
            self.logger.error(f"Error al inicializar componentes: {e}")
            raise
    
    def get_available_images(self):
        """
        Obtiene las imágenes disponibles en el directorio de datos.
        
        Returns:
            list: Lista de nombres de archivos de imágenes.
        """
        if not os.path.exists(self.data_dir):
            self.logger.warning(f"El directorio {self.data_dir} no existe. Creándolo...")
            os.makedirs(self.data_dir)
            return []
        
        image_files = [f for f in os.listdir(self.data_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        return image_files
    
    def process_face_swap(self, source_img_path, target_img_path, quality_level=2):
        """
        Procesa el intercambio de rostros entre dos imágenes.
        
        Args:
            source_img_path (str): Ruta a la imagen fuente (rostro a usar).
            target_img_path (str): Ruta a la imagen objetivo (donde poner el rostro).
            quality_level (int, opcional): Nivel de calidad del resultado (1-3).
            
        Returns:
            str: Ruta del archivo de resultado o None si ocurre un error.
        """
        try:
            self.logger.info(f"Iniciando intercambio de rostros con nivel de calidad {quality_level}")
            start_time = time.time()
            
            # Cargar imágenes
            source_img = cv2.imread(source_img_path)
            target_img = cv2.imread(target_img_path)
            
            if source_img is None or target_img is None:
                self.logger.error("No se pudieron cargar las imágenes")
                return None
            
            # Detectar rostros
            source_faces = self.face_detector.detect_faces(source_img)
            target_faces = self.face_detector.detect_faces(target_img)
            
            if not source_faces or not target_faces:
                self.logger.error("No se detectaron rostros en las imágenes")
                return None
            
            # Realizar intercambio de rostros
            result_img = self.face_swapper.swap_face(
                target_img, 
                target_faces[0], 
                source_img, 
                source_faces[0]
            )
            
            # Aplicar mejoras según el nivel de calidad
            if quality_level >= 1:
                result_img = self.image_enhancer.enhance_basic(result_img)
            
            if quality_level >= 2:
                result_img = self.image_enhancer.enhance_skin(result_img)
                result_img = self.image_enhancer.enhance_facial_features(result_img)
            
            if quality_level >= 3:
                result_img = self.image_enhancer.enhance_color_correction(
                    result_img, target_img, source_img
                )
                result_img = self.image_enhancer.enhance_hdr_effect(result_img)
            
            # Crear nombre del archivo de resultado
            source_name = os.path.splitext(os.path.basename(source_img_path))[0]
            target_name = os.path.splitext(os.path.basename(target_img_path))[0]
            quality_suffix = ["BASICO", "HD", "ULTRA_HD"][quality_level - 1]
            
            result_filename = f"{quality_suffix}_{target_name}_con_rostro_de_{source_name}.png"
            result_path = os.path.join(self.output_dir, result_filename)
            
            # Guardar resultado
            cv2.imwrite(result_path, result_img)
            
            elapsed_time = time.time() - start_time
            self.logger.info(f"Proceso completado en {elapsed_time:.2f} segundos")
            
            return result_path
        
        except Exception as e:
            self.logger.error(f"Error en el proceso de intercambio de rostros: {e}")
            return None
    
    def verify_model(self):
        """
        Verifica si el modelo necesario está disponible y lo descarga si es necesario.
        
        Returns:
            bool: True si el modelo está disponible, False en caso contrario.
        """
        if os.path.exists(self.model_path):
            return True
        
        from urllib import request
        import ssl
        
        try:
            self.logger.info(f"Descargando modelo desde Hugging Face...")
            
            # Crear directorio para el modelo si no existe
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            
            # Configurar contexto SSL para evitar errores de certificado
            ssl_context = ssl._create_unverified_context()
            
            # URL del modelo en Hugging Face
            model_url = "https://huggingface.co/hacksider/inswapper_128/resolve/main/inswapper_128.onnx"
            
            # Descargar modelo
            with request.urlopen(model_url, context=ssl_context) as response:
                with open(self.model_path, 'wb') as f:
                    f.write(response.read())
            
            self.logger.info(f"Modelo descargado correctamente en: {self.model_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error al descargar el modelo: {e}")
            return False
    
    def run(self):
        """
        Ejecuta la aplicación FaceSwapPro.
        """
        # Verificar que el modelo esté disponible
        if not self.verify_model():
            self.logger.error("No se pudo verificar o descargar el modelo necesario.")
            return
        
        # Ejecutar la interfaz gráfica
        self.app_window.run()