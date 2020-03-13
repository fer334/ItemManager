from django.contrib.auth.decorators import login_required
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

authfb = firebase.auth()
@login_required
def index( request ):
    return render(request, 'login/testLogin.html', {})

def login( request ):
    return render( request, 'login/login.html', { })

def register( request ):
    return render( request, 'login/register.html', { })

def postRegister(request):
    var_email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    try:
        user = authfb.create_user_with_email_and_password( var_email, password )
        nuevo_usuario = Usuario( nombre_usuario = username, email = var_email )
        nuevo_usuario.save()
    except:
        return render(request, 'login/register.html', {'error_message' : 'Error al registrar, pruebe con otro email y contraseña de 6 caracteres'})
    return render( request, 'login/postReg.html', {})

def makeLogin( request ):
    email = request.POST['email']
    password = request.POST['password']
    try:
        user = authfb.sign_in_with_email_and_password(email, password)
    except:
        message = 'Credenciales invalidas'
        return render( request, 'login/login.html',{ 'error_message' : message } )
    context = {
        'userFirebaseData': user
    }
    session_id = user['idToken']
    request.session['uid'] = str( session_id )
    return render( request, 'login/testLogin.html', context)

def logout( request ):
    auth.logout( request )
    return render( request, 'login/login.html',{})
