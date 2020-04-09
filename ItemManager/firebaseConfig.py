import pyrebase
config = {
    'apiKey': "AIzaSyCqhDwOP5cTSm58BV7gnkFnF4qz-26OWI8",
    'authDomain': "itemmanager-77211.firebaseapp.com",
    'databaseURL': "https://itemmanager-77211.firebaseio.com",
    'projectId': "itemmanager-77211",
    'storageBucket': "itemmanager-77211.appspot.com",
    'messagingSenderId': "972002011767",
    'appId': "1:972002011767:web:fe16134c99f6a8d6a3f472",
    'measurementId': "G-R78XM8ZQD3"
  }
firebase = pyrebase.initialize_app(config)