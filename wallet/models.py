from django.db import models
from django.utils import timezone as tz
from django.contrib.auth import get_user_model

User = get_user_model()

class Timestamp(models.Model):
    creado_en = models.DateTimeField(auto_now=True)
    actualizado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class CategoriaMovimiento(models.Model):
    class TipoMovimiento(models.TextChoices):
        GASTO = "G", "Gasto"
        INGRESO = "I", "Ingreso"

    tipo_movimiento = models.CharField(
        max_length=1,
        choices=TipoMovimiento.choices,
        default=TipoMovimiento.GASTO
    )
    nombre = models.CharField(max_length=125)

    def __str__(self):
        return self.nombre


class Movimiento(Timestamp):
    categoria = models.ForeignKey(
        CategoriaMovimiento,
        related_name="movimientos",
        on_delete=models.PROTECT
    )

    descripcion = models.TextField()
    monto = models.DecimalField(
        decimal_places=2,
        max_digits=7
    )
    fecha = models.DateField(default=tz.now)
    registrado_por = models.ForeignKey(
        User,
        related_name="movimientos",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    def __str__(self):
        return f"{self.descripcion}" 

    class Meta:
        ordering = ["-fecha"]
        indexes = [
            models.Index(
                fields=["-fecha"]
            )
        ]