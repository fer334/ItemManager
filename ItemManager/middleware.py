"""ItemManager middleware catalog."""

# Django
import re

from django.shortcuts import redirect
from django.urls import reverse

from administracion.models import Proyecto


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


class ProyectoMiddleware:
    """
    Middleware Proyectos

    Clase encargada de ser mediador para las solicitudes de request, y a la vez
    hace validaciones sobre los proyectos
    """

    def __init__(self, get_response):
        """Inicializador del Middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Código que se ejecutará para cada request antes de que se llame a la vista.
        """

        path = request.path

        if bool(re.match("(.*)/proyectos/[0-9]+/", path)):

            # url ejemplo /desarrollo/proyectos/12/tipo
            id_proyecto = path.split("/")[3]

            # No permitir entrar a urls estado denegado ni a url la vista ver
            # proyecto
            if not bool(re.match("(.*)/accesodenegado/estado", path)) \
                    and not bool(re.match("^(.*)/proyectos/[0-9]+/$", path)):

                # url ejemplo /administracion/
                obj_proyecto = Proyecto.objects.get(pk=id_proyecto)
                if obj_proyecto.estado == Proyecto.ESTADO_CANCELADO\
                        or obj_proyecto.estado == Proyecto.ESTADO_FINALIZADO:

                    return redirect(
                        'administracion:accesoDenegado',
                        id_proyecto=id_proyecto, caso='estado'
                    )

        response = self.get_response(request)
        return response
