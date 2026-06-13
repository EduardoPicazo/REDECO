"""
URL configuration for NE_REDECO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# pyrefly: ignore [missing-import]
from apps.consultas import views as consultas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Página de inicio (Raíz)
    path('', consultas_views.home, name='home'),
    
    # Módulo de Consultas y Quejas
    path('captura-queja/', consultas_views.captura_queja, name='captura_queja'),
    path('captura/ticket/<str:folio>/', consultas_views.detalle_ticket, name='detalle_ticket'),
    path('cierre/', consultas_views.cierre_trimestral, name='cierre_trimestral'),
    
    # Socios
    path('socios/', include('apps.socios.urls')),
    
    # 2. El buscador que ya tenías funcional
    path('demo/', consultas_views.demo_busqueda, name='demo_busqueda'),
]
