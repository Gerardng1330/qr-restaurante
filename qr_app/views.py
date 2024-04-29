from django.shortcuts import render
import qrcode
from io import BytesIO
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import redirect,get_object_or_404
from .models import Imagen
from django.contrib import messages
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import os

def gestion_de_imagenes(request):
    return render(request,'gestion_de_imagenes.html')

def codigo_qr(request):
    return render(request,'codigo_qr.html')

def upload(request):
    return render(request,'upload.html')


def upload_view(request):
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_image = request.FILES['image']
        
        # Abre la imagen utilizando PIL
        img = Image.open(uploaded_image)
        
        # Redimensiona la imagen a 800x800 píxeles (manteniendo la proporción)
        img.thumbnail((800, 800))
        
        # Crea el directorio temporal si no existe
        temp_directory = 'C:\\tmp\\'
        os.makedirs(temp_directory, exist_ok=True)
        
        # Guarda la imagen redimensionada en un archivo temporal
        temp_image_path = os.path.join(temp_directory, uploaded_image.name)
        img.save(temp_image_path)
        
        # Crea un objeto SimpleUploadedFile para la imagen redimensionada
        temp_image = open(temp_image_path, 'rb')
        temp_uploaded_image = SimpleUploadedFile(uploaded_image.name, temp_image.read())
        
        # Guarda la imagen redimensionada en el modelo
        imagen = Imagen(imagen=temp_uploaded_image)
        imagen.save()
        
        # Cierra y elimina el archivo temporal
        temp_image.close()
        os.remove(temp_image_path)
        
        messages.success(request, 'La imagen se subió correctamente.')
    else:
        pass
    
    return render(request, 'upload.html')

def menu_view(request):
    return render(request,'menu.html')

def image_management_view2(request):
    imagenes = Imagen.objects.all()
    return render(request, 'menu.html', {'imagenes': imagenes})

def delete_image(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)
    imagen.delete()
    return redirect('image_management_view')

def image_management_view(request):
    imagenes = Imagen.objects.all()
    return render(request, 'gestion_de_imagenes.html', {'imagenes': imagenes})



def qr_code_view(request):
    # URL a la que deseas redirigir cuando se escanea el código QR
    local_url = "http://127.0.0.1:2000/pagina"

    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(local_url)
    qr.make(fit=True)

    # Crear una imagen del código QR
    buffer = BytesIO()
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(buffer, format="PNG")

    # Devolver la imagen como respuesta HTTP
    return HttpResponse(buffer.getvalue(), content_type="image/png")