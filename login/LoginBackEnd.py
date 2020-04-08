"""
Clase creada para gestionar el Login del usuario
"""
from urllib.error import HTTPError

from django.contrib.auth.backends import BaseBackend
from .models import Usuario
from ItemManager.firebaseConfig import firebase

authfb = firebase.auth()


class LoginBackEnd(BaseBackend):
    """
    Clase que hereda de BaseBackend para implementar la autenticacion del usuario, esta clase realiza la coneccion con
    firebase y autentica al usuario en la base de datos de la app

    """
    def authenticate(self, request, email=None, password=None):
        """
        Metodo que se encarga de la autenticacion del usuario tanto en firebase como en la base local

        :param request: Request HTTP
        :param email: email del usuario a loguear
        :param password: password del usuario a loguear

        :returns Se retorna el objeto correspondiente al usuario de la base de datos local
        """
        try:
            userfb = authfb.sign_in_with_email_and_password(email, password)
            try:
                user = Usuario.objects.get(localId=userfb['localId'])
            except Usuario.DoesNotExist:
                return None
            return user
        except:
            """requests.exceptions.HTTPError as err:
            print( repr(err) )
            """
            return None


    def get_user(self, user_id):
        """
        Metodo que busca un usuario en la base local

        :param user_id: El id del usuario a buscar(De la BD local)

        :returns Se retorna el objeto correspondiente al usuario de la base de datos local
        """
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
