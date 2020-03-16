
import pyrebase
from .models import usr
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
firebase = pyrebase.initialize_app(config)
authfb = firebase.auth()


def crear_usuario(username, var_email, password):
    """
    Metodo que se encarga de la creacion del usuario tanto en firebase como en la base local

    :param username: El nombre de usuario a ser creado
    :param var_email: El email del usuario a ser creado
    :param password: El password del usuario a ser creado
    :returns  true si el usuario se creo correctamente, false si no
    """
    try:
        user = authfb.create_user_with_email_and_password(var_email, password)
        nuevo_usuario = usr(username=username, email=var_email, is_active=1, localId=user['localId'])
        nuevo_usuario.save()
        return True
    except:
        return False
