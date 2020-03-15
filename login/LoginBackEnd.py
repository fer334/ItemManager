"""
Clase creada para gestionar el Login del usuario
"""

from django.contrib.auth.backends import BaseBackend
import pyrebase
from  .models import usr

config = {
    'apiKey': "AIzaSyAbCiMgh8az4COYBvq038jbrvVGA16oCeo",
    'authDomain': "poliproyecto-6dfb4.firebaseapp.com",
    'databaseURL': "https://poliproyecto-6dfb4.firebaseio.com",
    'projectId': "poliproyecto-6dfb4",
    'storageBucket': "poliproyecto-6dfb4.appspot.com",
    'messagingSenderId': "562557261320",
    'appId': "1:562557261320:web:64f3792e7ca3608c1463bd",
    'measurementId': "G-GED6N0CHKC"
}
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

        :return Se retorna el objeto correspondiente al usuario de la base de datos local
        """
        try:
            userfb = authfb.sign_in_with_email_and_password(email, password)
            try:
                user = usr.objects.get( localId=userfb['localId'] )
            except usr.DoesNotExist:
                usuario = usr( email = email, localId= userfb['localId'] )
                usuario.save()
                user = usuario
            return user
        except:
            return None

    def get_user(self, user_id):
        """
        Metodo que busca un usuario en la base local

        :param user_id: El id del usuario a buscar(De la BD local)

        :return Se retorna el objeto correspondiente al usuario de la base de datos local
        """
        try:
            return usr.objects.get(pk=user_id)
        except usr.DoesNotExist:
            return None
