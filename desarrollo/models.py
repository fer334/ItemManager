from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from administracion.models import Fase


# Create your models here.

class Item(models.Model):
    nombre = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=100, default='en desarrollo', null=False)
    version = models.PositiveIntegerField(null=False, default=1)
    complejidad = models.PositiveIntegerField(default=5, null=False,
                                              validators=[MinValueValidator(1), MaxValueValidator(10)])
    descripcion = models.CharField(max_length=200, null=True)
    tipo_item = models.ForeignKey('administracion.TipoItem', on_delete=models.CASCADE)
    fase = models.ForeignKey('administracion.fase', on_delete=models.CASCADE, default=None)

    antecesores = models.ManyToManyField('desarrollo.Item', default=None, related_name='item_desarrollo_antecesores')
    sucesores = models.ManyToManyField('desarrollo.Item', default=None, related_name='item_desarrollo_sucesores')
    padres = models.ManyToManyField('desarrollo.Item', default=None, related_name='item_desarrollo_padres')
    hijos = models.ManyToManyField('desarrollo.Item', default=None, related_name='item_desarrollo_hijos')

    def __str__(self):
        return self.nombre


class AtributoParticular(models.Model):
    item = models.ForeignKey('desarrollo.Item', on_delete=models.CASCADE, default=None)
    nombre = models.CharField(max_length=200, null=False)
    tipo = models.CharField(max_length=100, null=False)
    valor = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre