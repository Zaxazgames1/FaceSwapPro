#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de instalación para FaceSwapPro.
Permite instalar la aplicación como un paquete.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="faceswappro",
    version="1.0.0",
    author="FaceSwapPro Team",
    author_email="johansebastianrojasramirez7@gmail.com",
    description="Aplicación avanzada para intercambio de rostros en imágenes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/usuario/FaceSwapPro",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "faceswappro=main:main",
        ],
    },
)