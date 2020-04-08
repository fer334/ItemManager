"""
Este modulo se encarga de registrar los usuarios en firebase y la base de datos del sistema
"""
from ItemManager.firebaseConfig import firebase
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
