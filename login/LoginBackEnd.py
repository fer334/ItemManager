"""
Clase creada para gestionar el Login del usuario
"""
from urllib.error import HTTPError

from django.contrib.auth.backends import BaseBackend
import pyrebase
from .models import Usuario

config = {
    'apiKey': "AIzaSyCqhDwOP5cTSm58BV7gnkFnF4qz-26OWI8",
    'authDomain': "itemmanager-77211.firebaseapp.com",
    'databaseURL': "https://itemmanager-77211.firebaseio.com",
    'projectId': "itemmanager-77211",
    'storageBucket': "itemmanager-77211.appspot.com",
    'messagingSenderId': "972002011767",
    'appId': "1:972002011767:web:fe16134c99f6a8d6a3f472",
    'measurementId': "G-R78XM8ZQD3"
  };
firebase = pyrebase.initialize_app( config )
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
                user = Usuario.objects.get( localId=userfb['localId'] )
            except Usuario.DoesNotExist:
                usuario = Usuario( email = email, localId= userfb['localId'] )
                usuario.save()
                user = usuario
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
