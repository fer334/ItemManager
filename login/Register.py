"""
Este modulo se encarga de registrar los usuarios en firebase y la base de datos del sistema
"""
import pyrebase
from .models import Usuario
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


def crear_usuario(var_email, password):
    """
    Metodo que se encarga de la creacion del usuario tanto en firebase

    :param username: El nombre de usuario a ser creado
    :param var_email: El email del usuario a ser creado
    :param password: El password del usuario a ser creado
    :returns true: si el usuario se creo correctamente, false si no
    """
    user = authfb.create_user_with_email_and_password(var_email, password)
    return user