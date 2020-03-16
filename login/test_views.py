"""
Modulo para hacer test sobre el modulo views.py
"""
from django.test import RequestFactory
from django.urls import reverse
from login.views import index, loginPage
from django.contrib.auth.models import AnonymousUser
from .models import usr
import pytest


class TestViews:
    """
    Clase para realizar pruebas sobre las vistas de la aplicacion login del proyecto
    """

    def test_index_usuario_no_autenticado(self):
        """
        La vista index tiene la marca de @login_required por lo que si el usuario no se ha logeado
        se redireccionara a login con el codigo 302 de redireccionamiento

        :return: el assert retornara true si se hace un redireccionamiento y false en otros casos
        """
        path = reverse('login:index')
        request = RequestFactory().get(path)
        # la funcion anonymousUser simula un usuario sin logearse
        request.user = AnonymousUser()

        response = index(request)

        assert response.status_code == 302

    @pytest.mark.django_db
    def test_index_usuario_autenticado(self):
        """
        Prueba parecida a la anterior pero con la diferencia de que se utiliza un usuario autenticado.

        :return: el assert retornara true si se hace un redireccionamiento y false en otros casos
        """
        path = reverse('login:index')
        request = RequestFactory().get(path)
        self.usuario = usr.objects.create_user(
            username='testusuario', email='estoes@unaprueba.com', password='password')
        request.user = self.usuario

        response = index(request)

        assert response.status_code == 200

    def test_login_page(self):
        """
        Esta vista no requiere previo logeo del usuario por lo que si se solicita el template relacionado
        a ella se retornara sin problemas y con un codigo 200 de exito

        :return: el assert retornara true si el codigo de respuesta es 200 (exito)
        """
        path = reverse('login:login')
        request = RequestFactory().get(path)
        request.user = AnonymousUser()

        response = loginPage(request)

        assert response.status_code == 200
