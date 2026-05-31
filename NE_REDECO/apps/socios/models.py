from django.db import models

class CatalogoSepomex(models.Model):
    codigo_postal = models.CharField(max_length=5)
    clave_entidad_federativa = models.IntegerField()
    descripcion_entidad_federativa = models.CharField(max_length=100)
    clave_delegacion_municipio = models.IntegerField()
    descripcion_delegacion_municipio = models.CharField(max_length=150)
    
    # Es muy común en SEPOMEX que algunas localidades vengan vacías
    clave_localidad = models.IntegerField(null=True, blank=True)
    descripcion_localidad = models.CharField(max_length=150, null=True, blank=True)
    
    clave_colonia = models.IntegerField()
    descripcion_colonia = models.CharField(max_length=150)

    class Meta:
        db_table = 'catalogo_sepomex'
        verbose_name = 'Registro Sepomex'
        verbose_name_plural = 'Catálogo Sepomex'
        # Índice explícito para acelerar las búsquedas predictivas por CP
        indexes = [
            models.Index(fields=['codigo_postal'], name='idx_codigo_postal'),
        ]

    def __str__(self):
        return f"{self.codigo_postal} - {self.descripcion_colonia}, {self.descripcion_delegacion_municipio}"

