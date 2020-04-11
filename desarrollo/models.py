"""
Mapeador objeto-relacional en el que es posible definir la estructura de la base de datos utilizando código Python.
"""
from django.db import models
from administracion.models import Fase


# Create your models here.

class Item(models.Model):
    """
    clase que representa a los ítems que son instanciados a partir de un tipo de ítem
    """
    #: nombre que identifica al ítem
    nombre = models.CharField(max_length=200, null=False)
    #: estado actual, puede tomar los valores: en desarrollo, pendiente de aprobación, aprobado, desactivado,
    # en revisión, en línea base
    estado = models.CharField(max_length=100, default='en desarrollo', null=False)
    #: version actual del ítem que va cambiando luego de cada nueva relación y cada modificación de sus datos
    version = models.PositiveIntegerField(null=False, default=1)
    #: valor que define el impacto del ítem en el proyecto. Toma valores enteros entre 1 y 10
    complejidad = models.PositiveIntegerField(default=5, null=False)
    #: comentarios opcionales para describir al ítem
    descripcion = models.CharField(max_length=200, null=True)
    #: tipo que tendrá el ítem, de eso dependen sus atributos particulares
    tipo_item = models.ForeignKey('administracion.TipoItem', on_delete=models.CASCADE)
    #: fase del proyecto en la que se crea el ítem
    fase = models.ForeignKey('administracion.Fase', on_delete=models.CASCADE, default=None)
    # constantes del modelo
    ESTADO_DESARROLLO = 'en desarrollo'
    ESTADO_PENDIENTE = 'Pendiente de Aprobacion'
    ESTADO_APROBADO = 'Aprobado'
    ESTADO_REVISION = 'En Revision'
    ESTADO_LINEABASE = 'En Linea Base'
    ESTADO_DESACTIVADO = 'Desactivado'

    def __str__(self):
        return self.nombre


class AtributoParticular(models.Model):
    """
    Esta clase representa cada uno de los atributos extra que tiene un ítem dependiendo de su tipo de ítem
    """
    #: item al cual pertenecen estos atributos
    item = models.ForeignKey('desarrollo.Item', on_delete=models.CASCADE, default=None)
    #: nombre del atributo
    nombre = models.CharField(max_length=200, null=False)
    #: tipo del atributo, puede tomar valores: text, numeric, file, date
    tipo = models.CharField(max_length=100, null=False)
    #: valor que es almacenado dentro del atributo
    valor = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre