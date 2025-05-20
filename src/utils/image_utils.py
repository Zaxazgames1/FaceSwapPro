#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de utilidades para el procesamiento de imágenes.

Este módulo contiene la clase ImageUtils que proporciona funciones
auxiliares para el procesamiento y manipulación de imágenes.
"""

import logging
import os
import cv2
import numpy as np
from PIL import Image

class ImageUtils:
    """
    Clase de utilidades para el procesamiento de imágenes.
    
    Proporciona funciones auxiliares para manipular imágenes,
    como redimensionamiento, conversión, carga y guardado.
    """
    
    def __init__(self):
        """
        Inicializa la clase de utilidades de imagen.
        """
        self.logger = logging.getLogger('FaceSwapPro.ImageUtils')
        self.logger.info("Inicializando utilidades de imagen...")
    
    def load_image(self, image_path):
        """
        Carga una imagen desde una ruta de archivo.
        
        Args:
            image_path (str): Ruta al archivo de imagen.
            
        Returns:
            numpy.ndarray: Imagen cargada en formato OpenCV (BGR) o None si hay error.
        """
        if not os.path.exists(image_path):
            self.logger.error(f"No se encontró la imagen en: {image_path}")
            return None
        
        try:
            image = cv2.imread(image_path)
            
            if image is None:
                self.logger.error(f"No se pudo cargar la imagen: {image_path}")
                return None
            
            self.logger.info(f"Imagen cargada correctamente: {image_path}")
            return image
        
        except Exception as e:
            self.logger.error(f"Error al cargar la imagen: {e}")
            return None
    
    def save_image(self, image, output_path, quality=95):
        """
        Guarda una imagen en un archivo.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            output_path (str): Ruta donde guardar la imagen.
            quality (int, opcional): Calidad de la imagen (0-100). Por defecto es 95.
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Determinar formato según la extensión
            ext = os.path.splitext(output_path)[1].lower()
            
            if ext == '.jpg' or ext == '.jpeg':
                # Guardar como JPEG
                cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            elif ext == '.png':
                # Guardar como PNG
                cv2.imwrite(output_path, image, [cv2.IMWRITE_PNG_COMPRESSION, min(9, 100 - quality // 10)])
            else:
                # Guardar con configuración predeterminada
                cv2.imwrite(output_path, image)
            
            self.logger.info(f"Imagen guardada correctamente en: {output_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error al guardar la imagen: {e}")
            return False
    
    def resize_image(self, image, max_size=1920):
        """
        Redimensiona una imagen manteniendo su relación de aspecto.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            max_size (int, opcional): Tamaño máximo (ancho o alto). Por defecto es 1920.
            
        Returns:
            numpy.ndarray: Imagen redimensionada.
        """
        # Obtener dimensiones actuales
        height, width = image.shape[:2]
        
        # Determinar factor de escala
        scale = 1.0
        if height > max_size or width > max_size:
            scale = min(max_size / height, max_size / width)
        
        # Calcular nuevas dimensiones
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Redimensionar imagen
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
        
        return resized
    
    def convert_to_pil(self, cv_image):
        """
        Convierte una imagen de OpenCV a formato PIL.
        
        Args:
            cv_image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            
        Returns:
            PIL.Image: Imagen en formato PIL (RGB).
        """
        # Convertir de BGR a RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        
        # Convertir a formato PIL
        pil_image = Image.fromarray(rgb_image)
        
        return pil_image
    
    def convert_to_cv(self, pil_image):
        """
        Convierte una imagen de PIL a formato OpenCV.
        
        Args:
            pil_image (PIL.Image): Imagen en formato PIL.
            
        Returns:
            numpy.ndarray: Imagen en formato OpenCV (BGR).
        """
        # Convertir de PIL a numpy array (RGB)
        rgb_image = np.array(pil_image)
        
        # Convertir de RGB a BGR
        cv_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        
        return cv_image
    
    def apply_watermark(self, image, text="FaceSwapPro"):
        """
        Aplica una marca de agua de texto a una imagen.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            text (str, opcional): Texto de la marca de agua. Por defecto es "FaceSwapPro".
            
        Returns:
            numpy.ndarray: Imagen con marca de agua.
        """
        result = image.copy()
        
        # Obtener dimensiones de la imagen
        h, w = result.shape[:2]
        
        # Configurar fuente
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = w / 1500.0  # Escalar según tamaño de imagen
        font_thickness = max(1, int(w / 1000.0))
        
        # Obtener tamaño del texto
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        
        # Posición del texto (esquina inferior derecha)
        text_x = w - text_size[0] - 10
        text_y = h - 10
        
        # Dibujar texto con sombra
        cv2.putText(result, text, (text_x + 2, text_y + 2), font, font_scale,
                   (0, 0, 0, 128), font_thickness, cv2.LINE_AA)
        cv2.putText(result, text, (text_x, text_y), font, font_scale,
                   (255, 255, 255, 200), font_thickness, cv2.LINE_AA)
        
        return result
    
    def create_comparison_image(self, original, result):
        """
        Crea una imagen de comparación lado a lado.
        
        Args:
            original (numpy.ndarray): Imagen original.
            result (numpy.ndarray): Imagen resultante.
            
        Returns:
            numpy.ndarray: Imagen de comparación.
        """
        # Redimensionar imágenes al mismo tamaño
        h1, w1 = original.shape[:2]
        h2, w2 = result.shape[:2]
        
        h = max(h1, h2)
        w = w1 + w2
        
        # Crear imagen combinada
        comparison = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Colocar imágenes
        comparison[:h1, :w1] = original
        comparison[:h2, w1:w1+w2] = result
        
        # Dibujar línea separadora
        cv2.line(comparison, (w1, 0), (w1, h), (0, 0, 255), 2)
        
        # Añadir etiquetas
        cv2.putText(comparison, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(comparison, "Resultado", (w1 + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 255, 0), 2, cv2.LINE_AA)
        
        return comparison