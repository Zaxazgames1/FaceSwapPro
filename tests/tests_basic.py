#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas unitarias para FaceSwapPro.

Este módulo contiene pruebas básicas para verificar
el funcionamiento correcto de los componentes principales.
"""

import unittest
import os
import sys
import logging
import cv2
import numpy as np

# Añadir directorio raíz al path para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import FaceDetector
from src.utils import ImageUtils

# Desactivar logging durante las pruebas
logging.disable(logging.CRITICAL)

class TestFaceDetector(unittest.TestCase):
    """
    Pruebas unitarias para el detector de rostros.
    """
    
    def setUp(self):
        """
        Prepara el entorno para las pruebas.
        """
        self.detector = FaceDetector()
        
        # Crear una imagen sintética con un "rostro" (un círculo)
        self.test_img = np.ones((300, 300, 3), dtype=np.uint8) * 255
        cv2.circle(self.test_img, (150, 150), 100, (0, 0, 0), -1)
        cv2.circle(self.test_img, (120, 120), 15, (255, 255, 255), -1)  # Ojo izquierdo
        cv2.circle(self.test_img, (180, 120), 15, (255, 255, 255), -1)  # Ojo derecho
        cv2.ellipse(self.test_img, (150, 180), (50, 20), 0, 0, 180, (255, 255, 255), -1)  # Boca
    
    def test_init(self):
        """
        Prueba que el detector se inicialice correctamente.
        """
        self.assertIsNotNone(self.detector.app)
    
    def test_detect_faces_empty(self):
        """
        Prueba la detección en una imagen vacía.
        """
        empty_img = np.ones((100, 100, 3), dtype=np.uint8) * 255
        faces = self.detector.detect_faces(empty_img)
        self.assertEqual(len(faces), 0)
    
    def test_crop_face(self):
        """
        Prueba la funcionalidad de recortar un rostro.
        """
        # Esta prueba solo verifica que la función no falle
        # No podemos usar detect_faces con la imagen sintética porque InsightFace
        # requiere rostros realistas, pero podemos simular un objeto "face" con la información necesaria
        
        class MockFace:
            def __init__(self):
                self.bbox = np.array([50, 50, 250, 250])  # x1, y1, x2, y2
        
        mock_face = MockFace()
        cropped = self.detector.crop_face(self.test_img, mock_face)
        
        # Verificar que el recorte tiene el tamaño esperado
        # Con un factor de expansión de 1.5, el recorte debería ser más grande que el bbox original
        self.assertGreater(cropped.shape[0], 200)  # height
        self.assertGreater(cropped.shape[1], 200)  # width

class TestImageUtils(unittest.TestCase):
    """
    Pruebas unitarias para las utilidades de imagen.
    """
    
    def setUp(self):
        """
        Prepara el entorno para las pruebas.
        """
        self.utils = ImageUtils()
        
        # Crear una imagen de prueba
        self.test_img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    
    def test_resize_image(self):
        """
        Prueba el redimensionamiento de imágenes.
        """
        # Crear una imagen grande
        large_img = np.ones((2000, 1000, 3), dtype=np.uint8) * 255
        
        # Redimensionar con tamaño máximo
        resized = self.utils.resize_image(large_img, max_size=800)
        
        # Verificar que el lado más grande no supera max_size
        self.assertLessEqual(max(resized.shape[0], resized.shape[1]), 800)
        
        # Verificar que se mantiene la relación de aspecto
        original_ratio = large_img.shape[0] / large_img.shape[1]
        resized_ratio = resized.shape[0] / resized.shape[1]
        self.assertAlmostEqual(original_ratio, resized_ratio, places=2)
    
    def test_convert_to_pil_and_back(self):
        """
        Prueba la conversión entre OpenCV y PIL.
        """
        # Dibujar algo en la imagen para asegurar que los datos cambian
        cv2.rectangle(self.test_img, (10, 10), (90, 90), (0, 0, 255), -1)
        
        # Convertir a PIL
        pil_img = self.utils.convert_to_pil(self.test_img)
        
        # Convertir de vuelta a OpenCV
        cv_img = self.utils.convert_to_cv(pil_img)
        
        # Verificar que las dimensiones se mantienen
        self.assertEqual(self.test_img.shape, cv_img.shape)
        
        # Verificar que los datos son similares (puede haber pequeñas diferencias por la conversión)
        diff = np.sum(np.abs(self.test_img.astype(int) - cv_img.astype(int)))
        avg_diff = diff / (self.test_img.size)
        self.assertLessEqual(avg_diff, 1.0)  # Diferencia promedio menor a 1

if __name__ == '__main__':
    unittest.main()