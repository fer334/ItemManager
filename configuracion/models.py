from django.db import models

# Create your models here.


class LineaBase(models.Model):
    """
    clase que representa a una linea base
    """
    #: lista de items de la linea base
    items = models.ManyToManyField('Item')
    ESTADO_CERRADA = 'Cerrada'
    ESTADO_ROTA = 'Rota'
    #: estado actual de la linea base
    estado = models.CharField(max_length=100, default=ESTADO_CERRADA, null=False)



