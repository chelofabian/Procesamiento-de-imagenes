from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

class Imagen:
    def __init__(self, ruta):
        self.ruta = ruta
        self.imagen = imread(ruta)

    def mostrar(self):
        plt.imshow(self.imagen, cmap='gray')
        plt.axis('off')
        plt.show()

    def guardar(self, nombre_archivo):
        plt.imsave(nombre_archivo, self.imagen)

    def convertir_a_grises(self):
        from skimage.color import rgb2gray
        self.imagen = rgb2gray(self.imagen)

    def reducir_niveles(self, niveles):
        if self.imagen.dtype == np.float64:
            imagen_reducida = np.floor(self.imagen * niveles) / niveles
        else:  # Asumiendo tipo entero (por ejemplo, uint8)
            imagen_reducida = (self.imagen // niveles) * niveles
        self.imagen = imagen_reducida.astype(self.imagen.dtype)   

    def detectar_bordes(self, umbral_minimo, umbral_maximo):
        from skimage import feature
        self.imagen = feature.canny(self.imagen, sigma=1, low_threshold=umbral_minimo, high_threshold=umbral_maximo)




# Inicializar
imagen = Imagen('Mario.jpg')
imagen.mostrar()

imagen.convertir_a_grises()
imagen.mostrar()

imagen.guardar('transformadas/imagen_grises_skimage.jpg')

imagen.reducir_niveles(4)
imagen.mostrar()

imagen.guardar('transformadas/imagen_grises_skimage_2.jpg')

imagen.detectar_bordes(0.1, 0.2)
imagen.mostrar()

imagen.guardar('transformadas/imagen_bordes_skimage.jpg')
