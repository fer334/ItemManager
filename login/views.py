"""
En este modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import auth
from .Register import crearUsuario
from django.views.generic import TemplateView

@login_required
def index(request):
    """
    Funcion que solo muestra el index, validando antes si el usuario inicio sesion

    """
    return render(request, 'login/index.html', {})


class LoginPage(TemplateView):
    """
    Clase que solo muestra el template del login

    """
    template_name = 'login/login.html'


class Register(TemplateView):
    """
    Clase que solo muestra el template de creacion de usuario

    """
    template_name = 'login/register.html'


def postRegister(request):
    """
    Funcion que se encarga de registrar al usuario, espera un POST Request

    :param POST[email]: Email del usuario nuevo
    :param POST[password]: Contraseña del usuario nuevo
    :param POST[username]: Nombre del usuario nuevo
    """
    var_email = request.POST['email']
    password = request.POST['password']
    username = request.POST['username']
    if crearUsuario(username, var_email, password):
        return render(request, 'login/postReg.html', {})
    else:
        return render(request, 'login/register.html', {'error_message': 'Error, vuelva a intenter'})


def makeLogin(request):
    """
    Funcion que se encarga de loguear al usuario

    :param POST[email]: Email del usuario
    :param POST[password]: Contraseña del usuario

    """
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, email=email, password=password)
    if user is None:
        message = 'Credenciales invalidas'
        return render(request, 'login/login.html', {'error_message': message})
    login(request, user)
    return render(request, 'login/index.html', {})


def logout(request):
    """
    Funcion que se encarga de cerrar la sesion del usuario

    """
    auth.logout(request)
    return render(request, 'login/login.html', {})
