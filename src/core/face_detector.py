#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para la detección de rostros en imágenes.

Este módulo contiene la clase FaceDetector que se encarga de
detectar rostros en imágenes utilizando InsightFace.
"""

import logging
import insightface
from insightface.app import FaceAnalysis
import numpy as np
import cv2

class FaceDetector:
    """
    Clase para la detección de rostros en imágenes.
    
    Utiliza InsightFace para detectar rostros con alta precisión,
    incluyendo puntos de referencia faciales y atributos.
    """
    
    def __init__(self, det_size=(640, 640)):
        """
        Inicializa el detector de rostros.
        
        Args:
            det_size (tuple, opcional): Tamaño del detector. Por defecto es (640, 640).
        """
        self.logger = logging.getLogger('FaceSwapPro.FaceDetector')
        self.logger.info("Inicializando detector de rostros...")
        
        # Verificar versión de InsightFace
        assert insightface.__version__ >= '0.7', "Se requiere InsightFace versión 0.7 o superior"
        
        try:
            # Inicializar el detector de rostros de InsightFace
            self.app = FaceAnalysis(name='buffalo_l')
            self.app.prepare(ctx_id=0, det_size=det_size)
            self.logger.info("Detector de rostros inicializado correctamente")
        except Exception as e:
            self.logger.error(f"Error al inicializar el detector de rostros: {e}")
            raise
    
    def detect_faces(self, image):
        """
        Detecta rostros en una imagen.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            
        Returns:
            list: Lista de rostros detectados ordenados de izquierda a derecha.
                 Cada rostro contiene información como bbox, landmarks, etc.
        """
        if image is None:
            self.logger.error("No se proporcionó una imagen válida")
            return []
        
        try:
            # Detectar rostros con InsightFace
            faces = self.app.get(image)
            
            # Ordenar rostros de izquierda a derecha
            faces = sorted(faces, key=lambda x: x.bbox[0])
            
            self.logger.info(f"Se detectaron {len(faces)} rostros en la imagen")
            return faces
        
        except Exception as e:
            self.logger.error(f"Error al detectar rostros: {e}")
            return []
    
    def get_largest_face(self, faces):
        """
        Obtiene el rostro más grande de una lista de rostros.
        
        Args:
            faces (list): Lista de rostros detectados.
            
        Returns:
            object: El rostro más grande o None si no hay rostros.
        """
        if not faces:
            return None
        
        # Calcular el área de cada rostro y obtener el más grande
        largest_face = max(faces, key=lambda face: 
                          (face.bbox[2] - face.bbox[0]) * (face.bbox[3] - face.bbox[1]))
        
        return largest_face
    
    def draw_face_landmarks(self, image, face):
        """
        Dibuja los puntos de referencia faciales en una imagen.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV.
            face (object): Rostro detectado con InsightFace.
            
        Returns:
            numpy.ndarray: Imagen con los puntos de referencia dibujados.
        """
        img_with_landmarks = image.copy()
        
        # Dibujar caja delimitadora
        bbox = face.bbox.astype(np.int32)
        cv2.rectangle(img_with_landmarks, 
                     (bbox[0], bbox[1]), 
                     (bbox[2], bbox[3]), 
                     (0, 255, 0), 2)
        
        # Dibujar puntos de referencia faciales
        landmarks = face.landmark_2d_106
        if landmarks is not None:
            for point in landmarks.astype(np.int32):
                cv2.circle(img_with_landmarks, tuple(point), 1, (0, 0, 255), -1)
        
        return img_with_landmarks
    
    def crop_face(self, image, face, expand_ratio=1.5):
        """
        Recorta un rostro de una imagen con un margen adicional.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV.
            face (object): Rostro detectado con InsightFace.
            expand_ratio (float, opcional): Ratio para expandir el recorte. Por defecto es 1.5.
            
        Returns:
            numpy.ndarray: Imagen recortada con el rostro.
        """
        h, w = image.shape[:2]
        bbox = face.bbox.astype(np.int32)
        
        # Calcular centro y tamaño
        center_x = (bbox[0] + bbox[2]) // 2
        center_y = (bbox[1] + bbox[3]) // 2
        
        size_x = (bbox[2] - bbox[0]) * expand_ratio
        size_y = (bbox[3] - bbox[1]) * expand_ratio
        
        # Calcular coordenadas para recorte
        x1 = max(0, int(center_x - size_x / 2))
        y1 = max(0, int(center_y - size_y / 2))
        x2 = min(w, int(center_x + size_x / 2))
        y2 = min(h, int(center_y + size_y / 2))
        
        # Recortar imagen
        cropped = image[y1:y2, x1:x2]
        
        return cropped