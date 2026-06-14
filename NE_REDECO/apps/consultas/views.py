from django.shortcuts import render
# pyrefly: ignore [missing-import]
from apps.socios.models import CatalogoSepomex
# pyrefly: ignore [missing-import]
from apps.consultas.models import Producto, Causa

def demo_busqueda(request):
    cp = request.GET.get('cp', '').strip()
    producto = request.GET.get('producto', '').strip()
    causa = request.GET.get('causa', '').strip()
    
    resultados_sepomex = None
    resultados_productos = None
    
    if cp:
        # Filtramos por CP exacto y limitamos a 20
        resultados_sepomex = CatalogoSepomex.objects.filter(codigo_postal=cp)[:20]
        
    if producto or causa:
        qs_productos = Producto.objects.all()
        if producto:
            qs_productos = qs_productos.filter(producto__icontains=producto)
        if causa:
            qs_productos = qs_productos.filter(causas__descripcion_causa__icontains=causa).distinct()
        resultados_productos = qs_productos[:20]
        
    return render(request, 'consultas/dashboard.html', {
        'resultados_sepomex': resultados_sepomex,
        'resultados_productos': resultados_productos
    })

def home(request):
    return render(request, 'consultas/home.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from .models import Queja
from .forms import QuejaForm
from django.contrib import messages
from datetime import date

from apps.socios.models import Socio

def captura_queja(request):
    socios_disponibles = Socio.objects.all()

    if request.method == 'POST':
        form = QuejaForm(request.POST)
        socio_id = request.POST.get('socio_id')
        estado_socio = request.POST.get('estado')
        municipio_socio = request.POST.get('municipio')
        localidad_socio = request.POST.get('localidad')
        
        if not socio_id or not estado_socio or not municipio_socio or not localidad_socio:
            messages.error(request, "Debe seleccionar un socio y asegurarse de que Estado, Municipio y Localidad no estén vacíos.")
            return render(request, 'consultas/captura_queja.html', {
                'form': form,
                'socios_disponibles': socios_disponibles
            })
        
        if form.is_valid():
            queja = form.save(commit=False)
            if socio_id:
                # El id real en la BD se llama clave_condusef, que es la llave primaria en tu diseño, 
                # o el id autogenerado si no lo definiste como PK. Vamos a usar la llave primaria que definiste.
                # Nota: Si clave_condusef es char, socio_id será ese string.
                queja.socio_referencia_id = socio_id
            queja.save()
            messages.success(request, f"¡Queja registrada exitosamente!")
            return redirect('detalle_ticket', folio=queja.folio)
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = QuejaForm(initial={'fecha_consulta': date.today()})

    return render(request, 'consultas/captura_queja.html', {
        'form': form,
        'socios_disponibles': socios_disponibles
    })

def detalle_ticket(request, folio):
    queja = get_object_or_404(Queja, folio=folio)
    return render(request, 'consultas/ticket_queja.html', {'queja': queja})

def cierre_trimestral(request):
    # GET: Mostrar tabla con filtros
    if request.method == 'GET':
        trimestre = request.GET.get('trimestre', '')
        anio = request.GET.get('anio', str(date.today().year))
        
        quejas = Queja.objects.all()
        
        if anio:
            quejas = quejas.filter(fecha_consulta__year=anio)
            
        if trimestre:
            t = int(trimestre)
            meses = []
            if t == 1: meses = [1, 2, 3]
            elif t == 2: meses = [4, 5, 6]
            elif t == 3: meses = [7, 8, 9]
            elif t == 4: meses = [10, 11, 12]
            quejas = quejas.filter(fecha_consulta__month__in=meses)
            
        return render(request, 'consultas/cierre_trimestral.html', {
            'quejas': quejas.order_by('-fecha_consulta'),
            'anios': range(2024, 2030),
            'trimestre_actual': trimestre,
            'anio_actual': anio
        })
        
    # POST: Generar JSON
    elif request.method == 'POST':
        queja_ids = request.POST.getlist('queja_ids')
        quejas_seleccionadas = Queja.objects.filter(folio__in=queja_ids)
        
        lote_json = []
        for q in quejas_seleccionadas:
            lote_json.append({
                "folio": q.folio,
                "fecha_consulta": q.fecha_consulta.strftime('%Y-%m-%d'),
                "estado": q.estado,
                "fecha_cierre": q.fecha_cierre.strftime('%Y-%m-%d') if q.fecha_cierre else None,
                "producto": q.producto.clave_producto,
                "causa": q.causa.clave_causa,
                "medio": q.medio
            })
            
        response = JsonResponse(lote_json, safe=False, json_dumps_params={'indent': 4})
        response['Content-Disposition'] = 'attachment; filename="lote_condusef.json"'
        return response
