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