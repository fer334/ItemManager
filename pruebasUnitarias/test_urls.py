"""
Modulo para hacer test sobre el modulo urls.py
"""
from django.urls import reverse, resolve
from django.test import TestCase


class TestUrls(TestCase):
    """
    Clase para realizar pruebas sobre los urls del proyecto ItemManager
    """

    def test_index_url(self):
        """
        CU 01:acceder al sistema. Iteración 1
        con las funciones reverse y resolve comprobamos que el path a index sea el correcto

        :return: el assert retornara True si el path está bien
        """
        path = reverse('login:index')
        self.assertEqual(resolve(path).view_name, 'login:index', "La prueba falló porque el nombre del template es "
                                                                 "incorrecto")

    def test_index_url_ejemplo_prueba_fallida(self):
        """
        CU 01: acceder al sistema. Iteración 1
        Prueba que falla de ejemplo para mostrar como hacer mensajes que expliquen el error

        :return: el assert retornara True si el path está bien
        """
        path = reverse('login:index')
        self.assertEqual(resolve(path).view_name, 'login:indexx', "La prueba falló porque el nombre del template es "
                                                                  "incorrecto")
