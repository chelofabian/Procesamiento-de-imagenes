from skimage import io, util
from skimage.restoration import inpaint, denoise_tv_bregman
import numpy as np
from skimage import transform
import skimage.filters

import numpy as np

class ProcesarImagen:
    def __init__(self, ruta):
        image = io.imread(ruta)
        self.imagen_original = util.img_as_float(image)
        self.imagen = self.imagen_original.copy()
        self.mask = np.zeros(self.imagen.shape[:-1])   
   
    def reescalar(self, scale):
        self.imagen = transform.rescale(self.imagen, scale, anti_aliasing=False, channel_axis=-1)
        self.mask = np.zeros(self.imagen.shape[:-1])  # Moficiar la máscara para que coincida con la imagen reescalada

    def quitar_ruido(self, sigma):
        self.imagen = denoise_tv_bregman(self.imagen, weight=sigma) #Cambio el metodo de quitar ruido a uno que funciona mejor

    def restaurar(self):
        self.imagen = inpaint.inpaint_biharmonic(self.imagen, self.mask, channel_axis=-1)

    def aplicar(self):
        self.imagen[self.mask == 0] = self.imagen_original[self.mask == 0]
