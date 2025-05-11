from app.procesamiento.imagenes import ProcesarImagen
from app.vistas.visor_imagenes import VisorImagenes, SeleccionarMascara


# Creamos una instancia de la clase ProcesarImagen con la imagen a mejorar
Imagen = ProcesarImagen("jose.jpg")

# Seleccionamos el área a restaurar
Mascara = SeleccionarMascara(Imagen.imagen)
Imagen.mask = Mascara.mask
VisorImagenes().mostrar_imagen(Imagen.mask, "Mascara seleccionada")

# Restauramos la imagen
Imagen.restaurar()
VisorImagenes().mostrar_imagen(Imagen.imagen, "Imagen restaurada")

# Aplicamos la mascara a la imagen original
Imagen.aplicar()
VisorImagenes().mostrar_imagen(Imagen.imagen, "Imagen restaurada solo mascara")

# Quitamos el ruido
Imagen.quitar_ruido(20)
VisorImagenes().mostrar_imagen(Imagen.imagen, "Imagen sin ruido")
