"""ItemManager middleware catalog."""

# Django
from django.shortcuts import redirect
from django.urls import reverse


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

        if not request.user.is_anonymous:
            if True not in [request.user.is_active, request.user.is_superuser]:
                if request.path not in [
                    reverse('login:index'),
                    reverse('login:AccesoDenegado'),
                    reverse('login:logout')
                ]:
                    return redirect('login:AccesoDenegado')
        response = self.get_response(request)
        return response


class GerenteAccountMiddleware:
    """
    Account access middleware.

    Mediador para solicitudes que involucren a las cuentas gerentes.
    """

    def __init__(self, get_response):
        """Inicializador del Middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Código que se ejecutará para cada request antes de que se llame a la vista.
        """

        if not request.user.is_anonymous:
            if not request.user.is_gerente and not request.user.is_superuser:
                username = request.user.username
                if request.path not in [
                    reverse('login:index'),
                    reverse('login:AccesoDenegado'),
                    reverse('login:logout'),
                    reverse('login:userUpdate', args=[username]),
                    # reverse('login:userUpdate', kwargs={'name': username}),
                ]:
                    return redirect('login:AccesoDenegado')
        response = self.get_response(request)
        return response
