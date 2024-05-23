from django.urls import path
from . import views

urlpatterns = [
    path('', views.codigo_qr, name='codigo_qr'),
    path('login/', views.login_password, name='login_password'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_view, name='upload'),
    path('panel/', views.panel, name='panel'),
    path('menu/', views.image_management_view2, name='menu'),
    path('login/gestion_de_imagenes/', views.image_management_view, name='image_management_view'),
    path('delete/<int:imagen_id>/', views.delete_image, name='delete_image'),
    path('delete_muelle/<int:imagen_id>/', views.delete_image_muelle, name='delete_image_muelle'),
    path('qr-code/', views.qr_code_view, name='qr_code_view'),
    path('gestion-de-imagenes/', views.gestion_de_imagenes, name='gestion-de-imagenes'),  
]
