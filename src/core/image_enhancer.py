#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para la mejora de calidad de imágenes.

Este módulo contiene la clase ImageEnhancer que se encarga de
mejorar la calidad de las imágenes y rostros intercambiados
utilizando diversas técnicas de procesamiento de imágenes.
"""

import logging
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

class ImageEnhancer:
    """
    Clase para mejorar la calidad de imágenes y rostros intercambiados.
    
    Utiliza diversas técnicas de procesamiento de imágenes para mejorar
    la calidad y el realismo de los rostros intercambiados.
    """
    
    def __init__(self):
        """
        Inicializa el mejorador de imágenes.
        """
        self.logger = logging.getLogger('FaceSwapPro.ImageEnhancer')
        self.logger.info("Inicializando mejorador de imágenes...")
        
        # Cargar clasificador de rostros para mejoras específicas
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.logger.info("Mejorador de imágenes inicializado correctamente")
        except Exception as e:
            self.logger.error(f"Error al cargar el clasificador de rostros: {e}")
            raise
    
    def enhance_basic(self, image):
        """
        Aplica mejoras básicas a la imagen.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            
        Returns:
            numpy.ndarray: Imagen mejorada.
        """
        self.logger.info("Aplicando mejoras básicas a la imagen...")
        
        # Convertir a RGB para PIL
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        # Mejorar nitidez
        enhancer = ImageEnhance.Sharpness(pil_img)
        pil_img = enhancer.enhance(1.3)
        
        # Mejorar contraste
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(1.1)
        
        # Mejorar color
        enhancer = ImageEnhance.Color(pil_img)
        pil_img = enhancer.enhance(1.1)
        
        # Convertir de vuelta a BGR para OpenCV
        enhanced_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        return enhanced_img
    
    def enhance_skin(self, image):
        """
        Mejora específicamente la textura de la piel.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            
        Returns:
            numpy.ndarray: Imagen con piel mejorada.
        """
        self.logger.info("Mejorando textura de piel...")
        
        # Detectar rostros
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return image
        
        result = image.copy()
        
        for (x, y, w, h) in faces:
            # Extraer región del rostro
            face_roi = result[y:y+h, x:x+w]
            
            # Aplicar filtro bilateral para suavizar la piel preservando bordes
            face_roi = cv2.bilateralFilter(face_roi, 9, 75, 75)
            
            # Aplicar suavizado gaussiano ligero
            face_roi = cv2.GaussianBlur(face_roi, (5, 5), 0)
            
            # Aplicar filtro de mejora de detalles
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            face_roi = cv2.filter2D(face_roi, -1, kernel)
            
            # Colocar el rostro mejorado de vuelta en la imagen
            result[y:y+h, x:x+w] = face_roi
        
        return result
    
    def enhance_facial_features(self, image):
        """
        Mejora características faciales específicas como ojos y labios.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            
        Returns:
            numpy.ndarray: Imagen con características faciales mejoradas.
        """
        self.logger.info("Mejorando características faciales...")
        
        # Detectar rostros
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return image
        
        # Convertir a HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Asegurarse que los canales son del tipo correcto
        h = h.astype(np.uint8)
        s = s.astype(np.uint8)
        v = v.astype(np.uint8)
        
        # Para cada rostro
        for (x, y, w, h_height) in faces:
            # Aproximar región de ojos (parte superior del rostro)
            eye_y = y + int(h_height * 0.2)
            eye_h = int(h_height * 0.25)
            
            # Aproximar región de labios (parte inferior del rostro)
            lip_y = y + int(h_height * 0.6)
            lip_h = int(h_height * 0.25)
            
            # Asegurarse de que las regiones están dentro de los límites de la imagen
            eye_y = max(0, min(eye_y, s.shape[0] - 1))
            eye_h = max(1, min(eye_h, s.shape[0] - eye_y))
            lip_y = max(0, min(lip_y, s.shape[0] - 1))
            lip_h = max(1, min(lip_h, s.shape[0] - lip_y))
            
            if eye_y + eye_h <= s.shape[0] and x + w <= s.shape[1]:
                # Aumentar saturación en ojos
                eye_region = s[eye_y:eye_y+eye_h, x:x+w].copy()
                eye_region = np.clip(eye_region.astype(np.int16) + 10, 0, 255).astype(np.uint8)
                s[eye_y:eye_y+eye_h, x:x+w] = eye_region
            
            if lip_y + lip_h <= s.shape[0] and x + w <= s.shape[1]:
                # Aumentar saturación en labios
                lip_region = s[lip_y:lip_y+lip_h, x:x+w].copy()
                lip_region = np.clip(lip_region.astype(np.int16) + 20, 0, 255).astype(np.uint8)
                s[lip_y:lip_y+lip_h, x:x+w] = lip_region
        
        # Unir canales y convertir de vuelta a BGR
        hsv_realzado = cv2.merge([h, s, v])
        imagen_realzada = cv2.cvtColor(hsv_realzado, cv2.COLOR_HSV2BGR)
        
        return imagen_realzada
    
    def enhance_color_correction(self, result_img, target_img, source_img):
        """
        Aplica corrección de color para hacer que el resultado combine mejor.
        
        Args:
            result_img (numpy.ndarray): Imagen resultado del intercambio.
            target_img (numpy.ndarray): Imagen objetivo original.
            source_img (numpy.ndarray): Imagen fuente original.
            
        Returns:
            numpy.ndarray: Imagen con colores corregidos.
        """
        self.logger.info("Aplicando corrección de color...")
        
        # Obtener la media de color de las imágenes
        mean_origen = cv2.mean(source_img)[:3]
        mean_destino = cv2.mean(target_img)[:3]
        
        # Calcular factores de corrección
        ratios = [d/o if o > 0 else 1.0 for o, d in zip(mean_origen, mean_destino)]
        
        # Aplicar corrección de color
        canales = cv2.split(result_img)
        canales_corregidos = []
        
        for i, canal in enumerate(canales[:3]):
            corregido = canal * (ratios[i] * 0.7 + 0.3)  # Mezcla para no sobrecorregir
            corregido = np.clip(corregido, 0, 255).astype(np.uint8)
            canales_corregidos.append(corregido)
        
        if len(canales) > 3:  # Si hay canal alfa
            canales_corregidos.append(canales[3])
        
        resultado_corregido = cv2.merge(canales_corregidos)
        return resultado_corregido
    
    def enhance_hdr_effect(self, image):
        """
        Aplica un efecto HDR a la imagen para mayor detalle y viveza.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            
        Returns:
            numpy.ndarray: Imagen con efecto HDR.
        """
        self.logger.info("Aplicando efecto HDR...")
        
        # Convertir a espacio de color LAB para manipular contraste sin afectar color
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Fusionar canales nuevamente
        lab = cv2.merge((l, a, b))
        
        # Convertir de vuelta a BGR
        imagen_hdr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # Aumentar saturación y detalles
        hsv = cv2.cvtColor(imagen_hdr, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = cv2.add(s, 10)  # Aumentar saturación
        hsv = cv2.merge((h, s, v))
        imagen_hdr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return imagen_hdr
    
    def apply_all_enhancements(self, image, level=3):
        """
        Aplica todas las mejoras disponibles según el nivel especificado.
        
        Args:
            image (numpy.ndarray): Imagen en formato OpenCV (BGR).
            level (int, opcional): Nivel de mejora (1-3). Por defecto es 3.
            
        Returns:
            numpy.ndarray: Imagen mejorada.
        """
        self.logger.info(f"Aplicando todas las mejoras (nivel {level})...")
        
        result = image.copy()
        
        # Nivel 1: Mejoras básicas
        result = self.enhance_basic(result)
        
        if level >= 2:
            # Nivel 2: Mejoras de piel y características faciales
            result = self.enhance_skin(result)
            result = self.enhance_facial_features(result)
        
        if level >= 3:
            # Nivel 3: Efecto HDR
            result = self.enhance_hdr_effect(result)
        
        return result