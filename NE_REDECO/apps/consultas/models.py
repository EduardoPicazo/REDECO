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

