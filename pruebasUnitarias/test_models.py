"""
Modulo para hacer test sobre el modulo models.py
"""
from login.models import Usuario
import pytest


@pytest.mark.django_db
class TestModels:
    """
    Esta clase se utiliza para probar las clases que implementan o utilizan modelos django en el proyecto ItemManager
    """

    def test_usr(self):
        """
        CU 05: crear usuarios. Iteración 1
        Se probará la creación de un usuario con la implementacion Usuario

        :return: los asserts devuelven true si el usuario fue correctamente creado
        """
        usuario = Usuario.objects.create_user(username="prueba", email="prueba@mail.com", password="contraseña")

        assert usuario.username == 'prueba'
        assert usuario.email == 'prueba@mail.com'
        # obs: la contraseña estará encriptada por lo que no será igual a la guardada
        assert usuario.password != 'contraseña', "falla porque esta encriptado"
