#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para crear un ejecutable de FaceSwapPro utilizando PyInstaller.

Este script crea un ejecutable independiente que puede
distribuirse sin necesidad de instalar Python.
"""

import os
import sys
import shutil
import subprocess

def main():
    """
    Función principal para crear el ejecutable.
    """
    print("=== Creando ejecutable de FaceSwapPro ===")
    
    # Verificar que PyInstaller está instalado
    try:
        import PyInstaller
        print("PyInstaller encontrado.")
    except ImportError:
        print("PyInstaller no encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=5.13.0"])
    
    # Verificar dependencias
    print("Verificando dependencias...")
    try:
        # Primero intentamos instalar las dependencias de desarrollo
        if os.path.exists("requirements-dev.txt"):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"])
        else:
            print("Archivo requirements-dev.txt no encontrado, instalando solo las dependencias básicas.")
    except subprocess.CalledProcessError:
        print("No se pudieron instalar las dependencias de desarrollo. Continuando...")
    
    # Instalamos las dependencias básicas (necesarias para la aplicación)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Limpiar directorio dist si existe
    if os.path.exists("dist"):
        print("Limpiando directorio dist anterior...")
        shutil.rmtree("dist")
    
    # Crear carpetas para modelos y datos vacías en el directorio dist
    os.makedirs("dist/FaceSwapPro/models", exist_ok=True)
    os.makedirs("dist/FaceSwapPro/data", exist_ok=True)
    os.makedirs("dist/FaceSwapPro/output", exist_ok=True)
    
    # Copiar archivos README, LICENSE, etc.
    print("Copiando archivos de documentación...")
    for file in ["README.md", "LICENSE", "requirements.txt"]:
        if os.path.exists(file):
            shutil.copy2(file, f"dist/FaceSwapPro/{file}")
    
    # Crear el ejecutable con PyInstaller
    print("Creando ejecutable...")
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=FaceSwapPro",
        "--onedir",
        "--windowed",
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",
        "--add-data=src;src",
        "--hidden-import=insightface",
        "--hidden-import=onnxruntime",
        "main.py"
    ]
    
    # Eliminar argumentos vacíos
    pyinstaller_cmd = [arg for arg in pyinstaller_cmd if arg]
    
    subprocess.check_call(pyinstaller_cmd)
    
    print("\n=== Ejecutable creado exitosamente ===")
    print(f"El ejecutable se encuentra en: {os.path.abspath('dist/FaceSwapPro/FaceSwapPro.exe')}")
    print("\nPara distribuir la aplicación, comprime la carpeta dist/FaceSwapPro")

if __name__ == "__main__":
    main()