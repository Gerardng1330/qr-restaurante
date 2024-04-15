from django.urls import path
from . import views

urlpatterns = [
    path('', views.codigo_qr, name='codigo_qr'),
    path('upload/', views.upload_view, name='upload'),
    path('delete/<int:imagen_id>/', views.delete_image, name='delete_image'),
    path('delete/<int:imagen_id>/', views.delete_image, name='delete_image'),
    path('qr-code/', views.qr_code_view, name='qr_code_view'),
    path('gestion-de-imagenes/', views.image_management_view, name='gestion-de-imagenes'),  

]
