import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from apps.socios.models import CatalogoSepomex
from apps.consultas.models import Producto, Causa

class Command(BaseCommand):
    help = 'Carga los catálogos de Sepomex y Productos/Causas desde archivos Excel en la carpeta data/'

    def handle(self, *args, **options):
        # Detectar dinámicamente la ruta de la carpeta 'data/' un nivel arriba de BASE_DIR
        parent_dir = os.path.dirname(settings.BASE_DIR)
        data_dir = os.path.join(parent_dir, 'backend', 'data')
        
        archivo_sepomex = os.path.join(data_dir, 'Catálogo Sepomex.xlsx')
        archivo_causas = os.path.join(data_dir, 'CAT-PRODUCTOS-CAUSAS.xlsx')

        self.cargar_sepomex(archivo_sepomex)
        self.cargar_productos_causas(archivo_causas)

    def safe_int(self, value):
        if pd.isna(value) or value is None or value == '':
            return None
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return None

    def cargar_sepomex(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(self.style.ERROR(f'El archivo no existe: {filepath}'))
            return

        self.stdout.write(self.style.WARNING('Iniciando carga de Catálogo Sepomex...'))
        count = 0
        try:
            # Los encabezados reales en el archivo de Sepomex están en la fila 3 (índice 2)
            df = pd.read_excel(filepath, sheet_name='Hoja1', header=2)
            
            # Limpiar espacios en los nombres de las columnas para evitar errores
            df.columns = df.columns.str.strip()
            
            # Rellenar NaNs con string vacío
            df = df.fillna('')
            records = df.to_dict('records')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al leer el archivo Excel {filepath}: {e}'))
            return

        with transaction.atomic():
            for row in records:
                try:
                    c_loc = self.safe_int(row.get('Clave localidad'))
                    d_loc = str(row.get('Descripción de localidad', '')).strip() if row.get('Descripción de localidad') else None
                    
                    cp = str(row.get('Código Postal', '')).strip()
                    if cp:
                        # Rellenar con 0 a la izquierda si el CP perdió el 0 inicial
                        cp = cp.zfill(5)
                    else:
                        # Si el código postal está vacío o inválido, saltar
                        continue
                        
                    obj, created = CatalogoSepomex.objects.get_or_create(
                        codigo_postal=cp,
                        clave_entidad_federativa=self.safe_int(row.get('Clave de entidad federativa', 0)),
                        descripcion_entidad_federativa=str(row.get('Descripción de entidad federativa', '')).strip(),
                        clave_delegacion_municipio=self.safe_int(row.get('Clave de delegación/municipio', 0)),
                        descripcion_delegacion_municipio=str(row.get('Descripción de delegación/municipio', '')).strip(),
                        clave_localidad=c_loc,
                        descripcion_localidad=d_loc,
                        clave_colonia=self.safe_int(row.get('Clave colonia', 0)),
                        descripcion_colonia=str(row.get('Descripción de colonia', '')).strip(),
                    )
                    if created:
                        count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error en fila Sepomex (CP {row.get("Código Postal")}): {e}'))
                
        self.stdout.write(self.style.SUCCESS(f'Se cargaron {count} registros nuevos de Sepomex exitosamente.'))

    def cargar_productos_causas(self, filepath):
        if not os.path.exists(filepath):
            self.stdout.write(self.style.ERROR(f'El archivo no existe: {filepath}'))
            return

        self.stdout.write(self.style.WARNING('Iniciando carga de Productos y Causas...'))
        count_prod = 0
        count_causa = 0
        
        try:
            # Los encabezados están en la primera fila (índice 0)
            df = pd.read_excel(filepath, sheet_name='CAT-PRODUCTOS-CAUSAS', header=0)
            
            # Limpiar espacios en los nombres de columnas
            df.columns = df.columns.str.strip()
            
            df = df.fillna('')
            records = df.to_dict('records')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al leer el archivo Excel {filepath}: {e}'))
            return

        with transaction.atomic():
            for row in records:
                try:
                    clave_prod = self.safe_int(row.get('CLAVE DE TIPO DE OPERACIÓN, PRODUCTO Y SUBPRODUCTO'))
                    if clave_prod is None:
                        continue
                        
                    # Registrar primero el Producto
                    producto, created_prod = Producto.objects.get_or_create(
                        clave_producto=clave_prod,
                        defaults={
                            'tipo_operacion': str(row.get('TIPO DE OPERACIÓN', '')).strip(),
                            'producto': str(row.get('PRODUCTO', '')).strip(),
                            'subproducto': str(row.get('SUBPRODUCTO', '')).strip() if row.get('SUBPRODUCTO') else None,
                        }
                    )
                    if created_prod:
                        count_prod += 1

                    # Registrar la Causa asociada
                    clave_causa = self.safe_int(row.get('CLAVE CAUSA'))
                    if clave_causa is not None:
                        causa, created_causa = Causa.objects.get_or_create(
                            clave_causa=clave_causa,
                            producto=producto,
                            defaults={
                                'descripcion_causa': str(row.get('DESCRIPCIÓN DE LA CAUSA', '')).strip(),
                            }
                        )
                        if created_causa:
                            count_causa += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error en fila Producto/Causa (Prod {row.get("CLAVE DE TIPO DE OPERACIÓN, PRODUCTO Y SUBPRODUCTO")}): {e}'))

        self.stdout.write(self.style.SUCCESS(f'Se cargaron {count_prod} productos y {count_causa} causas exitosamente.'))
