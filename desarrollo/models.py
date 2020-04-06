from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class Item(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=100, default='en desarrollo', null=False)
    version = models.CharField(max_length=100, null=False, default='1.0.0')
    complejidad = models.PositiveIntegerField(default=5, null=False,
                                              validators=[MinValueValidator(1), MaxValueValidator(10)])
    descripcion = models.CharField(max_length=200, null=True)
    tipo_item = models.ForeignKey('administracion.TipoItem', on_delete=models.CASCADE)
    proyecto = models.ForeignKey('administracion.Proyecto', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class AtributoParticular(models.Model):
    item = models.ManyToManyField('desarrollo.Item')
    nombre = models.CharField(max_length=200, null=False)
    tipo = models.CharField(max_length=100, null=False)
    valor = models.CharField(max_length=300)
    es_requerido = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
