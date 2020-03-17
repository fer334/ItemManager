from django.db import models


# Create your models here.
class Proyecto(models.Model):
    nombre = models.CharField(max_length=200)
    pass


"""
Esta clase representa los tipos de items

:param nombre: Se almacena el nombre del tipo de item
:type string
:param descripcion: Descripcion del tipo de item
:type string
:param prefijo: Prefijo para mostrarse en todos los items instanciados de esta plantilla
:type string
:param proyecto: Proyecto asociado al Tipo de Item
:type Proyecto
 
"""


class TipoItem(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField( max_length=800)
    prefijo = models.CharField(max_length=5)
    #proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre


"""
Esta clase representa las plantilla de atributos usada por el tipo de item 

:param nombre: Se almacena el nombre del tipo de item
:type string
:param tipo: Tipo del item a ser instanciado
:type string
:param proyecto: TipoItem asociado a la plantilla
:type TipoItem

"""


class PlantillaAtributo(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre