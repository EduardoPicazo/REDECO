import os
import django
import sys

# Asegurar que el entorno de Django esté configurado correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NE_REDECO.settings')
django.setup()

from apps.consultas.models import Causa, Producto

def run():
    print("Iniciando parche de catálogo de Causas...")
    
    # 1. Obtenemos un producto genérico o lo creamos si no existe
    producto_generico = Producto.objects.first()
    
    if not producto_generico:
        producto_generico = Producto.objects.create(
            clave_producto=999999,
            tipo_operacion='General',
            producto='Producto Genérico (Creado por Sistema)'
        )
        print("INFO: Se creó un Producto Genérico para asociar la causa.")

    # 2. Creamos o actualizamos la causa 1211
    causa, created = Causa.objects.get_or_create(
        clave_causa=1211,
        defaults={
            'descripcion_causa': 'Consulta de estado de cuenta',
            'producto': producto_generico
        }
    )
    
    if created:
        print(f"ÉXITO: La causa 1211 ('{causa.descripcion_causa}') ha sido insertada exitosamente, asociada al producto [{producto_generico.clave_producto}].")
    else:
        print(f"INFO: La causa 1211 ya existía en la base de datos ('{causa.descripcion_causa}').")

if __name__ == '__main__':
    run()
