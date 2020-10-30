"""
Mapeador objeto-relacional en el que es posible definir la estructura de la base de datos utilizando código Python.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.db.models import Q
from administracion.models import Proyecto


# Create your models here.


class Usuario(AbstractUser):
    """
    Clase que representa al usuario en la base de datos local que extiende del
    modelo AbstractUser de django
    """

    #: Atributo para el campo del Correo Electronico
    email = models.EmailField(
        'Dirección de correo electrónico',
        unique=True,
        blank=False,
    )

    #: Atributo para el campo id en la base de datos de Firebase
    localId = models.CharField(max_length=200)

    #: Atributo para el token dela base de Firebase
    id_token = models.CharField(max_length=100, null=True, default=None)

    #: Atributo para el campo diferenciar usuarios normales de gerentes
    is_gerente = models.BooleanField(
        "Gerente",
        default=False
    )

    def es_participante(self):
        """
        Metodo que comprueba que el usuario participa o no de algun proyecto
        que ha iniciado o que esta en estado de en ejecucion

        :return: retorna True si forma participa y False en caso contrario
        """

        consulta = Q(estado='iniciado') | Q(estado='en ejecucion')
        if Proyecto.objects.filter(consulta, participantes=self.id).count() == 0:
            return False
        else:
            return True


class HistoricalAccesos(models.Model):
    """
    Clase que sirve para guardar datos de auditoría de los accesos al sistema
    """
    #: usuario que realizó la acción
    history_user = models.CharField(max_length=150, default='None')
    #: fecha y hora en la que se realizó la acción
    history_date = models.DateTimeField(default=now)
    #: razón de cambio (nulo por defecto)
    history_change_reason = models.CharField(max_length=200, null=True)
    #: tipo de acción que puede ser o acceder al sistema o salir del sistema
    history_type = models.CharField(max_length=200)
    # constantes
    TIPO_ACCESO = 'Acceso al sistema'
    TIPO_SALIDA = 'Salida del Sistema '
