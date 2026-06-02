from django.shortcuts import render
from apps.socios.models import CatalogoSepomex
from apps.consultas.models import Producto

def demo_busqueda(request):
    cp = request.GET.get('cp', '')
    producto = request.GET.get('producto', '')
    
    resultados_sepomex = None
    resultados_productos = None
    
    if cp:
        # Filtramos por CP exacto y limitamos a 20
        resultados_sepomex = CatalogoSepomex.objects.filter(codigo_postal=cp)[:20]
        
    if producto:
        # Filtramos productos que contengan la palabra y limitamos a 20
        resultados_productos = Producto.objects.filter(producto__icontains=producto)[:20]
        
    return render(request, 'demo.html', {
        'cp': cp,
        'producto': producto,
        'resultados_sepomex': resultados_sepomex,
        'resultados_productos': resultados_productos
    })
