from skimage import util
from skimage.restoration import inpaint, denoise_tv_bregman
import numpy as np
from skimage import transform


class ProcesarImagen:
    def __init__(self, imagen):
        # Convertir la imagen a float y crear una mascara vacia (cambio en como se maneja la imagen, antes las cargabamos acá y ahora recibimos el array, EN TEORIA NO DEBERIAMOS ENTONCES CONVERTIR A FLOAT PERO POR LAS DUDAS)
        if imagen.dtype != np.float32 and imagen.dtype != np.float64:
            self.imagen_original = util.img_as_float(imagen)
        else:
            self.imagen_original = imagen.copy()
        self.imagen = self.imagen_original.copy()
        self.mascara = np.zeros(self.imagen.shape[:-1])   

    def reescalar(self, scale):
        self.imagen = transform.rescale(self.imagen, scale, anti_aliasing=False, channel_axis=-1)
        self.mascara = np.zeros(self.imagen.shape[:-1]) # Modificar la máscara para que coincida con la imagen reescalada, con esto si o sí se tiene que reescalar antes de procesar algo

    def quitar_ruido(self, sigma):
        self.imagen = denoise_tv_bregman(self.imagen, weight=sigma)  #Cambio el metodo de quitar ruido a uno que funciona mejor

    def restaurar(self):
        self.imagen = inpaint.inpaint_biharmonic(self.imagen, self.mascara, channel_axis=-1)

    def aplicar(self):
        self.imagen[self.mascara == 0] = self.imagen_original[self.mascara == 0]
