from django.db import models

# Create your models here.
from django.db import models


class Edificio(models.Model):
    class TipoEdificio(models.TextChoices):
        RESIDENCIAL = 'residencial', 'Residencial'
        COMERCIAL = 'comercial', 'Comercial'

    nombre = models.CharField(max_length=150)
    direccion = models.CharField('dirección', max_length=255)
    ciudad = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=20,
        choices=TipoEdificio.choices,
        default=TipoEdificio.RESIDENCIAL,
    )

    def __str__(self):
        return f'{self.nombre} ({self.ciudad})'


class Departamento(models.Model):
    nombre_propietario = models.CharField('nombre completo del propietario', max_length=200)
    costo = models.DecimalField('costo del departamento', max_digits=12, decimal_places=2)
    numero_cuartos = models.PositiveSmallIntegerField('número de cuartos')
    edificio = models.ForeignKey(
        Edificio,
        on_delete=models.CASCADE,
        related_name='departamentos',
    )

    def __str__(self):
        return f'{self.nombre_propietario} - {self.edificio.nombre}'