#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de línea de comandos para FaceSwapPro.

Este script permite utilizar las funcionalidades de FaceSwapPro
sin necesidad de la interfaz gráfica, desde la línea de comandos.
"""

import argparse
import os
import sys
import logging
from src import FaceSwapApp

def parse_arguments():
    """
    Analiza los argumentos de línea de comandos.
    
    Returns:
        argparse.Namespace: Objeto con los argumentos analizados.
    """
    parser = argparse.ArgumentParser(
        description="FaceSwapPro - Intercambio de rostros en línea de comandos",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('-s', '--source', required=True,
                       help='Ruta a la imagen fuente (rostro a usar)')
    
    parser.add_argument('-t', '--target', required=True,
                       help='Ruta a la imagen objetivo (donde poner el rostro)')
    
    parser.add_argument('-o', '--output',
                       help='Ruta para guardar la imagen resultante')
    
    parser.add_argument('-q', '--quality', type=int, choices=[1, 2, 3], default=2,
                       help='Nivel de calidad: 1=Básico, 2=HD, 3=Ultra HD')
    
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Mostrar información detallada del proceso')
    
    return parser.parse_args()

def setup_logging(verbose):
    """
    Configura el nivel de logging según la verbosidad.
    
    Args:
        verbose (bool): Si es True, se muestra información detallada.
    """
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """
    Función principal del script de línea de comandos.
    """
    # Analizar argumentos
    args = parse_arguments()
    
    # Configurar logging
    setup_logging(args.verbose)
    logger = logging.getLogger('FaceSwapProCLI')
    
    # Comprobar que las imágenes existen
    if not os.path.exists(args.source):
        logger.error(f"No se encuentra la imagen fuente: {args.source}")
        return 1
    
    if not os.path.exists(args.target):
        logger.error(f"No se encuentra la imagen objetivo: {args.target}")
        return 1
    
    # Configurar rutas
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
    try:
        logger.info("Iniciando FaceSwapPro en modo línea de comandos...")
        app = FaceSwapApp(model_path, data_dir, output_dir)
        
        # Verificar que el modelo esté disponible
        if not app.verify_model():
            logger.error("No se pudo verificar o descargar el modelo necesario.")
            return 1
        
        # Procesar intercambio de rostros
        logger.info(f"Procesando intercambio con calidad {args.quality}...")
        result_path = app.process_face_swap(args.source, args.target, args.quality)
        
        if not result_path:
            logger.error("No se pudo completar el intercambio de rostros.")
            return 1
        
        # Si se especificó una ruta de salida, copiar el resultado
        if args.output:
            import shutil
            try:
                shutil.copy2(result_path, args.output)
                logger.info(f"Resultado guardado en: {args.output}")
            except Exception as e:
                logger.error(f"Error al guardar resultado: {e}")
                return 1
        else:
            logger.info(f"Resultado guardado en: {result_path}")
        
        logger.info("Procesamiento completado con éxito.")
        return 0
    
    except Exception as e:
        logger.error(f"Error durante la ejecución: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())