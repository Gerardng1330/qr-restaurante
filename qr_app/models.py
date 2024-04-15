from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.

#tabla para guardar la imagen
class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')


