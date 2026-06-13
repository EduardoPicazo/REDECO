from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_socios, name='lista_socios'),
    path('buscar-cp/', views.buscar_cp, name='buscar_cp'),
    path('agregar/', views.agregar_socio, name='agregar_socio'),
]
