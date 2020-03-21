"""
Modulo para hacer test sobre el modulo urls.py
"""
from django.urls import reverse, resolve


class TestUrls:
    """
    Clase para realizar pruebas sobre los urls de la aplicacion login
    """

    def test_index_url(self):
        """
        con las funciones reverse y resolve comprobamos que el path a index sea el correcto

        :return: el assert retornara True si el path está bien
        """
        path = reverse('login:index')
        assert resolve(path).view_name == 'login:index'

    def test_index_url_ejemplo_prueba_fallida(self):
        """
        Prueba que falla de ejemplo para mostrar como hacer mensajes que expliquen el error

        :return: el assert retornara True si el path está bien
        """
        path = reverse('login:index')
        assert resolve(path).view_name == 'login:indexx', "La prueba falló porque el nombre del template es incorrecto"
