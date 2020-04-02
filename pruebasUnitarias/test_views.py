"""
Modulo para hacer test sobre el modulo views.py
"""
from django.test import RequestFactory
from django.urls import reverse
from login.views import index
from django.contrib.auth.models import AnonymousUser
from login.models import Usuario
import pytest


class TestViews:
    """
    Clase para realizar pruebas sobre las vistas de la aplicacion login del proyecto
    """

    def test_index_usuario_no_autenticado(self):
        """
        CU 01: acceder al sistema. Iteración 1
        La vista index tiene la marca de @login_required por lo que si el usuario no se ha logeado
        se redireccionara a login con el codigo 302 de redireccionamiento

        :return: el assert retornara true si se hace un redireccionamiento y false en otros casos
        """
        path = reverse('login:index')
        request = RequestFactory().get(path)
        # la funcion anonymousUser simula un usuario sin logearse
        request.user = AnonymousUser()

        response = index(request)

        assert response.status_code == 302, 'Prueba falló porque no hubo redirección'

    @pytest.mark.django_db
    def test_index_usuario_autenticado(self):
        """
        CU 01: acceder al sistema y CU 02: registrar usuario. Iteración 1
        Prueba parecida a la anterior pero con la diferencia de que se utiliza un usuario autenticado.

        :return: el assert retornara true si se hace un redireccionamiento y false en otros casos
        """
        path = reverse('login:index')
        request = RequestFactory().get(path)
        self.usuario = Usuario.objects.create_user(
            username='testusuario', email='estoes@unaprueba.com', password='password')
        request.user = self.usuario

        response = index(request)

        assert response.status_code == 200, 'La prueba falló porque el usuario no fue registrado'

