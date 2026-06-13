from django.shortcuts import render
from django.db.models import Q
from .models import Socio

def lista_socios(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    estatus = request.GET.get('estatus', '').strip()

    socios = Socio.objects.all()

    if q:
        socios = socios.filter(
            Q(nombre_institucion__icontains=q) | 
            Q(clave_condusef__icontains=q)
        )
    
    if estado:
        socios = socios.filter(estado_republica=estado)
        
    if estatus:
        socios = socios.filter(estatus=estatus)

    # Ordenar por defecto, o podrías agregar un order_by('nombre_institucion')
    socios = socios.order_by('nombre_institucion')

    context = {
        'socios': socios,
        'estados_disponibles': Socio.ESTADOS_CHOICES,
        'estatus_disponibles': Socio.ESTATUS_CHOICES,
    }
    return render(request, 'socios/lista_socios.html', context)
