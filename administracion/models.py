"""
Mapeador objeto-relacional en el que es posible definir la estructura de la base de datos utilizando código Python.
"""
from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.

class Proyecto(models.Model):
    """
    Clase que representa a los proyectos que administrará el sistema con sus respectivos atributos
    """
    #: nombre del proyecto
    nombre = models.CharField(max_length=200, null=False)
    #: fecha en la que el proyecto comienza
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    #: fecha y hora en la que el proyecto pasa a estado de ejecución
    fecha_ejecucion = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    #: fecha y hora en la que el proyecto pasa a finalizado
    fecha_finalizado = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    #: fecha y hoar en la que el proyecto pasa a cancelado
    fecha_cancelado = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    #: estado actual del proyecto, puede variar entre iniciado, en ejecución, cancelado, finalizado
    estado = models.CharField(max_length=200, default='iniciado')
    #: cantidad de fases que tiene el proyecto
    numero_fases = models.IntegerField(null=False)
    #: cantidad de miembros que deberá tener el comité, debe ser impar y mayor o igual a 3
    cant_comite = models.IntegerField(null=False)
    #: usuario que toma el rol de gerente del proyecto
    gerente = models.IntegerField(null=False)
    #: conjunto impar de usuarios que conforma el comité para el proyecto
    comite = models.ManyToManyField('login.Usuario', related_name='usuario_login_comite')
    #: equipo de usuarios que participa en el proyecto
    participantes = models.ManyToManyField('login.Usuario', related_name='usuario_login_participante')
    #: campo que sirve para realizar auditoría de los objetos del modelo
    history = HistoricalRecords()

    ESTADO_CANCELADO = 'cancelado'
    ESTADO_INICIADO = 'iniciado'
    ESTADO_EN_EJECUCION = 'en ejecucion'
    ESTADO_FINALIZADO = 'finalizado'

    def __str__(self):
        return self.nombre

    def es_comite(self, id_usuario):
        """
        función booleana que retorna true si un usuario es parte del comité del proyecto

        :param id_usuario: identificar unico del usuario del que se desea saber si es parte del comité
        :return: retorna True si forma parte y False en caso contrario
        """
        for usuario in self.comite.all():
            if usuario.id == id_usuario:
                return True
        return False

    def es_participante(self, id_usuario):
        """
        función booleana para saber si un usuario es participante del proyecto

        :param id_usuario: identificador único del usuario el cual se quiere saber si es participante del proyecto
        :return: True si es participante y False en caso contrario
        """
        for usuario in self.participantes.all():
            if usuario.id == id_usuario:
                return True
        return False


class TipoItem(models.Model):
    """
    Esta clase representa los tipos de items
    """
    #: Se almacena el nombre del tipo de item
    nombre = models.CharField(max_length=200)
    #: Descripcion del tipo de item
    descripcion = models.CharField(max_length=800)
    #: Prefijo para mostrarse en todos los items instanciados de esta plantilla
    prefijo = models.CharField(max_length=5)
    #: Proyecto asociado al Tipo de Item
    proyecto = models.ManyToManyField('Proyecto')
    #: campo que sirve para realizar auditoría de los objetos del modelo
    history = HistoricalRecords()

    def __str__(self):
        return self.nombre


class PlantillaAtributo(models.Model):
    """
    Esta clase representa las plantilla de atributos usada por el tipo de item

    """
    #: Se almacena el nombre del tipo de item
    nombre = models.CharField(max_length=200)
    #: Tipo del atributo a ser instanciado
    tipo = models.CharField(max_length=100)
    #: TipoItem asociado a la plantilla
    tipo_item = models.ForeignKey(TipoItem, on_delete=models.CASCADE)
    #: Atributo que indica si completar el atributo es requerido
    es_requerido = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Fase(models.Model):
    """
    Esta clase representa las fases
    """

    FASE_ESTADO_CERRADA = 'cerrada'
    FASE_ESTADO_ABIERTA = 'abierta'
    #: Se almacena el nombre de la fase
    nombre = models.CharField(max_length=200, null=False)
    #: Descripcion de la fase
    descripcion = models.CharField(max_length=400, null=True)
    #: Estado de la fase, iniciada, cerrada etc.
    estado = models.CharField(max_length=200, default=FASE_ESTADO_ABIERTA)
    #: Proyecto asociado a la fase
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    #: lista de tipos de ítem
    tipos_item = models.ManyToManyField('TipoItem', blank=True)
    #: campo que sirve para realizar auditoría de los objetos del modelo
    history = HistoricalRecords()

    class Meta:
        ordering = ['id']


class Rol(models.Model):
    """
    Clase que representa los roles de los usuarios en los proyectos
    """
    #: Nombre a ser asignado al Rol
    nombre = models.CharField(max_length=150, default='null')
    #: Proyecto asociado
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, null=True)
    #: Items del proyecto
    crear_item = models.BooleanField(default=False)
    #: Cambios realizados a los items del proyecto
    modificar_item = models.BooleanField(default=False)
    #: Dejar inactivo un item
    desactivar_item = models.BooleanField(default=False)
    #: Confirmar que el item es correcto
    aprobar_item = models.BooleanField(default=False)
    #: Cambiar version de un item
    reversionar_item = models.BooleanField(default=False)
    #: crear relaciones de tipo padre e hijo
    crear_relaciones_ph = models.BooleanField(default=False)
    #: crear relaciones de tipo antecesor y sucesor
    crear_relaciones_as = models.BooleanField(default=False)
    #: borrar relaciones del proyecto
    borrar_relaciones = models.BooleanField(default=False)
    #: ver Items del proyecto
    ver_item = models.BooleanField(default=False)
    #: crear lineas base en el proyecto
    crear_linea_base = models.BooleanField(default=False)
    #: cerrar fases del proyecto
    cerrar_fase = models.BooleanField(default=False)
    #: cerrar el proyecto
    cerrar_proyecto = models.BooleanField(default=False)
    #: ver proyecto
    ver_proyecto = models.BooleanField(default=False)
    #: solicitar ruptura de linea base
    solicitar_ruptura_lb = models.BooleanField(default=False)

    #: ver si el rol está activo
    activo = models.BooleanField(default=True)

    CREAR_ITEM = 'CREAR_ITEM'
    MODIFICAR_ITEM = 'MODIFICAR_ITEM'
    DESACTIVAR_ITEM = 'DESACTIVAR_ITEM'
    APROBAR_ITEM = 'APROBAR_ITEM'
    REVERSIONAR_ITEM = 'REVERSIONAR_ITEM'
    CREAR_RELACIONES_PH = 'CREAR_RELACIONES_PH'
    CREAR_RELACIONES_AS = 'CREAR_RELACIONES_AS'
    BORRAR_RELACIONES = 'BORRAR_RELACIONES'
    VER_ITEM = 'VER_ITEM'
    CREAR_LINEA_BASE = 'CREAR_LINEA_BASE'
    CERRAR_FASE = 'CERRAR_FASE'
    CERRAR_PROYECTO = 'CERRAR_PROYECTO'
    VER_PROYECTO = 'VER_PROYECTO'
    SOLICITAR_RUPTURA_LB = 'SOLICITAR_RUPTURA'

    def get_permisos_clean(self):
        """
        Metodo que colecta los permisos activos
        :return: una lista de permisos activos
        """
        permisos = []
        permisos = permisos + (['Crear Item'] if self.crear_item else [])
        permisos = permisos + (['Modificar Item'] if self.modificar_item else [])
        permisos = permisos + (['Desactivar Item'] if self.desactivar_item else [])
        permisos = permisos + (['Aprobar Item'] if self.aprobar_item else [])
        permisos = permisos + (['Reversionar Item'] if self.reversionar_item else [])
        permisos = permisos + (['Crear Relaciones Padre Hijo'] if self.crear_relaciones_ph else [])
        permisos = permisos + (['Crear Relaciones Antecesor Sucesor'] if self.crear_relaciones_as else [])
        permisos = permisos + (['Borrar Relaciones'] if self.borrar_relaciones else [])
        permisos = permisos + (['Ver Item'] if self.ver_item else [])
        permisos = permisos + (['Crear Linea Base'] if self.crear_linea_base else [])
        permisos = permisos + (['Cerrar Fase'] if self.cerrar_fase else [])
        permisos = permisos + (['Cerrar Proyecto'] if self.cerrar_proyecto else [])
        permisos = permisos + (['Ver Proyecto'] if self.ver_proyecto else [])
        permisos = permisos + (['Solicitar Ruptura Linea Base'] if self.solicitar_ruptura_lb else [])

        return permisos

    def __str__(self):
        return self.nombre


class UsuarioxRol(models.Model):
    """
    Clase en la cual se definen los roles del usuario
    """
    #: Usuario al cual le corresponde dicho rol
    usuario = models.ForeignKey('login.Usuario', on_delete=models.CASCADE)
    #: Rol del usuario
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    #: Fase del proyecto al cual esta asociado el usuario
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    #:
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.usuario.username} es {self.rol.nombre} en {self.fase.nombre} - {self.activo}'
