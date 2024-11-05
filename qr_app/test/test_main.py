import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client
from qr_app.models import card, Imagen  # Asegúrate de que estos modelos estén disponibles

User = get_user_model()






@pytest.mark.django_db
def test_login_password_valid_user(client, django_user_model):
    user = django_user_model.objects.create_user(username='validuser', password='ng133020')
    
    url = reverse('login_password')
    response = client.post(url, {'username': 'validuser', 'password': 'ng133020'})
    
    assert response.status_code == 302
    assert response.url == reverse('prueba')  # Cambia 'prueba' al nombre de la URL de redirección correcta

@pytest.mark.django_db
def test_login_password_invalid_user(client):
    url = reverse('login_password')
    response = client.post(url, {'username': 'invaliduser', 'password': 'wrongpassword'})
    
    assert response.status_code == 302
    messages = list(get_messages(response.wsgi_request))
    assert any('Usuario o contraseña incorrectos.' in str(m) for m in messages)


