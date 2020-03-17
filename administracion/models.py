from django.db import models


# Create your models here.
class Proyecto(models):
    pass

"""
Esta clase representa los tipos de items
"""
class TipoItem(models):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField( max_length=800)
    prefijo = models.CharField(max_length=5)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre


class PlantillaAtributo(models):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre