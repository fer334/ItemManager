from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class usr( AbstractUser ):
    localId = models.CharField( max_length=200)
    pass
