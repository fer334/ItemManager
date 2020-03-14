"""
Modulo que se encarga de presentar el modelo de la base de datos
"""

from django.db import models


# Create your models here.
class Usuario(models.Model):
    """
    Clase que hereda de models para representar a los usuarios que serán utilizados por el sistema con
    sus atributos respectivos

    """
    nombre_usuario = models.CharField(max_length=100)
    nombre_y_apellido = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    # ¿se queda la contraseña?
    contrasegna = models.CharField(max_length=200, default="empty")
    # implementacion provisional de la lista de permisos: permiso1|permiso2|...
    lista_permisos_sistema = models.CharField(max_length=800)

    def __init__(self, nombre_usuario, nombre_real, email, contrasegna, lista_permisos):
        """
        Constructor de la clase Usuario

        :param nombre_usuario: username para el sistema
        :param nombre_real: nombre y apellidos
        :param email: email para registrarse
        :param contrasegna: contraseña para acceder al sistema
        :param lista_permisos: lista de permisos del sistema para el usuario
        """
        self.nombre_usuario = nombre_usuario
        self.nombre_y_apellido = nombre_real
        self.email = email
        self.contrasegna = contrasegna
        self.lista_permisos_sistema = lista_permisos

    def __str__(self):
        """
        funcion para representar como string la clase usuario
        :return: retorna el nombre de usuario
        """
        return self.nombre_usuario
