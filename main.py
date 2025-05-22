from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import io # Para BytesIO (IMAGEN EN MEMORIA)
from skimage import io as skio # Para leer y guardar la imagen
import numpy as np
from app.procesamiento.imagenes import ProcesarImagen

app = FastAPI()

@app.post("/procesar-imagen/")
async def procesar_la_imagen(file: UploadFile = File(...), escala: float = 1.0, sigma: float = 0.1, mascara: str = None):
    
    # Se queda esperando el archivo y lo lee como un array
    archivo = await file.read()
    imagen_array = skio.imread(io.BytesIO(archivo))

    # Inicializa el procesador de imagen con el array de la imagen
    Imagen = ProcesarImagen(imagen_array)

    # Aplica los métodos de procesamiento que definimos en la clase ProcesarImagen, aca hay que redefinir la forma en que pasamos la mascara porque antes habiamos definido una interfase gráfica...
    Imagen.reescalar(escala)
    #Mascara = SeleccionarMascara(Imagen.imagen) -> Viejo
    #Imagen.mask = Mascara.mask -> Viejo
    Imagen.quitar_ruido(sigma)
    Imagen.restaurar()
    #procesador.aplicar() -> No la aplicamos aun porque como no hay mascar aun se veria igual que la original


    # Convierte la imagen procesada que viene como array a uint8 (que es el clasico 0-255) para que el output sea una imagen normal
    imagen_procesada_uint8 = (Imagen.imagen * 255).astype(np.uint8)

    # Guarda la imagen procesada en memoria para no escribir en disco y la devuelve como respuesta
    respuesta_imagen_buffer = io.BytesIO()
    skio.imsave(respuesta_imagen_buffer, imagen_procesada_uint8, plugin='imageio', format='png') 
    respuesta_imagen_buffer.seek(0)

    return StreamingResponse(respuesta_imagen_buffer, media_type="image/png")