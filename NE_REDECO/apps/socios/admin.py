from django.contrib import admin
from .models import CatalogoSepomex, Socio

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ('clave_condusef', 'nombre_institucion', 'tipo_entidad', 'estado_republica', 'estatus', 'fecha_registro')
    search_fields = ('clave_condusef', 'nombre_institucion')
    list_filter = ('estatus', 'tipo_entidad', 'estado_republica')
    readonly_fields = ('fecha_registro',)

@admin.register(CatalogoSepomex)
class CatalogoSepomexAdmin(admin.ModelAdmin):
    list_display = ('codigo_postal', 'descripcion_colonia', 'descripcion_delegacion_municipio', 'descripcion_entidad_federativa')
    search_fields = ('codigo_postal', 'descripcion_colonia')
