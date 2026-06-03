from django.shortcuts import render
from apps.socios.models import CatalogoSepomex
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
