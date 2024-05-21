from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.

#tabla para guardar la imagen gallipan
class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')

#tabla para guardar la imagen muelle
class ImagenMuelle(models.Model):
    imagen_muelle = models.ImageField(upload_to='imagenesMuelle/')

class LoginForm(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)