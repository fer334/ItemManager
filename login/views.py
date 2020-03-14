from urllib.error import HTTPError

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
import pyrebase
from django.contrib import auth
from .models import usr
import os

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

@login_required
def index( request ):
    return render(request, 'login/index.html', {})

def loginPage( request ):
    return render( request, 'login/login.html', { })

def register( request ):
    return render( request, 'login/register.html', { })

def postRegister(request):
    var_email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    user = authfb.create_user_with_email_and_password( var_email, password )
    nuevo_usuario = usr( username = username, email= var_email, is_active= 1, localId = user['localId'] )
    nuevo_usuario.save()
    return render( request, 'login/postReg.html', {})

def makeLogin( request ):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate( request, email=email, password=password)
    if user is None:
        message = 'Credenciales invalidas'
        return render(request, 'login/login.html', {'error_message': message})
    login( request, user )
    return render( request, 'login/index.html', {})

def logout( request ):
    auth.logout( request )
    return render( request, 'login/login.html',{})

"""
def makeLogin( request ):
    email = request.POST['email']
    password = request.POST['password']
    try:
        userfb = authfb.sign_in_with_email_and_password(email, password)
    except HTTPError as err:
        pass

    user = authenticate( request, email=email, password=password)
    if user is None:
        message = 'Credenciales invalidas'
        return render(request, 'login/login.html', {'error_message': message})
    login( request, user )
    context = {
        'userFirebaseData': userfb
    }
    return render( request, 'login/index.html', context)
"""
