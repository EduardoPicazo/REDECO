from django.db import models

class Producto(models.Model):
    clave_producto = models.BigIntegerField(
        primary_key=True,
        help_text="Clave compuesta oficial por tipo de operación, producto y subproducto"
    )
    tipo_operacion = models.CharField(max_length=255)
    producto = models.CharField(max_length=255)
    # Puede ser null ya que algunos productos generales no tienen subproducto definido
    subproducto = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        # Muestra la clave de producto y una porción del nombre para fácil lectura
        return f"[{self.clave_producto}] {self.producto}"


class Causa(models.Model):
    # Nota: Django ya crea automáticamente un campo `id` autoincremental (models.BigAutoField)
    clave_causa = models.IntegerField()
    descripcion_causa = models.TextField()
    
    # Llave foránea hacia Producto (muchas Causas pertenecen a un Producto)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='causas'
    )

    class Meta:
        db_table = 'causas'
        verbose_name = 'Causa'
        verbose_name_plural = 'Causas'

    def __str__(self):
        return f"[{self.clave_causa}] {self.descripcion_causa[:50]}..."

from django.core.exceptions import ValidationError

class Queja(models.Model):
    ESTADO_CHOICES = [
        (1, 'Abierto/En proceso'),
        (2, 'Concluido/Cerrado')
    ]

    folio = models.CharField(max_length=50, primary_key=True, blank=True, verbose_name="Folio")
    fecha_consulta = models.DateField(verbose_name="Fecha de Consulta")
    estado = models.IntegerField(choices=ESTADO_CHOICES, default=1, verbose_name="Estado")
    fecha_cierre = models.DateField(null=True, blank=True, verbose_name="Fecha de Cierre")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='quejas', verbose_name="Producto")
    causa = models.ForeignKey(Causa, on_delete=models.CASCADE, related_name='quejas', verbose_name="Causa")
    medio = models.CharField(max_length=100, default='Teléfono', verbose_name="Medio de Recepción")
    socio_referencia = models.ForeignKey('socios.Socio', on_delete=models.CASCADE, null=True, blank=True, related_name='quejas', verbose_name="Socio de Referencia")

    class Meta:
        db_table = 'quejas'
        verbose_name = 'Queja'
        verbose_name_plural = 'Quejas'

    def __str__(self):
        return f"Folio {self.folio} - {self.get_estado_display()}"

    def clean(self):
        super().clean()
        if self.estado == 2 and not self.fecha_cierre:
            raise ValidationError({'fecha_cierre': 'La fecha de cierre es obligatoria cuando el estado es Concluido/Cerrado.'})

    def save(self, *args, **kwargs):
        if not self.folio:
            year = self.fecha_consulta.strftime('%y')
            month = self.fecha_consulta.strftime('%m')
            
            # Contar registros en el mismo mes y año
            count = Queja.objects.filter(
                fecha_consulta__year=self.fecha_consulta.year,
                fecha_consulta__month=self.fecha_consulta.month
            ).count()
            
            consecutivo = count + 1
            self.folio = f"{year}{month}{consecutivo:02d}"
            
        super().save(*args, **kwargs)

