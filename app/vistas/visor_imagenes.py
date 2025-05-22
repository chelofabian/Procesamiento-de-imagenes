import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from matplotlib.widgets import PolygonSelector

class VisorImagenes():
    def __init__(self):
        pass

    def mostrar_imagen(self, imagen, titulo):
        self.imagen = imagen
        self.titulo = titulo
        import matplotlib.pyplot as plt

        plt.imshow(self.imagen)
        plt.title(self.titulo)
        plt.show()


class SeleccionarMascara():
    def __init__(self, imagen):
        self.imagen = imagen
        self.mascara = np.zeros(self.imagen.shape[:2], dtype=np.uint8)

        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Seleccionar mascara en la imagen")
        self.ax.imshow(self.imagen)
        self.selector = PolygonSelector(self.ax, self.on_select)

        plt.show()

    def on_select(self, verts):
        from skimage.draw import polygon
        rr, cc = polygon(np.array([v[1] for v in verts]), np.array([v[0] for v in verts]), self.imagen.shape[:2])
        self.mascara[rr, cc] = 1
     
