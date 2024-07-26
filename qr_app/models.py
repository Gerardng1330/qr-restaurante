from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

#tabla para guardar la informacion de las cartas (titulo y imagen)
class card(models.Model):
    title=models.CharField(max_length=200)
    imagen_card=models.ImageField(upload_to='card/')
    
    def __str__(self):
        return self.title

#tabla para guardar la imagen gallipan
class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')

#tabla para guardar la imagen muelle
class ImagenMuelle(models.Model):
    imagen_muelle = models.ImageField(upload_to='imagenesMuelle/')

#tabla para guardar el usuario y la contraseña
class LoginForm(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)