from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
import pyrebase
from django.contrib import auth
from .models import Usuario
from django.views.generic.base import TemplateView
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
