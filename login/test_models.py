from login.models import Usuario


class TestModels:
    """
    clase para realizar pruebas sobre los modelos de la aplicación login
    """
    def test_usuario(self):
        """
        prueba de inicializacion de la clase usuario
        """
        usuario = Usuario("user1","Ulises Suario","user1@hotmail.com","12345abdce","")
        assert usuario.nombre_usuario == "user1"
        assert usuario.nombre_y_apellido == "Ulises Suario"
        assert usuario.email == "user1@hotmail.com"
        assert usuario.contrasegna == "12345abdce"
