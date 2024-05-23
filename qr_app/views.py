from django.shortcuts import render
import qrcode
from io import BytesIO
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import redirect,get_object_or_404
from .models import Imagen, ImagenMuelle
from django.contrib import messages
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

def login_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gestion-de-imagenes')  # Redirige a la página de gestión de imágenes
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect(request.path_info)
    else:
        return render(request, 'login.html')

@login_required
def gestion_de_imagenes(request):
    if request.method == 'POST':
        if 'delete_image_id' in request.POST:
            imagen_id = request.POST.get('delete_image_id')
            upload_type = request.POST.get('uploadType')
            if upload_type == 'Gallipan':
                imagen = get_object_or_404(Imagen, id=imagen_id)
                imagen.delete()
                messages.success(request, 'Imagen de Gallipan eliminada con éxito')
            elif upload_type == 'Muelle':
                imagen_muelle = get_object_or_404(ImagenMuelle, id=imagen_id)
                imagen_muelle.delete()
                messages.success(request, 'Imagen de Muelle Restaurante eliminada con éxito')
            else:
                messages.error(request, 'Tipo de eliminación desconocido')
        elif 'image' in request.FILES:
            upload_type = request.POST.get('uploadType')
            uploaded_image = request.FILES['image']
            
            if not uploaded_image:
                messages.error(request, 'No se seleccionó ninguna imagen.')
            else:
                img = Image.open(uploaded_image)
                img.thumbnail((800, 800))
                temp_directory = 'C:\\tmp\\'
                os.makedirs(temp_directory, exist_ok=True)
                temp_image_path = os.path.join(temp_directory, uploaded_image.name)
                img.save(temp_image_path)
                temp_image = open(temp_image_path, 'rb')
                temp_uploaded_image = SimpleUploadedFile(uploaded_image.name, temp_image.read())
                
                if upload_type == 'Gallipan':
                    nueva_imagen = Imagen(imagen=temp_uploaded_image)
                    nueva_imagen.save()
                    messages.success(request, 'Imagen subida a Gallipan con éxito')
                elif upload_type == 'Muelle':
                    nueva_imagen = ImagenMuelle(imagen_muelle=temp_uploaded_image)
                    nueva_imagen.save()
                    messages.success(request, 'Imagen subida a Muelle Restaurante con éxito')
                else:
                    messages.error(request, 'Tipo de subida desconocido')
                
                temp_image.close()
                os.remove(temp_image_path)
        
        return redirect('gestion-de-imagenes')
    
    imagenes = Imagen.objects.all()
    imagenes_muelle = ImagenMuelle.objects.all()
    context = {
        'imagenes': imagenes,
        'imagenesMuelle': imagenes_muelle,
    }
    return render(request, 'gestion_de_imagenes.html', context)

def logout_view(request):
    logout(request)
    return redirect('login_password')

@login_required
def panel(request):
    return render(request,'choose_file.html')

def codigo_qr(request):
    return render(request,'codigo_qr.html')

def upload(request):
    return render(request,'upload.html')

def login_view(request):
    return render(request, 'login.html')

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

@csrf_exempt
def delete_image(request):
    if request.method == 'POST' and request.is_ajax():
        imagen_id = request.POST.get('imagen_id')
        upload_type = request.POST.get('upload_type')

        try:
            if upload_type == 'Gallipan':
                imagen = get_object_or_404(Imagen, id=imagen_id)
            elif upload_type == 'Muelle':
                imagen = get_object_or_404(ImagenMuelle, id=imagen_id)
            else:
                return JsonResponse({'success': False, 'error': 'Tipo de imagen no reconocido'})

            imagen.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def delete_image_muelle(request, imagen_id):
    imagen_muelle = get_object_or_404(Imagen, id=imagen_id)
    imagen_muelle.delete()
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