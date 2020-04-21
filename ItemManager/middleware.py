"""ItemManager middleware catalog."""

# Django
import re

from django.shortcuts import redirect
from django.urls import reverse

from administracion.models import Proyecto
from desarrollo.models import Item
from login.models import Usuario


class ActiveAccountMiddleware:
    """
    Account access middleware.

    Mediador para solicitudes que involucren a las cuentas activas.
    """

    def __init__(self, get_response):
        """Inicializador del Middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Código que se ejecutará para cada request antes de que se llame a la vista.
        """
        if request.path == '/':
            # Al inicio cualquiera puede entrar pues se verifica antes si esta
            # logueado o si es un usuario sin cuenta activa
            pass

        elif not request.user.is_anonymous:
            # esta logueado
            puede_entrar = "/accesoDenegado|/logout"

            # Cualquier usuario puede entrar modificar su username
            if request.path == reverse('login:userUpdate', args=[request.user]):
                pass

            elif request.user.is_superuser:
                # Es admin
                puede_entrar += "|/admin|/(.*)/update"

                if not bool(re.match(puede_entrar, request.path)):
                    # El path es distinto a puede_entrar
                    return redirect(
                        'login:AccesoDenegado',
                        # {"message": "El administrador no pueder ver los proyectos"}
                    )
            elif not request.user.is_active:
                # No tiene cuenta activa y no es admin
                if not bool(re.match(puede_entrar, request.path)):
                    # El path es distinto a puede_entrar
                    return redirect(
                        'login:AccesoDenegado',
                        # {"message": "No tienes el rol de gerente, no puedes ver los proyectos"}
                    )
            elif not request.user.is_gerente:
                # Si no es gerente y tiene cuenta activa
                puede_entrar += "|/desarrollo"
                if not bool(re.match(puede_entrar, request.path)):
                    # El path es distinto a puede_entrar
                    return redirect(
                        'login:AccesoDenegado',
                        # {"message": "No tienes el rol de gerente, no puedes ver los proyectos"}
                    )
            elif request.user.is_gerente:
                puede_entrar += "|/administracion|/desarrollo"
                if not bool(re.match(puede_entrar, request.path)):
                    # El path es distinto a puede_entrar
                    return redirect(
                        'login:AccesoDenegado',
                        # {"message": "No tienes el rol de gerente, no puedes ver los proyectos"}
                    )
        else:
            # No esta logueado

            # Puede entrar a:
            puede_entrar = "/login|/register|/accesoDenegado"

            if not bool(re.match(puede_entrar, request.path)):
                # Si no es alguno de esos
                return redirect(
                    'login:AccesoDenegado',
                    # {"message": "No haz iniciado sesion en el sistema"}
                )

        response = self.get_response(request)
        return response


class EstadoProyectoMiddleware:
    """
    Middleware Estados Proyectos

    Clase encargada de ser mediador para las solicitudes de request, y a la vez
    hace validaciones sobre los estados de los proyectos
    """

    def __init__(self, get_response):
        """Inicializador del Middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Código que se ejecutará para cada request antes de que se llame a la vista.
        """

        path = request.path
        # para URLs con el id del proyecto en ellos
        if bool(re.match("(.*)/proyectos/[0-9]+/", path)):

            # url ejemplo /desarrollo/proyectos/12/tipo
            id_proyecto = path.split("/")[3]
            obj_proyecto = Proyecto.objects.get(pk=id_proyecto)

            # (borrar si no es necesario) user_proyect = Usuario.objects.get(id=obj_proyecto.gerente)

            # Permitir entrar a accesodenegado y a proyectos/1/
            if not bool(re.match("(.*)/accesodenegado/", path))\
                    and not bool(re.match("^(.*)/proyectos/[0-9]+/$", path)):

                # No permitir si el usuario actual es distinto al gerente del proyecto
                """ probar si lo comentado no es necesario                
                if request.user.id != user_proyect.id:
                    return redirect(
                        'administracion:accesoDenegado',
                        id_proyecto=id_proyecto, caso="gerente"
                    )
                """
                # if para estado del proyecto cancelado
                if obj_proyecto.estado == Proyecto.ESTADO_CANCELADO:
                    return redirect(
                        'administracion:accesoDenegado',
                        id_proyecto=id_proyecto, caso='estado'
                    )
                # if para estado finalizado
                elif obj_proyecto.estado == Proyecto.ESTADO_FINALIZADO:
                    # para el view administrar participantes y ver roles si el proyecto está en finalizado no se debe
                    # redireccionar a acceso denegado
                    if not (bool(re.match("^(.*)/proyectos/[0-9]+/participantes(.*)", path))
                            or bool(re.match("^(.*)/proyectos/[0-9]+/roles(.*)", path))
                            or bool(re.match("^(.*)/proyectos/[0-9]+/items/[0-9]+", path))):
                        return redirect(
                            'administracion:accesoDenegado',
                            id_proyecto=id_proyecto, caso='estado')
                # if para estado en ejecucion
                elif obj_proyecto.estado == Proyecto.ESTADO_EN_EJECUCION:
                    # vistas a las que no se puede acceder en este estado
                    if request.path in [
                        reverse('administracion:importarTipoItem', args=[id_proyecto]),
                        reverse('administracion:crearTipoItem', args=[id_proyecto]),
                        reverse('administracion:registrarEnBase', args=[id_proyecto])] \
                            or bool(re.match("^(.*)/proyectos/[0-9]+/(.*)mostrarImport(.*)", path)):
                        return redirect('administracion:accesoDenegado',
                                        id_proyecto=id_proyecto, caso='estado')
                # if para estado iniciado
                elif obj_proyecto.estado == Proyecto.ESTADO_INICIADO:
                    # si se encuentra en módulo de desarrollo bloquear acceso
                    if bool(re.match("^(.*)/desarrollo/(.*)", path)):
                        return redirect('administracion:accesoDenegado',
                                        id_proyecto=id_proyecto, caso='estado')
        # para URLs con el id del ítem en ellos
        elif bool(re.match("(.*)/items/[0-9]+/", path)):
            id_item = path.split("/")[3]
            item = Item.objects.get(pk=id_item)
            fase = item.fase
            proyecto = fase.proyecto
            if proyecto.estado != Proyecto.ESTADO_EN_EJECUCION:
                return redirect('administracion:accesoDenegado',
                                id_proyecto=proyecto.id, caso='estado')

        response = self.get_response(request)
        return response
