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
from .forms import UserEditForm
from .forms import SignUpForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import card,ImagenOtroCard
from .forms import CardForm

def add_card(request):
    cards = card.objects.all()
    form = CardForm()
    
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('prueba')  # Redirige a la misma página para actualizar la lista de tarjetas
    
    return render(request, 'prueba.html', {'cards': cards, 'form': form})

def delete_card(request, card_id):
    cards = get_object_or_404(card, id=card_id)
    
    if request.method == 'POST':
        cards.delete()
        return redirect('prueba')  # Redirige a la misma página para actualizar la lista de tarjetas

    return render(request, 'prueba.html')

@login_required
def edit_profile(request):
    cards = card.objects.all()

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito')
            return redirect('edit_profile')
    else:
        form = UserEditForm(instance=request.user)
    
    context = {
        'form': form,
        'cards':cards,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def register(request):
    cards = card.objects.all()

    form = SignUpForm()
    password_form = PasswordChangeForm(request.user)
    
    if request.method == 'POST':
        if 'old_password' in request.POST:  # Cambio de contraseña
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Tu contraseña ha sido cambiada con éxito.', extra_tags='password_change')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario de contraseña.', extra_tags='password_change')
        else:  # Registro de nuevo usuario
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.email = form.cleaned_data.get('email')
                user.is_staff = True
                user.save()
                messages.success(request, f'Cuenta creada para {user.username}!', extra_tags='user_registration')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario de registro.', extra_tags='user_registration')

    context = {
        'form': form,
        'password_form': password_form,
        'cards':cards,
    }
    return render(request, 'edit_profile.html', context)


def login_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('prueba')  # Redirige a la página de gestión de imágenes
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return redirect(request.path_info)
    else:
        return render(request, 'login.html')

@login_required
def gestion_gallipan(request):
    imagenes = Imagen.objects.all()
    return render(request, 'gallipan.html',{'imagenes':imagenes})

@login_required
def ver_muelle(request):
    imagenes = ImagenMuelle.objects.all()
    return render(request, 'muelle.html',{'imagenes':imagenes})

@login_required
def gestion_muelle(request):
    cards = card.objects.all()

    if request.method == 'POST':
        if 'delete_image_id' in request.POST:
            imagen_id = request.POST.get('delete_image_id')
            imagen_muelle = get_object_or_404(ImagenMuelle, id=imagen_id)
            imagen_muelle.delete()
            messages.success(request, 'Imagen de Muelle Restaurante eliminada con éxito')
        elif 'image' in request.FILES:
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
                nueva_imagen = ImagenMuelle(imagen_muelle=temp_uploaded_image)
                nueva_imagen.save()
                messages.success(request, 'Imagen subida a Muelle Restaurante con éxito')
                temp_image.close()
                os.remove(temp_image_path)
        elif 'move_image_id' in request.POST:
            image_id = request.POST['move_image_id']
            action = request.POST['move_action']
            image = get_object_or_404(ImagenMuelle, id=image_id)

            if action == 'up':
                previous_image = ImagenMuelle.objects.filter(order__lt=image.order).order_by('-order').first()
                if previous_image:
                    image.order, previous_image.order = previous_image.order, image.order
                    image.save()
                    previous_image.save()
            elif action == 'down':
                next_image = ImagenMuelle.objects.filter(order__gt=image.order).order_by('order').first()
                if next_image:
                    image.order, next_image.order = next_image.order, image.order
                    image.save()
                    next_image.save()

        return redirect('menu-muelle')

    # Ordenar las imágenes por el campo `order`
    imagenes_muelle = ImagenMuelle.objects.all().order_by('order')
    context = {
        'imagenesMuelle': imagenes_muelle,
        'cards': cards,
    }
    return render(request, 'menu_muelle.html', context)


@login_required
def gestion_inicio(request):
    return render(request,'inicio.html')

def otroCard(request):
    cards = card.objects.all()
    card_obj = card.objects.first()
    imagenes = ImagenOtroCard.objects.all().order_by('order')

    if request.method == 'POST':
        if 'delete_image_id' in request.POST:
            imagen_id = request.POST.get('delete_image_id')
            imagen_otroCard = get_object_or_404(ImagenOtroCard, id=imagen_id)
            imagen_otroCard.delete()
            messages.success(request, 'Imagen eliminada con éxito')

        elif 'image' in request.FILES:
            uploaded_image = request.FILES['image']
            if not uploaded_image:
                messages.error(request, 'No se seleccionó ninguna imagen.')
            else:
                img = Image.open(uploaded_image)
                img.thumbnail((800, 800))  # Ajusta el tamaño de la imagen
                temp_directory = 'C:\\tmp\\'
                os.makedirs(temp_directory, exist_ok=True)
                temp_image_path = os.path.join(temp_directory, uploaded_image.name)
                img.save(temp_image_path)
                temp_image = open(temp_image_path, 'rb')
                temp_uploaded_image = SimpleUploadedFile(uploaded_image.name, temp_image.read())
                nueva_imagen = ImagenOtroCard(imagen_otroCard=temp_uploaded_image)
                nueva_imagen.save()
                messages.success(request, 'Imagen subida a Gallipan con éxito')
                temp_image.close()
                os.remove(temp_image_path)

        elif 'move_image_id' in request.POST:
            image_id = request.POST['move_image_id']
            action = request.POST['move_action']
            image = ImagenOtroCard.objects.get(id=image_id)

            if action == 'up':
                previous_image = ImagenOtroCard.objects.filter(order__lt=image.order).order_by('-order').first()
                if previous_image:
                    image.order, previous_image.order = previous_image.order, image.order
                    image.save()
                    previous_image.save()
            elif action == 'down':
                next_image = ImagenOtroCard.objects.filter(order__gt=image.order).order_by('order').first()
                if next_image:
                    image.order, next_image.order = next_image.order, image.order
                    image.save()
                    next_image.save()

        return redirect('otroCard')

    context = {
        'imagenes': imagenes,
        'cards': cards,
        'card_obj': card_obj,

    }
    return render(request, 'otroCard.html', context)


def logout_view(request):
    logout(request)
    return redirect('login_password')

def codigo_qr(request):
    return render(request,'codigo_qr.html')

def muelle_qr(request):
    return render(request,'muelle_qr.html')

def prueba(request):
    return render(request,'prueba.html')

def login_view(request):
    return render(request, 'login.html')


def menu_view(request):
    return render(request,'menu.html')

@login_required
def image_management_view2(request):
    cards = card.objects.all()

    if request.method == 'POST':
        if 'delete_image_id' in request.POST:
            imagen_id = request.POST.get('delete_image_id')
            imagen = get_object_or_404(Imagen, id=imagen_id)
            imagen.delete()
            messages.success(request, 'Imagen de Gallipan eliminada con éxito')
        elif 'image' in request.FILES:
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
                nueva_imagen = Imagen(imagen=temp_uploaded_image)
                nueva_imagen.save()
                messages.success(request, 'Imagen subida a Gallipan con éxito')
                temp_image.close()
                os.remove(temp_image_path)
        elif 'move_image_id' in request.POST:
            image_id = request.POST['move_image_id']
            action = request.POST['move_action']
            image = Imagen.objects.get(id=image_id)

            print(f"Moving image ID {image_id} {action} - Current order: {image.order}")

            if action == 'up':
                previous_image = Imagen.objects.filter(order__lt=image.order).order_by('-order').first()
                if previous_image:
                    print(f"Previous image order: {previous_image.order}")
                    # Intercambia los valores de 'order'
                    image.order, previous_image.order = previous_image.order, image.order
                    image.save()
                    previous_image.save()
            elif action == 'down':
                next_image = Imagen.objects.filter(order__gt=image.order).order_by('order').first()
                if next_image:
                    print(f"Next image order: {next_image.order}")
                    # Intercambia los valores de 'order'
                    image.order, next_image.order = next_image.order, image.order
                    image.save()
                    next_image.save()

        return redirect('menu-gallipan')

    imagenes = Imagen.objects.all().order_by('order')
    context = {
        'imagenes': imagenes,
        'cards': cards,
    }
    return render(request, 'menu_gallipan.html', context)


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

@login_required
def menu_muelle(request):
    cards = card.objects.all()

    if request.method == 'POST':
        if 'delete_image_id' in request.POST:
            imagen_id = request.POST.get('delete_image_id')
            imagen_muelle = get_object_or_404(ImagenMuelle, id=imagen_id)
            imagen_muelle.delete()
            messages.success(request, 'Imagen de Muelle Restaurante eliminada con éxito')
        elif 'image' in request.FILES:
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
                nueva_imagen = ImagenMuelle(imagen_muelle=temp_uploaded_image)
                nueva_imagen.save()
                messages.success(request, 'Imagen subida a Muelle Restaurante con éxito')
                temp_image.close()
                os.remove(temp_image_path)
        return redirect('menu-muelle')

    imagenes_muelle = ImagenMuelle.objects.all()
    context = {
        'imagenesMuelle': imagenes_muelle,
        'cards':cards,
    }
    return render(request, 'menu_muelle.html', context)

def delete_image_muelle(request, imagen_id):
    imagen_muelle = get_object_or_404(Imagen, id=imagen_id)
    imagen_muelle.delete()
    return redirect('image_management_view')

def image_management_view(request):
    imagenes = Imagen.objects.all()
    return render(request, 'gestion_de_imagenes.html', {'imagenes': imagenes})


def side(request):
    cards = card.objects.all()
    if request.method == 'POST':
        if 'delete_image_id' in request.POST:
            imagen_id = request.POST.get('delete_image_id')
            imagen_muelle = get_object_or_404(ImagenMuelle, id=imagen_id)
            imagen_muelle.delete()
            messages.success(request, 'Imagen de Muelle Restaurante eliminada con éxito')
        elif 'image' in request.FILES:
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
                nueva_imagen = ImagenMuelle(imagen_muelle=temp_uploaded_image)
                nueva_imagen.save()
                messages.success(request, 'Imagen subida a Muelle Restaurante con éxito')
                temp_image.close()
                os.remove(temp_image_path)
        return redirect('gestion-muelle')

    imagenes_muelle = ImagenMuelle.objects.all()
    context = {
        'imagenesMuelle': imagenes_muelle,
        'cards':cards,
    }
    return render(request, 'side.html', context)

def qr_code_view(request):
    # URL a la que deseas redirigir cuando se escanea el código QR
    local_url = "https://www.google.com/"

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


def muelle_qr_view(request):
    # URL a la que deseas redirigir cuando se escanea el código QR
    local_url = "http://127.0.0.1:2000/muelle_qr"

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