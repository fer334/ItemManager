"""
En este modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
# Django
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import TemplateView
from django.http import HttpResponse

# RegisterBackend
from login.Register import crear_usuario

# Forms
from login.forms import RegisterForm, UpdateUserForm, AdminUpdUserForm

# Models
from login.models import Usuario


@login_required
def index(request):
    """
    Funcion que solo muestra el index, validando antes si el usuario inicio sesion

    """
    if request.user.is_superuser:
        return render(request, 'login/admin.html')
    elif request.user.is_active:
        return render(request, 'login/index.html')
    else:
        return render(request, 'login/no_active.html')


def user_login(request):
    """
    Vista que se encarga de loguear al usuario

    :param POST[email]: Email del usuario
    :param POST[password]: Contraseña del usuario
    """

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is None:
            message = 'Credenciales invalidas'
            return render(request, 'login/login.html', {'error_message': message})
        login(request, user)

        return redirect('login:index')

    return render(request, 'login/login.html')


def logout(request):
    """
    Funcion que se encarga de cerrar la sesion del usuario

    """
    auth.logout(request)
    return redirect('login:login')


def admin(request):
    """
    Vista que solo sera visible para el administrador
    """
    return render(request, 'login/admin.html')


def users_access(request):
    usuarios = Usuario.objects.order_by('id'). \
        exclude(is_superuser=True)

    if request.method == 'POST':
        usuarios = request.POST
        print(usuarios)
        Usuario.objects.update(is_active=False)
        Usuario.objects.update(is_gerente=False)
        for id_usuario, valor in usuarios.items():
            if id_usuario != 'csrfmiddlewaretoken':
                if id_usuario.isnumeric() or \
                        id_usuario.split('g')[1].isnumeric():

                    # si encuentra una g antes es el campo gerente
                    if id_usuario.find('g') == 0:
                        Usuario.objects.filter(
                            id=id_usuario.split('g')[1]
                        ).update(is_gerente=valor)

                    # sino es el campo is_active
                    else:
                        Usuario.objects.filter(
                            id=id_usuario
                        ).update(is_active=valor)
        return redirect('login:index')

    return render(
        request,
        'login/access.html',
        {'usuarios': usuarios, }
    )


def user_register(request):
    """
    Vista que se encarga de registrar al usuario, espera un POST Request

    :param request:
    :param POST[email]: Email del usuario nuevo
    :param POST[password]: Contraseña del usuario nuevo
    :param POST[username]: Nombre del usuario nuevo
    """

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login:login')
    else:
        form = RegisterForm()
    return render(request, 'login/register.html', {'form': form})


def user_update(request, name):
    """
    Vista encargada de la modificacion de datos
    de los usuarios
    """

    instance = Usuario.objects.get(username=name)
    if request.method == 'POST':
        form = UpdateUserForm(
            request.POST,
            instance=instance,
        )
        if form.is_valid():
            form.update(key=name)
            return redirect('login:index')

    else:
        print('instance')
        print(instance.id)
        form = UpdateUserForm(
            instance=instance,
            initial={'username': name}
        )

    return render(
        request=request,
        template_name='login/user_update.html',
        context={
            'form': form,
        }
    )
