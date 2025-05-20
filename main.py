#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FaceSwapPro - Aplicación avanzada de intercambio de rostros

Este script inicia la aplicación FaceSwapPro, que permite realizar intercambios
de rostros entre imágenes con calidad profesional utilizando modelos de IA
y técnicas avanzadas de procesamiento de imágenes.
"""

import os
import sys
from src import FaceSwapApp

def main():
    """
    Función principal que inicia la aplicación FaceSwapPro.
    """
    # Configuración de rutas
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    data_dir = os.path.join(base_dir, "data")
    output_dir = os.path.join(base_dir, "output")
    
    # Crear directorios si no existen
    for directory in [models_dir, data_dir, output_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Modelo a utilizar
    model_path = os.path.join(models_dir, "inswapper_128.onnx")
    
    # Iniciar aplicación
    app = FaceSwapApp(model_path, data_dir, output_dir)
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)