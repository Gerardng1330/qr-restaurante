from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your models here.

#tabla para guardar la imagen
class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')


class LoginForm(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)