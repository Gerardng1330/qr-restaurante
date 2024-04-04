from django.shortcuts import render
import qrcode
from io import BytesIO
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import redirect

def menu(request):
    return render(request,'menu.html')

def pagina(request):
    return render(request,'inicio.html')

def generate_qr_code_view(request):
   redirect_url = "https://www.google.com"
   return redirect(redirect_url)

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