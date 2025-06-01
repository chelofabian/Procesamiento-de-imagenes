from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import io # Para BytesIO (IMAGEN EN MEMORIA)
from skimage import io as skio # Para leer y guardar la imagen
import numpy as np
from procesamiento.imagenes import ProcesarImagen
import ast

app = FastAPI()

@app.get("/")
async def principal():
    return {"message": "Bienvenido a la API de procesamiento de imágenes. Usa /procesar-imagen/ para procesar una imagen, o bien ingresá a /docs para ver la documentación interactiva."}

@app.post("/procesar-imagen/")
async def procesar_la_imagen(file: UploadFile = File(...), escala: float = 1.0, sigma: float = 0.1, mascara: str = None):
    
    # Se queda esperando el archivo y lo lee como un array
    archivo = await file.read()
    imagen_array = skio.imread(io.BytesIO(archivo))

    # Inicializa el procesador de imagen con el array de la imagen
    Imagen = ProcesarImagen(imagen_array)

    # Aplica los métodos de procesamiento que definimos en la clase ProcesarImagen, aca hay que redefinir la forma en que pasamos la mascara porque antes habiamos definido una interfase gráfica...
    # Imagen.reescalar(escala)

    if mascara is not None:
        # Convierte la cadena de la máscara en un array de booleanos
        try:
            mascara_lista = ast.literal_eval(mascara)
            mascara_array = np.array(mascara_lista, dtype=bool)
            # Redimensiona la máscara si es necesario
            if mascara_array.shape != Imagen.imagen.shape[:-1]:
                mascara_array = np.resize(mascara_array, Imagen.imagen.shape[:-1])
            Imagen.mascara = mascara_array
        except Exception as e:
            raise ValueError(f"Error al procesar la máscara: {e}")
    else:
        Imagen.mascara = np.zeros(Imagen.imagen.shape[:-1], dtype=bool)


    # Pasos especificos de procesamiento ################ -> Esto capaz hay que meterlo en otra clase pero por ahora lo dejamos asi

    Imagen.quitar_ruido(sigma)
    Imagen.restaurar()
    Imagen.quitar_ruido(sigma)
    Imagen.aplicar() 

    # fin pasos especificos de procesamiento ############

    # Convierte la imagen procesada que viene como array a uint8 (que es el clasico 0-255) para que el output sea una imagen normal
    imagen_procesada_uint8 = (Imagen.imagen * 255).astype(np.uint8)

    # Guarda la imagen procesada en memoria para no escribir en disco y la devuelve como respuesta
    respuesta_imagen_memoria = io.BytesIO()
    skio.imsave(respuesta_imagen_memoria, imagen_procesada_uint8, plugin='imageio', format='png') 
    respuesta_imagen_memoria.seek(0)

    return StreamingResponse(respuesta_imagen_memoria, media_type="image/png")