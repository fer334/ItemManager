from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class usr( AbstractUser ):
    """
    Clase que representa al usuario en la base de datos local

    """
    localId = models.CharField( max_length=200)
    pass
