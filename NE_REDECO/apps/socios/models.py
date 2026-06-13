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


class Socio(models.Model):
    TIPO_ENTIDAD_CHOICES = [
        ('Caja de Ahorro', 'Caja de Ahorro'),
        ('Sucursal', 'Sucursal'),
        ('Sofipo', 'Sociedad Financiera Popular (SOFIPO)'),
        ('Banco', 'Banco'),
        ('Otro', 'Otro'),
    ]

    ESTADOS_CHOICES = [
        ('Aguascalientes', 'Aguascalientes'),
        ('Baja California', 'Baja California'),
        ('Baja California Sur', 'Baja California Sur'),
        ('Campeche', 'Campeche'),
        ('Chiapas', 'Chiapas'),
        ('Chihuahua', 'Chihuahua'),
        ('Ciudad de México', 'Ciudad de México'),
        ('Coahuila', 'Coahuila'),
        ('Colima', 'Colima'),
        ('Durango', 'Durango'),
        ('Guanajuato', 'Guanajuato'),
        ('Guerrero', 'Guerrero'),
        ('Hidalgo', 'Hidalgo'),
        ('Jalisco', 'Jalisco'),
        ('Estado de México', 'Estado de México'),
        ('Michoacán', 'Michoacán'),
        ('Morelos', 'Morelos'),
        ('Nayarit', 'Nayarit'),
        ('Nuevo León', 'Nuevo León'),
        ('Oaxaca', 'Oaxaca'),
        ('Puebla', 'Puebla'),
        ('Querétaro', 'Querétaro'),
        ('Quintana Roo', 'Quintana Roo'),
        ('San Luis Potosí', 'San Luis Potosí'),
        ('Sinaloa', 'Sinaloa'),
        ('Sonora', 'Sonora'),
        ('Tabasco', 'Tabasco'),
        ('Tamaulipas', 'Tamaulipas'),
        ('Tlaxcala', 'Tlaxcala'),
        ('Veracruz', 'Veracruz'),
        ('Yucatán', 'Yucatán'),
        ('Zacatecas', 'Zacatecas'),
    ]

    ESTATUS_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    clave_condusef = models.CharField(max_length=50, unique=True, verbose_name="Clave CONDUSEF")
    nombre_institucion = models.CharField(max_length=255, verbose_name="Nombre de la Institución")
    tipo_entidad = models.CharField(max_length=50, choices=TIPO_ENTIDAD_CHOICES, verbose_name="Tipo de Entidad")
    estado_republica = models.CharField(max_length=50, choices=ESTADOS_CHOICES, verbose_name="Estado de la República")
    estatus = models.CharField(max_length=15, choices=ESTATUS_CHOICES, default='Activo', verbose_name="Estatus")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        db_table = 'socio'
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'

    def __str__(self):
        return f"[{self.clave_condusef}] {self.nombre_institucion}"
