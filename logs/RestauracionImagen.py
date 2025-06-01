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
damaged_image = skimage.io.imread("app/subidas/imagenoriginal.png")
#Reescalamiento
image_rescaled = transform.rescale(damaged_image, 1, anti_aliasing=False, channel_axis=-1)

# Mostrar imagen original y reescalada con matplotlib
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(damaged_image)
plt.title("Imagen original")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(image_rescaled)
plt.title("Imagen reescalada")
#plt.axis("off")

plt.tight_layout()
plt.show()

#3 - Quitar el ruido a la imagen dañida

filtered_image = skimage.filters.gaussian(image_rescaled, sigma=3)
plt.figure(figsize=(10, 5))
plt.imshow(filtered_image)
plt.title ("Imagen sin ruido")
#plt.axis("off")
plt.show()

#Create a mascara. The image's torn out parts will be 
#white in the mascara, the rest of the mascara will be black. 


mascara = np.zeros(image_rescaled.shape[:-1])
mascara[128:180,66:170]=1
#mascara[150:183, 0:75]=1
#mascara[315:435, 355:488]=1
#Display the mascara:
skimage.io.imshow(mascara)
plt.title('Binary mascara')
#plt.axis('off')

# Restaurar la imagen 
"""
# ############################################################
# Falta como meter este cambio a la original
# ############################################################
# 
# """
restored_image = skimage.restoration.inpaint_biharmonic(filtered_image, mascara, channel_axis=-1)

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







