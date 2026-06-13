import os
import django
import sys
import random
from datetime import date, timedelta

# Configurar entorno de Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NE_REDECO.settings')
django.setup()

from apps.consultas.models import Producto, Causa, Queja
from apps.socios.models import Socio

def seed():
    print("Iniciando inyección de datos de prueba (Seed)...")
    
    # 1. Limpieza de Quejas Previas
    # Borramos todas las quejas para evitar inflar la base de datos cada vez que se ejecute el script
    # y para probar limpiamente la generación de folios.
    Queja.objects.all().delete()
    print("- Se han limpiado las Quejas previas.")

    # 2. Catálogo de Productos
    productos_data = [
        {'clave_producto': 1001, 'tipo_operacion': 'Crédito', 'producto': 'Crédito AVIO'},
        {'clave_producto': 1002, 'tipo_operacion': 'Crédito', 'producto': 'Crédito Refaccionario'},
        {'clave_producto': 1003, 'tipo_operacion': 'Crédito', 'producto': 'Crédito con Aval'},
        {'clave_producto': 2001, 'tipo_operacion': 'Tarjeta', 'producto': 'Tarjeta de Crédito'},
    ]
    
    productos_creados = []
    for p in productos_data:
        obj, created = Producto.objects.get_or_create(
            clave_producto=p['clave_producto'],
            defaults={'tipo_operacion': p['tipo_operacion'], 'producto': p['producto']}
        )
        productos_creados.append(obj)
    print(f"- Se validaron/crearon {len(productos_creados)} Productos.")

    # 3. Catálogo de Causas
    causas_data = [
        {'clave_causa': 1211, 'descripcion_causa': 'Consulta de estado de cuenta', 'producto': productos_creados[0]},
        {'clave_causa': 1212, 'descripcion_causa': 'Cargos no reconocidos', 'producto': productos_creados[3]},
        {'clave_causa': 1213, 'descripcion_causa': 'Bloqueo de cuenta injustificado', 'producto': productos_creados[1]},
        {'clave_causa': 1214, 'descripcion_causa': 'Problemas con el cobro de intereses', 'producto': productos_creados[2]},
    ]
    
    causas_creadas = []
    for c in causas_data:
        obj, created = Causa.objects.get_or_create(
            clave_causa=c['clave_causa'],
            defaults={'descripcion_causa': c['descripcion_causa'], 'producto': c['producto']}
        )
        causas_creadas.append(obj)
    print(f"- Se validaron/crearon {len(causas_creadas)} Causas (Incluyendo 1211).")

    # 4. Socios de Prueba
    socios_data = [
        {'clave_condusef': 'SOCIO-001', 'nombre': 'Caja Popular Alianza', 'entidad': 'Caja de Ahorro', 'estado': 'Jalisco'},
        {'clave_condusef': 'SOCIO-002', 'nombre': 'Cooperativa Regional de Sur', 'entidad': 'Caja de Ahorro', 'estado': 'Oaxaca'},
        {'clave_condusef': 'SOCIO-003', 'nombre': 'Financiera Sofipo Plus', 'entidad': 'Sofipo', 'estado': 'Ciudad de México'},
    ]
    
    socios_creados = []
    for s in socios_data:
        obj, created = Socio.objects.get_or_create(
            clave_condusef=s['clave_condusef'],
            defaults={
                'nombre_institucion': s['nombre'],
                'tipo_entidad': s['entidad'],
                'estado_republica': s['estado']
            }
        )
        socios_creados.append(obj)
    print(f"- Se validaron/crearon {len(socios_creados)} Socios de prueba.")

    # 5. Generación de Quejas (10 a 15)
    meses_pruebas = [4, 5, 6] # Abril, Mayo, Junio
    total_quejas = random.randint(10, 15)
    
    for i in range(total_quejas):
        # Fechas aleatorias
        mes = random.choice(meses_pruebas)
        dia = random.randint(1, 28)
        fecha_consulta = date(2026, mes, dia)
        
        # Estado (1=Abierto, 2=Cerrado)
        estado = random.choice([1, 2])
        fecha_cierre = None
        
        if estado == 2:
            # Si está cerrada, la fecha de cierre es entre 1 y 15 días después
            fecha_cierre = fecha_consulta + timedelta(days=random.randint(1, 15))
            
        # Producto, Causa y Socio aleatorio
        causa_random = random.choice(causas_creadas)
        
        Queja.objects.create(
            fecha_consulta=fecha_consulta,
            estado=estado,
            fecha_cierre=fecha_cierre,
            producto=causa_random.producto, # Asegura congruencia entre producto y causa
            causa=causa_random,
            medio=random.choice(['Teléfono', 'Presencial', 'Correo', 'Portal Web']),
            socio_referencia=random.choice(socios_creados)
        )
        
    print(f"- ¡ÉXITO! Se generaron {total_quejas} quejas automáticas simuladas para Abril-Junio 2026.")
    print("  Los folios automáticos (YYMMNN) fueron generados y guardados en la BD.")

if __name__ == '__main__':
    seed()
