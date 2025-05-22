# Restauración de imágenes con Sckit-image

# **FALTA REESCRIBIR CON LOS ÚLTIMOS CAMBIOS**

## Lo que se hizo es la api mas básicas de las apis... 

-----------------------------------------------

## Requisitos

1. Scikit-image (pip install scikit-image)
2. Matplot (pip install matplot)
3. Numpy (Instala automaticamente con scikit-image)

## Conceptos a tener en cuenta

### Carga de imagenes

Normalmente, los valores de color de la imagen se almacenan como números enteros dentro de un rango específico, por ejemplo, de 0 a 255. 
Es recomendable que las imagenes estén en formato de punto flotante en el rango o [-1,1], esto permite operar con valores decimales y evita la perdida de información. 
Para esto se puede usar la función: **función skimage.util.img_as_float()**

### Organización del espacio de trabajo

#### app:
* procesamiento: para almacenar todos los modulos referentes al procesamiento de imágenes
* vistas: para almacenar todo lo referente a la interfase gráfica. 

> A medida que el código cresca se van a ir agregando carpetas.

#### logs: 

* Contiene archivos .py que fueron parte del desarrollo inicial pero que no serán aplicados por el momento. 

#### Subidas: 

* Lugar donde se almacenan las imágenes originales. 

#### Transformadas: 

* Lugar donde se guardan los resultados. 

## Funcionamiento

Por el momento el llamado al procesamiento de imagenes se realiza en el main. 

### Clase **ProcesarImagen** (desde app/procesamiento/imagenes): 

Se encarga de cargar la imagen y convertirla. Guarda tambien una instancia de la imagen original para comparaciones futuras y crea la máscara en relación al tamaño de inicio de la fotografia. 

Dentro de esta clase se pueden realizar las siguientes operaciones: 

* Reescalar.
* Quitar ruido.
* Restaurar
* Aplicar modificaciones a la imagen original. 

### Clase **VisorImagenes** (desde app/vistas/visor_imagenes):

Visualización básica de imagenes, en modulo a parte para poder ir cambiandolo a necesidad. 

### Clase **SeleccionarMascara** (desde app/vistas/visor_imagenes):

Permite seleccionar el área de mascara a aplicar sobre una imagen.  

