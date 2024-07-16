from django.urls import path
from . import views

urlpatterns = [
    #codigos qr
    path('muelle-qr',views.muelle_qr, name='muelle-qr'),
    path('gallipan-qr', views.codigo_qr, name='codigo_qr'),
    #views de los qr
    path('qr-code/', views.qr_code_view, name='qr_code_view'),
    path('muelle-qr-code/',views.muelle_qr_view, name='qr_muelle_view'),
    #urls para el admin
    path('login/', views.login_password, name='login_password'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_view, name='upload'),
    path('panel/', views.panel, name='panel'),
    path('edit-profile/', views.register, name='edit_profile'),
    #links para ver el menu de los qr
    path('menu-gallipan/', views.image_management_view2, name='menu-gallipan'),
    path('menu-muelle/', views.menu_muelle, name='menu-muelle'),
    path('side/', views.side, name='side'),
    path('inicio/', views.gestion_inicio, name='inicio'),
    #links de qr
    path('gallipan/', views.gestion_gallipan, name='gestionGallipan'),
    path('muelle/', views.gestion_muelle, name='gestionMuelle'),
    path('login/gestion_de_imagenes/', views.image_management_view, name='image_management_view'),
    path('delete/<int:imagen_id>/', views.delete_image, name='delete_image'),
    path('delete_muelle/<int:imagen_id>/', views.delete_image_muelle, name='delete_image_muelle'),


]
