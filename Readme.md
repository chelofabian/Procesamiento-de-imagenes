# Restauración de Imágenes con Scikit-image y FastAPI

Este proyecto implementa una API básica para la restauración de imágenes utilizando la biblioteca Scikit-image. Permite cargar una imagen, aplicar varias operaciones de procesamiento como eliminación de ruido y restauración de áreas dañadas (inpainting) basadas en una máscara, y devuelve la imagen procesada.

## Requisitos

* Python 3.x
* FastAPI (`pip install fastapi`)
* Uvicorn (`pip install uvicorn[standard]`) o cualquier otro servidor ASGI.
* Scikit-image (`pip install scikit-image`)
* NumPy (se instala automáticamente con Scikit-image)
* python-multipart (`pip install python-multipart`) (para `UploadFile` en FastAPI)

## Conceptos Clave de Procesamiento de Imágenes

### Carga de Imágenes
Los valores de color de las imágenes suelen almacenarse como enteros (por ejemplo, 0-255). Para operaciones de procesamiento, es recomendable convertir las imágenes a formato de punto flotante (rango [0,1] o [-1,1]). Esto permite trabajar con valores decimales y evita la pérdida de información. En este proyecto, se utiliza `skimage.util.img_as_float()` para esta conversión si la imagen de entrada no está ya en formato flotante.

## Organización del Espacio de Trabajo

* **`app/`**: Contiene la lógica principal de la aplicación.
    * **`main.py`**: Define la API FastAPI, sus endpoints y maneja las solicitudes HTTP.
    * **`procesamiento/`**: Módulos relacionados con el procesamiento de imágenes.
        * **`imagenes.py`**: Contiene la clase `ProcesarImagen` que encapsula las operaciones de procesamiento.
* **`logs/`**: Archivos Python o carpetas de etapas iniciales de desarrollo o pruebas que no se utilizan directamente en la API actual.

## Funcionamiento de la API

La API se construye con FastAPI. El procesamiento de imágenes se invoca a través de un endpoint específico.

### Endpoints

* **`GET /`**
    * Descripción: Devuelve un mensaje de bienvenida.
    * Respuesta: `{"message": "Bienvenido a la API de procesamiento de imágenes. Usa /procesar-imagen/ para procesar una imagen, o bien ingresá a /docs para ver la documentación interactiva."}`

* **`POST /procesar-imagen/`**
    * Descripción: Procesa una imagen cargada.
    * Request:
        * `file`: Un archivo de imagen (UploadFile).
        * `escala` (opcional): Factor de reescalamiento (float, default: `1.0`). *Nota: Actualmente, el reescalamiento está comentado en `main.py`.*
        * `sigma` (opcional): Peso para la eliminación de ruido (float, default: `0.1`).
        * `mascara` (opcional): Una cadena de texto que representa una lista de listas o un array NumPy para la máscara (ej: `"[[False, True], [True, False]]"`). Si no se provee, se usa una máscara vacía (todo `False`).
    * Proceso:
        1.  Lee el archivo de imagen cargado.
        2.  Inicializa la clase `ProcesarImagen` con los datos de la imagen.
        3.  Si se proporciona una `mascara` en formato string, la convierte a un array NumPy booleano. Si las dimensiones no coinciden con la imagen, intenta redimensionarla. Si no se proporciona, se crea una máscara de ceros (ninguna área enmascarada).
        4.  Aplica las siguientes operaciones de procesamiento en secuencia:
            * Eliminación de ruido (`quitar_ruido`).
            * Restauración de la imagen (`restaurar`).
            * Eliminación de ruido nuevamente (`quitar_ruido`).
            * Aplica los cambios de la imagen procesada a la original solo en las áreas no enmascaradas (`aplicar`).
        5.  Convierte la imagen procesada a formato `uint8` (rango 0-255).
        6.  Guarda la imagen procesada en memoria y la devuelve como una respuesta PNG.
    * Respuesta: `StreamingResponse` con la imagen procesada en formato PNG.

### Cómo ejecutar la API localmente:

1.  Asegúrate de tener todos los requisitos instalados.
2.  Navega al directorio raíz del proyecto.
3.  Ejecuta la aplicación usando Uvicorn:
    ```bash
    uvicorn app.main:app --reload
    ```
4.  Accede a la documentación interactiva de la API en `http://127.0.0.1:8000/docs`.

## Componentes Principales

### Clase `ProcesarImagen` (desde `app/procesamiento/imagenes.py`)

Esta clase se encarga de cargar la imagen (recibe un array NumPy), convertirla a formato flotante si es necesario, y aplicar diversas operaciones de procesamiento.

* **`__init__(self, imagen)`**:
    * Convierte la imagen de entrada a tipo flotante (`float`) si no lo es.
    * Guarda una copia de la imagen original (convertida a flotante) para comparaciones o para aplicar cambios selectivamente.
    * Inicializa `self.imagen` como una copia de la imagen original.
    * Crea una máscara inicial vacía (un array de ceros) con las dimensiones de la imagen (sin el canal de color).

* **`reescalar(self, scale)`**:
    * Reescala `self.imagen` utilizando `transform.rescale`.
    * Reinicia la máscara para que coincida con las nuevas dimensiones de la imagen.
    * *Nota: Este método existe pero su llamada está actualmente comentada en `main.py`.*

* **`quitar_ruido(self, sigma)`**:
    * Aplica la eliminación de ruido utilizando el algoritmo de Total Variation Bregman (`denoise_tv_bregman`).

* **`restaurar(self)`**:
    * Restaura las regiones de `self.imagen` especificadas por `self.mascara` utilizando `inpaint.inpaint_biharmonic`.

* **`aplicar(self)`**:
    * Combina la imagen procesada con la imagen original. Las partes de la imagen original que no estaban enmascaradas (`self.mascara == 0`) se restauran a partir de `self.imagen_original`. Esto asegura que solo las áreas enmascaradas y luego restauradas retengan los cambios del inpainting, mientras que el resto de la imagen permanece fiel al original después del procesamiento de ruido.

### Clases de Vista (Mencionadas en el Readme Original)

* **`VisorImagenes`**: Mencionada para visualización básica de imágenes.
* **`SeleccionarMascara`**: Mencionada para permitir la selección del área de máscara.

> *Nota: Estas clases parecen ser de una etapa anterior o para una interfaz gráfica, ya que la API actual en `main.py` maneja la máscara como una cadena de texto y no utiliza directamente estas clases de "vistas".*

## Notas Adicionales

* La API actual es una versión básica y podría expandirse con más funcionalidades y opciones de procesamiento.
* El manejo de la máscara a través de una cadena de texto en la API requiere que el cliente formatee correctamente la máscara.