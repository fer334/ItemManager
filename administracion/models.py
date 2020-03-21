from django.db import models


class Rol(models.Model):
    """
    Clase que representa los roles de los usuarios en los proyectos
    :param Id_Rol: Identificador del Rol
    :param Nombre: Nombre a ser asignado al Rol
    :param Permisos: lista de permisos asociados a ese Rol
    """


    Nombre =  models.CharField( max_length= 150, default= 'null')
    Permisos = models.CharField(max_length= 1000, default='null')




    def __str__(self):
        return (self.Nombre)

class UsuarioxRol(models.Model):
    """ Clase en la cual se definen los roles del usuario
    :param Id: Identificador del rol correspondiente
    :param Usuario: Usuario al cual le corresponde dicho rol
    :param rol: Rol del usuario
    """

    Usuario = models.ForeignKey('login.usr')
    rol = models.ForeignKey('Rol')


    def __str__(self):
        return self.Id


