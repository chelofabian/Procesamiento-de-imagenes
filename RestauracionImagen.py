#Importación de las librarías necesarias


import skimage
print(skimage.__version__)


import skimage.io
from skimage.restoration import inpaint
import matplotlib.pyplot as plt
import numpy as np
from skimage import transform
import skimage.filters

# Carga y reescalamiento de una imagen dañida

#Carga de la imagen
damaged_image = skimage.io.imread("/Users/aliocha/Documents/IFTS18/Tecnica_Procesamiento_Imagenes/imagenoriginal.png")
#Reescalamiento
image_rescaled = transform.rescale(damaged_image, 1/4, anti_aliasing=False, channel_axis=-1)

#Mostrar imageb - no se usa más
#skimage.io.imshow(damaged_image)
#skimage.io.imshow(image_rescaled)

# Mostrar imagen original y reescalada con matplotlib
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(damaged_image)
plt.title("Imagen original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_rescaled)
plt.title("Imagen reescalada")
plt.axis("off")

plt.tight_layout()
plt.show()

#3 - Quitar el ruido a la imagen dañida
filtered_image = skimage.filters.gaussian(image_rescaled, sigma=2)
plt.figure(figsize=(10, 5))
plt.imshow(filtered_image)
plt.title ("Imagen sin ruido")
plt.axis("off")
plt.show()

#Create a mask. The image's torn out parts will be 
#white in the mask, the rest of the mask will be black. 
mask = np.zeros(image_rescaled.shape[:-1])
mask[360:400,40:100]=1
mask[382:405, 330:357]=1
mask[315:435, 355:488]=1
#Display the mask:
skimage.io.imshow(mask)
plt.title('Binary Mask')
plt.axis('off')

# Restablecer la imagen:
from skimage.draw import rectangle

# Suponiendo que quieres enmascarar un área rectangular de la imagen para restaurarla
# Coordenadas de la esquina superior izquierda y la esquina inferior derecha de la máscara
start_row, start_col = 50, 50  # Establecer donde comienza la máscara
end_row, end_col = 150, 150    # Establecer donde termina la máscara

# Crear la máscara (binaria)
mask = np.zeros(filtered_image.shape[:2], dtype=bool)  # Forma de la máscara (gris, no RGB)
rr, cc = rectangle(start=(start_row, start_col), end=(end_row, end_col), extent=None, shape=mask.shape)
mask[rr, cc] = 1  # Poner a 1 los píxeles que se van a restaurar

# Restaurar la imagen:
restored_image = skimage.restoration.inpaint_biharmonic(filtered_image, mask, channel_axis=-1)

# Graficar la imagen restaurada junto con la imagen original:
f, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(image_rescaled)
ax[0].set_title('Imagen Original')
ax[0].axis('off')
ax[1].imshow(restored_image)
ax[1].set_title('Imagen Restaurada')
ax[1].axis('off')

plt.tight_layout()
plt.show()







