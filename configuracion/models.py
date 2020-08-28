from django.db import models
from desarrollo.models import Item
from django.utils.timezone import now
from desarrollo.models import Fase
# Create your models here.


class LineaBase(models.Model):
    """
    clase que representa a una linea base
    """
    #: lista de items de la linea base
    items = models.ManyToManyField(Item)
    fecha_creacion = models.DateField(default=now)
    creador = models.ForeignKey('login.Usuario', on_delete=models.CASCADE, default=None, null=True)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, null=False)
    ESTADO_CERRADA = 'Cerrada'
    ESTADO_ROTA = 'Rota'
    TIPO_PARCIAL = 'Parcial'
    TIPO_TOTAL = 'Total'
    tipo = models.CharField(max_length=100, default=TIPO_PARCIAL)
    #: estado actual de la linea base
    estado = models.CharField(max_length=100, default=ESTADO_CERRADA, null=False)


class Solicitud(models.Model):
    """
    Clase que representa la solicitud de cambios
    """
    items_a_modificar = models.ManyToManyField(Item)
    fecha_solicitud = models.DateField(default=now)
    solicitado_por = models.ForeignKey('login.Usuario', on_delete=models.CASCADE, default=None, null=True)
    linea_base = models.ForeignKey('configuracion.LineaBase', on_delete=models.CASCADE, default=None, null=True)
    justificacion = models.CharField(max_length=200, null=False)
    solicitud_activa = models.BooleanField(default=True)

    def ha_votado(self, votante):
        for voto in self.votoruptura_set.all():
            if voto.votante == votante:
                return True
        return False

class VotoRuptura(models.Model):
    """
    Clase que representa un voto del comite
    """
    solicitud = models.ForeignKey(Solicitud, null=False, on_delete=models.DO_NOTHING)
    votante = models.ForeignKey('login.Usuario', null=False, on_delete=models.DO_NOTHING)
    valor_voto = models.BooleanField(default=False) #TRUE a favor FALSE en contra
    fecha_voto = models.DateField(default=now)

