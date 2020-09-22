"""
Modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
# Django
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth

# Forms
from login.forms import RegisterForm, UpdateUserForm

# Models
from login.models import Usuario


@login_required
def index(request):
    """
    Método que muestra el index, validando antes si el usuario inició sesión

    :param request: objeto tipo diccionario que permite acceder a datos
    :return: objeto que se encarga de renderar admin.html, index.html o no_active.html
    :rtype: render
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

    :param request: objeto tipo diccionario que permite acceder a datos
    :return: objeto que se encarga de renderar login.html
    :return: redirección a la vista index
    :rtype: render, redirect
    """

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is None:
            message = 'Credenciales invalidas'
            return render(request, 'login/login.html', {'error_message': message})
        login(request, user)
        #request.session.set_expiry(3600)
        #SE SACA EL SESSION TIMEOUT DE CADA USUSARIO
        return redirect('login:index')

    return render(request, 'login/login.html')


def logout(request):
    """
    Función que se encarga de cerrar la sesión del usuario

    :param request: objeto tipo diccionario que permite acceder a datos
    :return: redireccion a la vista login
    :rtype: redirect
    """
    auth.logout(request)
    return redirect('login:login')


def admin(request):
    """
    Vista que solo sera visible para el administrador

    :param request: objeto tipo diccionario que permite acceder a datos
    :return: objeto que se encarga de renderar admin.html
    :rtype: render
    """
    return render(request, 'login/admin.html')


def users_access(request):
    """
    Vista para modificar el acceso de los usuarios al sistema, ademas hacer a un
    usuario gerente

    :param request: objeto tipo diccionario que permite acceder a datos
    :return: objeto que se encarga de renderar access.html
    :rtype: render
    """
    usuarios = Usuario.objects.order_by('id'). \
        exclude(is_superuser=True)

    if request.method == 'POST':
        usuarios = request.POST
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
    Vista que se encarga de registrar a un usuario

    :param request: objeto tipo diccionario que permite acceder a datos
    :return: objeto que se encarga de renderar register.html
    :rtype: render
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
    Vista encargada de la modificacion de datos de los usuarios

    :param request: objeto tipo diccionario que permite acceder a datos
    :param name: nombre del usuario a modificar
    :return: objeto que se encarga de renderar user_update.html
    :rtype: render
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
