
from ItemManager.settings import BASE_DIR
from datetime import datetime
from ItemManager.firebaseConfig import firebase
from login.models import Usuario
import os

TEMP_FILES_DIR = BASE_DIR+'/desarrollo/temp';


def generar_nombre(nombre):
    now = datetime.now()
    nombre = f'{now.strftime("%Y_%m_%d_%H_%M_%S")}_{nombre}'
    return nombre


def handle_uploaded_file(archivo, id_proyecto, user):

    final_storage_path = f'{id_proyecto}/{generar_nombre(archivo)}'
    final_path = f'{TEMP_FILES_DIR}/{generar_nombre(archivo)}'
    user_obj = Usuario.objects.get(username=user)
    with open(final_path, 'wb+') as destination:
        try:
            for chunk in archivo.chunks(): 
                destination.write(chunk)
            storage = firebase.storage()
            storage.child(final_storage_path).put(final_path)
            os.remove(final_path)
            url = storage.child(final_storage_path).get_url(user_obj.id_token)
            return url
        except:
            return None
    return None
