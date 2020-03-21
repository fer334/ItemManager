from django.db import models
from login.models import usr


# Create your models here.

class Proyecto(models.Model):
    """
    Clase que representa a los proyectos que administrará el sistema con sus respectivos atributos

    :param nombre: nombre del proyecto
    :param fecha_inicio: fecha en la que el proyecto comienza
    :param estado: estado actual del proyecto, puede variar entre iniciado, en ejecución, cancelado, finalizado
    :param numero_fases = cantidad de fases que tiene el proyecto
    :param cant_comite = cantidad de miembros que deberá tener el comité, debe ser impar y mayor o igual a 3
    :param fases: lista de fases del proyecto
    :param gerente: usuario que toma el rol de gerente del proyecto
    :param comite: conjunto impar de usuarios que conforma el comité para el proyecto
    :param participantes: equipo de usuarios que participa en el proyecto
    """
    nombre = models.CharField(max_length=200, default='null')
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    estado = models.CharField(max_length=200, default='iniciado')
    numero_fases = models.IntegerField(default=0)
    cant_comite = models.IntegerField(default=0)
    # ponerse de acuerdo después para fases
    # fases = models.ForeignKey('Fase', on_delete=models.CASCADE)
    # para el gerente sería mejor que el usuario tenga un foreign key a proyectos
    gerente = models.CharField(max_length=700, default='null')
    comite = models.CharField(max_length=700, default='null')
    # ponerse de acuerdo después para participantes
    participantes = models.ManyToManyField('login.usr')
    # este no: tipos_de_item = models.ManyToManyField('TipoItem')

    def __str__(self):
        return self.nombre


class Fase(models.Model):
    """
    Esta clase representa las fases

    :param nombre: Se almacena el nombre de la fase
    :type string
    :param descripcion: Descripcion de la fase
    :type string
    :param estado: Estado de la fase, iniciada, cerrada etc.
    :type string
    :param proyecto: Proyecto asociado a la fase
    :type Proyecto
    """
    nombre = models.CharField(max_length=200, null=False)
    descripcion = models.CharField(max_length=400, null=True)
    estado = models.CharField(max_length=200, default='abierta')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)


class TipoItem(models.Model):
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

    nombre = models.CharField(max_length=200)
    descripcion = models.CharField( max_length=800)
    prefijo = models.CharField(max_length=5)
    proyecto = models.ManyToManyField('Proyecto')

    def __str__(self):
        return self.nombre


class PlantillaAtributo(models.Model):
    """
    Esta clase representa las plantilla de atributos usada por el tipo de item

    :param nombre: Se almacena el nombre del tipo de item
    :type string
    :param tipo: Tipo del item a ser instanciado
    :type string
    :param proyecto: TipoItem asociado a la plantilla
    :type TipoItem

    """
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

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


