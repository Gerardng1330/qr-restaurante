from django.urls import path
from . import views

urlpatterns = [
    path('', views.codigo_qr, name='codigo_qr'),
    path('loginyu/', views.login_password, name='login_password'),
    path('upload/', views.upload_view, name='upload'),
    path('menu/', views.image_management_view2, name='menu'),
    path('gestion_de_imagenes/', views.image_management_view, name='image_management_view'),
    path('delete/<int:imagen_id>/', views.delete_image, name='delete_image'),
    path('qr-code/', views.qr_code_view, name='qr_code_view'),
    path('gestion-de-imagenes/', views.image_management_view, name='gestion-de-imagenes'),  

]
