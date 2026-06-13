from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_socios, name='lista_socios'),
]
