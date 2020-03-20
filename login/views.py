"""
En este modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import TemplateView

from login.Register import crear_usuario

#Forms
from login.forms import RegisterForm


@login_required
def index(request):
    """
    Funcion que solo muestra el index, validando antes si el usuario inicio sesion

    """
    return render(request, 'login/index.html', {})


def user_login(request):
    """
    Vista que se encarga de loguear al usuario

    :param POST[email]: Email del usuario
    :param POST[password]: Contraseña del usuario
    """
 
    if request.method=='POST':
#        form = UsuarioForm(request.POST)
 #       if form.is_valid():

            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is None:
                message = 'Credenciales invalidas'
                return render(request, 'login/login.html', {'error_message': message})
            login(request, user)
            return redirect('login:index')

    else:
  #      form = ProyectoForm()
        pass

    return render(request, 'login/login.html')


def user_register(request):
    """
    Vista que se encarga de registrar al usuario, espera un POST Request

    :param POST[email]: Email del usuario nuevo
    :param POST[password]: Contraseña del usuario nuevo
    :param POST[username]: Nombre del usuario nuevo
    """

    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login:login')

    else:
        form = RegisterForm()
        #print(form)
    return render(request,'login/register.html',{'form':form})

def logout(request):
    """
    Funcion que se encarga de cerrar la sesion del usuario

    """
    auth.logout(request)
    return redirect('login:login')