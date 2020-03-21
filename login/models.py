"""
Mapeador objeto-relacional en el que es posible definir la estructura de la base de datos utilizando código Python.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Usuario(AbstractUser):
    """
    Clase que representa al usuario en la base de datos local que extiende del modelo AbstractUser
    de django
    """
    localId = models.CharField(max_length=200)
    pass
