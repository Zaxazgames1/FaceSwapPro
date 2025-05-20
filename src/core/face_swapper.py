#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo para el intercambio de rostros en imágenes.

Este módulo contiene la clase FaceSwapper que se encarga de
realizar el intercambio de rostros utilizando InsightFace.
"""

import logging
import os
import insightface
import cv2
import numpy as np

class FaceSwapper:
    """
    Clase para realizar el intercambio de rostros en imágenes.
    
    Utiliza el modelo InsightFace para intercambiar rostros
    entre imágenes con alta calidad y precisión.
    """
    
    def __init__(self, model_path):
        """
        Inicializa el intercambiador de rostros.
        
        Args:
            model_path (str): Ruta al modelo de intercambio de rostros (ONNX).
        """
        self.logger = logging.getLogger('FaceSwapPro.FaceSwapper')
        self.logger.info("Inicializando intercambiador de rostros...")
        
        if not os.path.exists(model_path):
            self.logger.error(f"No se encontró el modelo en: {model_path}")
            raise FileNotFoundError(f"No se encontró el modelo en: {model_path}")
        
        try:
            # Cargar el modelo de intercambio de rostros
            self.swapper = insightface.model_zoo.get_model(model_path)
            self.logger.info("Modelo de intercambio cargado correctamente")
        except Exception as e:
            self.logger.error(f"Error al cargar el modelo de intercambio: {e}")
            raise
    
    def swap_face(self, target_img, target_face, source_img, source_face):
        """
        Intercambia un rostro de la imagen fuente a la imagen objetivo.
        
        Args:
            target_img (numpy.ndarray): Imagen objetivo donde se colocará el rostro.
            target_face (object): Rostro detectado en la imagen objetivo.
            source_img (numpy.ndarray): Imagen fuente de donde se tomará el rostro.
            source_face (object): Rostro detectado en la imagen fuente.
            
        Returns:
            numpy.ndarray: Imagen resultante con el rostro intercambiado.
        """
        try:
            # Realizar intercambio de rostros
            self.logger.info("Realizando intercambio de rostros...")
            result = target_img.copy()
            result = self.swapper.get(result, target_face, source_face, paste_back=True)
            
            self.logger.info("Intercambio de rostros completado exitosamente")
            return result
        
        except Exception as e:
            self.logger.error(f"Error al intercambiar rostros: {e}")
            return target_img.copy()  # Devolver imagen original en caso de error
    
    def swap_multiple_faces(self, target_img, target_faces, source_img, source_face):
        """
        Intercambia un rostro de la imagen fuente a múltiples rostros en la imagen objetivo.
        
        Args:
            target_img (numpy.ndarray): Imagen objetivo donde se colocarán los rostros.
            target_faces (list): Lista de rostros detectados en la imagen objetivo.
            source_img (numpy.ndarray): Imagen fuente de donde se tomará el rostro.
            source_face (object): Rostro detectado en la imagen fuente.
            
        Returns:
            numpy.ndarray: Imagen resultante con los rostros intercambiados.
        """
        try:
            # Realizar intercambio de rostros para cada rostro detectado
            self.logger.info(f"Realizando intercambio de {len(target_faces)} rostros...")
            result = target_img.copy()
            
            for face in target_faces:
                result = self.swapper.get(result, face, source_face, paste_back=True)
            
            self.logger.info("Intercambio de múltiples rostros completado exitosamente")
            return result
        
        except Exception as e:
            self.logger.error(f"Error al intercambiar múltiples rostros: {e}")
            return target_img.copy()  # Devolver imagen original en caso de error
    
    def adjust_face_boundary(self, result, target_img, face_bbox, blend_ratio=0.5):
        """
        Ajusta los bordes del rostro intercambiado para una mejor fusión.
        
        Args:
            result (numpy.ndarray): Imagen con el rostro intercambiado.
            target_img (numpy.ndarray): Imagen objetivo original.
            face_bbox (numpy.ndarray): Caja delimitadora del rostro.
            blend_ratio (float, opcional): Ratio de fusión. Por defecto es 0.5.
            
        Returns:
            numpy.ndarray: Imagen con los bordes del rostro ajustados.
        """
        # Convertir bbox a enteros
        x1, y1, x2, y2 = [int(coord) for coord in face_bbox]
        
        # Crear una máscara para la región del rostro
        mask = np.zeros_like(result, dtype=np.float32)
        cv2.rectangle(mask, (x1, y1), (x2, y2), (1, 1, 1), -1)
        
        # Difuminar la máscara para una transición suave
        mask = cv2.GaussianBlur(mask, (25, 25), 0)
        
        # Combinar la imagen original y el resultado usando la máscara
        blended = cv2.addWeighted(
            result.astype(np.float32), blend_ratio,
            target_img.astype(np.float32), 1 - blend_ratio,
            0
        )
        
        # Aplicar la máscara
        final_result = result.copy()
        final_result = result * mask + target_img * (1 - mask)
        
        return final_result.astype(np.uint8)