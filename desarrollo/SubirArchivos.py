
from ItemManager.settings import BASE_DIR
from datetime import datetime
from ItemManager.firebaseConfig import firebase
import os

TEMP_FILES_DIR = BASE_DIR+'/desarrollo/temp';


def generar_nombre(nombre):
    now = datetime.now()
    nombre = f'{now.strftime("%Y_%m_%d_%H_%M_%S")}_{nombre}'
    return nombre


def handle_uploaded_file(f, id_proyecto):
    final_storage_path = f'{id_proyecto}/{generar_nombre(f)}'
    final_path = f'{TEMP_FILES_DIR}/{generar_nombre(f)}'
    with open(final_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        storage = firebase.storage()
        storage.child(final_storage_path).put(final_path)
        os.remove(final_path)
        #url = storage.child('sc.png').get_url(None)
        #print(url)
    return
