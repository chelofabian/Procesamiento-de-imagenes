import cv2
import matplotlib.pyplot as plt

#1. Carga y visualización de la imagen original: 

imagen = cv2.imread('Mario.jpg')
imagen_bgr = cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)

plt.imshow(imagen_bgr)
plt.axis('off')
plt.savefig('transformadas/imagen_bgr.jpg', dpi=300)

#2. Conversión a escala de grises:

imagen_grises = cv2.imread('transformadas/imagen_bgr.jpg', cv2.IMREAD_GRAYSCALE)

plt.imshow(imagen_grises, cmap='gray')
plt.axis('off')
plt.savefig('transformadas/imagen_grises.jpg', dpi=300)

# 3. Reducción de niveles de gris: 

def reducir_imagen(imagen, niveles):
    factor = 256 // niveles
    """
    factor = 256 / 7 # -> 36,57
    factor = 256 // 7 # -> 36
    """
    imagen_reescalada = (imagen//factor) * factor
    plt.imshow(imagen_reescalada, cmap='gray')
    plt.axis('off')
    plt.savefig(f'transformadas/imagen_grises_{niveles}.jpg', dpi=300)

niveles = [2, 4, 8, 16, 32, 64, 128, 256]

for i in niveles:
    reducir_imagen(imagen_grises, i)

# 4.

def detectar_bordes(imagen, umbral_minimo, umbral_maximo):

    imagen_reescalada = cv2.Canny(imagen, umbral_minimo, umbral_maximo)
    plt.imshow(imagen_reescalada, cmap='gray')
    plt.axis('off')
    plt.savefig(f'transformadas/imagen_con_bordes_{umbral_minimo}_a_{umbral_maximo}.jpg', dpi=300)

umbrales = [(100, 200), (50, 150), (150, 250), (200, 300)]

for umbral in umbrales:
    detectar_bordes(imagen_grises, umbral[0], umbral[1])


