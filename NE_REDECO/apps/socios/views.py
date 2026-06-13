from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Socio, CatalogoSepomex
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
        'tipos_entidad': Socio.TIPO_ENTIDAD_CHOICES,
    }
    return render(request, 'socios/lista_socios.html', context)


def buscar_cp(request):
    cp = request.GET.get('cp', '').strip()
    if not cp or len(cp) != 5:
        return JsonResponse({'error': 'Código postal inválido'}, status=400)
        
    resultados = CatalogoSepomex.objects.filter(codigo_postal=cp)
    
    if not resultados.exists():
        return JsonResponse({'error': 'Código postal no encontrado'}, status=404)
        
    # Asumimos que para un mismo CP, el estado y el municipio son los mismos
    primer_registro = resultados.first()
    estado = primer_registro.descripcion_entidad_federativa
    municipio = primer_registro.descripcion_delegacion_municipio
    
    # Obtenemos la lista de colonias (sin duplicados)
    colonias = list(resultados.values_list('descripcion_colonia', flat=True).distinct().order_by('descripcion_colonia'))
    
    return JsonResponse({
        'estado': estado,
        'municipio': municipio,
        'colonias': colonias
    })

def agregar_socio(request):
    if request.method == 'POST':
        clave_condusef = request.POST.get('clave_condusef', '').strip()
        nombre_institucion = request.POST.get('nombre_institucion', '').strip()
        tipo_entidad = request.POST.get('tipo_entidad', '').strip()
        codigo_postal = request.POST.get('codigo_postal', '').strip()
        estado_republica = request.POST.get('estado_republica', '').strip()
        municipio = request.POST.get('municipio', '').strip()
        colonia = request.POST.get('colonia', '').strip()
        estatus = request.POST.get('estatus', '').strip()
        
        # Validación básica
        if not all([clave_condusef, nombre_institucion, tipo_entidad, estado_republica]):
            messages.error(request, 'Por favor completa los campos obligatorios.')
            return redirect('lista_socios')
            
        try:
            Socio.objects.create(
                clave_condusef=clave_condusef,
                nombre_institucion=nombre_institucion,
                tipo_entidad=tipo_entidad,
                codigo_postal=codigo_postal,
                estado_republica=estado_republica,
                municipio=municipio,
                colonia=colonia,
                estatus=estatus or 'Activo'
            )
            messages.success(request, 'Socio agregado correctamente.')
        except Exception as e:
            messages.error(request, f'Error al guardar el socio: {str(e)}')
            
        return redirect('lista_socios')
    
    return redirect('lista_socios')
