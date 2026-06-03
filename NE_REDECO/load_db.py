import os
import sys
import django
import pandas as pd
import math

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NE_REDECO.settings')
django.setup()

from apps.socios.models import CatalogoSepomex
from django.db import transaction

def run():
    print("Leyendo el archivo Excel...")
    try:
        # skiprows=2 porque el primer renglón es título general y el segundo es vacío/metadatos,
        # los nombres de las columnas están en la fila 3 (índice 2).
        df = pd.read_excel(r'..\backend\data\Catálogo Sepomex.xlsx', skiprows=2)
        # Limpiar espacios al final de los nombres de las columnas
        df.columns = [col.strip() for col in df.columns]
    except Exception as e:
        print(f"Error al leer el excel: {e}")
        return
        
    print(f"Leídos {len(df)} registros. Preparando inserción masiva...")
    
    # Limpiar tabla antes de insertar
    CatalogoSepomex.objects.all().delete()
    
    batch_size = 5000
    objs = []
    
    for index, row in df.iterrows():
        try:
            # Manejo de valores nulos o NaN
            clave_localidad = row['Clave localidad']
            if pd.isna(clave_localidad):
                clave_localidad = None
            else:
                clave_localidad = int(clave_localidad)
                
            desc_localidad = row['Descripción de localidad']
            if pd.isna(desc_localidad):
                desc_localidad = None
            else:
                desc_localidad = str(desc_localidad)

            obj = CatalogoSepomex(
                clave_entidad_federativa=int(row['Clave de entidad federativa']),
                descripcion_entidad_federativa=str(row['Descripción de entidad federativa']),
                codigo_postal=str(row['Código Postal']).zfill(5),
                clave_delegacion_municipio=int(row['Clave de delegación/municipio']),
                descripcion_delegacion_municipio=str(row['Descripción de delegación/municipio']),
                clave_localidad=clave_localidad,
                descripcion_localidad=desc_localidad,
                clave_colonia=int(row['Clave colonia']),
                descripcion_colonia=str(row['Descripción de colonia'])
            )
            objs.append(obj)
        except Exception as e:
            print(f"Error parseando fila {index}: {e}")
            break

        if len(objs) >= batch_size:
            with transaction.atomic():
                CatalogoSepomex.objects.bulk_create(objs)
            print(f"Insertados {index + 1} registros...")
            objs = []
            
    # Insertar los restantes
    if objs:
        with transaction.atomic():
            CatalogoSepomex.objects.bulk_create(objs)
        print("Inserción de remanentes completada.")
        
    print("¡Carga masiva finalizada!")
    print(f"Total registros en BD: {CatalogoSepomex.objects.count()}")

if __name__ == '__main__':
    run()
