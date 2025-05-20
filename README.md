# FaceSwapPro

![FaceSwapPro Logo](https://i.imgur.com/placeholder-logo.png)

FaceSwapPro es una aplicación avanzada para intercambio de rostros en imágenes, desarrollada con Python y tecnología de inteligencia artificial. Utilizando el modelo InsightFace, permite intercambiar rostros con resultados ultra-realistas y ofrece diferentes niveles de calidad para adaptarse a diversas necesidades.

## Características

- ✅ **Interfaz gráfica intuitiva**: Fácil de usar para usuarios sin conocimientos técnicos
- ✅ **Alta calidad de intercambio**: Resultados realistas con preservación de detalles faciales
- ✅ **Múltiples niveles de calidad**: Desde procesamiento básico rápido hasta ultra HD
- ✅ **Mejoras avanzadas de imagen**: Incluye corrección de color, mejora de piel y efectos HDR
- ✅ **100% local**: Todo el procesamiento se realiza en tu computadora, sin envío de datos

## Requisitos del sistema

- Python 3.7 o superior
- Windows, macOS o Linux
- Mínimo 4GB de RAM (8GB recomendado para calidad Ultra HD)
- Espacio en disco: 2GB mínimo

## Instalación

### 1. Clonar o descargar el repositorio

```
git clone https://github.com/usuario/FaceSwapPro.git
cd FaceSwapPro
```

O simplemente descarga y descomprime el archivo ZIP.

### 2. Instalar dependencias

Para usuarios regulares:
```
pip install -r requirements.txt
```

Para desarrolladores (incluye herramientas de desarrollo):
```
pip install -r requirements.txt -r requirements-dev.txt
```

### 3. Ejecutar la aplicación

```
python main.py
```

La primera vez que ejecutes la aplicación, se descargará automáticamente el modelo necesario.

## Uso

1. **Iniciar la aplicación** ejecutando `python main.py`
2. **Seleccionar imágenes**: 
   - Imagen fuente (de donde se tomará el rostro)
   - Imagen objetivo (donde se colocará el rostro)
3. **Elegir nivel de calidad**:
   - Básico: Más rápido, resultados aceptables
   - HD: Balance entre calidad y velocidad (recomendado)
   - Ultra HD: Mayor calidad, procesamiento más lento
4. **Procesar**: Hacer clic en "¡Intercambiar Rostros!"
5. **Guardar o compartir** el resultado

## Estructura del proyecto

```
FaceSwapPro/
├── main.py                # Punto de entrada principal
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Este archivo
├── src/                   # Código fuente
│   ├── __init__.py
│   ├── face_swap_app.py   # Clase principal de la aplicación
│   ├── core/              # Componentes principales
│   │   ├── __init__.py
│   │   ├── face_detector.py
│   │   ├── face_swapper.py
│   │   └── image_enhancer.py
│   ├── gui/               # Interfaz gráfica
│   │   ├── __init__.py
│   │   └── app_window.py
│   └── utils/             # Utilidades
│       ├── __init__.py
│       └── image_utils.py
├── models/                # Modelos pre-entrenados
├── data/                  # Carpeta para imágenes de entrada
└── output/                # Carpeta para resultados
```

## Consejos para mejores resultados

- Utiliza imágenes con rostros claramente visibles y bien iluminados
- Para resultados óptimos, usa imágenes donde los rostros tengan expresiones y ángulos similares
- Las imágenes de alta resolución producen mejores resultados
- Si experimentas problemas con la detección de rostros, intenta con otras imágenes

## Solución de problemas

**P: La aplicación muestra un error al iniciar**  
R: Asegúrate de haber instalado todas las dependencias con `pip install -r requirements.txt`

**P: No se detectan rostros en mis imágenes**  
R: Usa imágenes con rostros claramente visibles y frontales. Evita imágenes con rostros muy pequeños o parcialmente ocultos.

**P: El resultado no se ve realista**  
R: Prueba con el nivel de calidad "Ultra HD" y asegúrate de usar imágenes de buena calidad con iluminación similar.

## Licencia

Este proyecto se distribuye bajo licencia MIT. Consulta el archivo LICENSE para más detalles.

## Créditos

- [InsightFace](https://github.com/deepinsight/insightface) - Para el modelo de detección e intercambio facial
- [OpenCV](https://opencv.org/) - Para procesamiento de imágenes
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Para la interfaz gráfica

---

⚠️ **Nota ética**: Esta herramienta está diseñada con fines educativos, creativos y de entretenimiento. Por favor, úsala de manera responsable y respetando la privacidad y consentimiento de las personas.