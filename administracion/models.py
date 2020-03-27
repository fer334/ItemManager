"""
Mapeador objeto-relacional en el que es posible definir la estructura de la base de datos utilizando código Python.
"""
from django.db import models


# Create your models here.

class Proyecto(models.Model):
    """
    Clase que representa a los proyectos que administrará el sistema con sus respectivos atributos
    """
    #: nombre: nombre del proyecto
    nombre = models.CharField(max_length=200, null=False)
    #: fecha_inicio: fecha en la que el proyecto comienza
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    #: estado: estado actual del proyecto, puede variar entre iniciado, en ejecución, cancelado, finalizado
    estado = models.CharField(max_length=200, default='iniciado')
    #: numero_fases = cantidad de fases que tiene el proyecto
    numero_fases = models.IntegerField(null=False)
    #: cant_comite = cantidad de miembros que deberá tener el comité, debe ser impar y mayor o igual a 3
    cant_comite = models.IntegerField(null=False)
    #: gerente: usuario que toma el rol de gerente del proyecto
    gerente = models.IntegerField(null=False)
    #: comite: conjunto impar de usuarios que conforma el comité para el proyecto
    comite = models.ManyToManyField('login.Usuario', related_name='usuario_login_comite')
    #: participantes: equipo de usuarios que participa en el proyecto
    participantes = models.ManyToManyField('login.Usuario', related_name='usuario_login_participante')

    def __str__(self):
        return self.nombre

    def es_comite(self, id_usuario):
        """
        función booleana que retorna true si un usuario es parte del comité del proyecto

        :param id_usuario: identificar unico del usuario del que se desea saber si es parte del comité
        :return: retorna True si forma parte y False en caso contrario
        """
        for usuario in self.comite:
            if usuario.id == id_usuario:
                return True
        return False


class Fase(models.Model):
    """
    Esta clase representa las fases
    """
    #: nombre: Se almacena el nombre de la fase
    nombre = models.CharField(max_length=200, null=False)
    #: descripcion: Descripcion de la fase
    descripcion = models.CharField(max_length=400, null=True)
    #: estado: Estado de la fase, iniciada, cerrada etc.
    estado = models.CharField(max_length=200, default='abierta')
    #: proyecto: Proyecto asociado a la fase
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
    descripcion = models.CharField(max_length=800)
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
    nombre = models.CharField(max_length=150, default='null')
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)
    crear_item = models.BooleanField(default=False)
    modificar_item = models.BooleanField(default=False)
    desactivar_item = models.BooleanField(default=False)
    aprobar_item = models.BooleanField(default=False)
    reversionar_item = models.BooleanField(default=False)
    crear_relaciones_ph = models.BooleanField(default=False)
    crear_relaciones_as = models.BooleanField(default=False)
    borrar_relaciones = models.BooleanField(default=False)

    def __str__(self):
        return (self.nombre)


class UsuarioxRol(models.Model):
    """ Clase en la cual se definen los roles del usuario
    :param Id: Identificador del rol correspondiente
    :param Usuario: Usuario al cual le corresponde dicho rol
    :param rol: Rol del usuario
    """

    usuario = models.ForeignKey('login.Usuario', on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.id
