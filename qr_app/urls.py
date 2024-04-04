from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('pagina/', views.pagina, name='pagina'),
    path('generate-qr-code/', views.generate_qr_code_view, name='generate_qr_code_view'),
    path('qr-code/', views.qr_code_view, name='qr_code_view'),  
]
