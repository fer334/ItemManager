"""
Vistas que seran utilizadas por la app
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth
from .Register import crearUsuario
import os


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
    if crearUsuario(username, var_email, password):
        return render(request, 'login/postReg.html', {})
    else:
        return render(request, 'login/register.html', {'error_message': 'Error, vuelva a intenter'})


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
