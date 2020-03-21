"""
Este modulo se encarga de registrar los usuarios en firebase y la base de datos del sistema
"""
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