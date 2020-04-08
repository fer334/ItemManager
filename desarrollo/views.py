from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .SubirArchivos import handle_uploaded_file
from administracion.models import Proyecto
from django.urls import reverse
from .forms import ItemForm, GeeksForm
from login.LoginBackEnd import firebase


def index(request, filtro):
    """
    Vista que despliega la lista de proyectos con su estado actual, también permite filtrar los proyectos según estado,
    además solo muestra los proyectos de los cuales es gerente el usuario que hizo el request

    :param request: objeto tipo diccionario que permite acceder a datos
    :param filtro: este parámetro indica el estado según se filtrarán los proyectos. Si el valor es 'todos' no se aplicará ningún filtro
    :return: objeto que se encarga de renderear proyecto_ver_todos.html
    :rtype: render
    """
    # lista final de proyectos con filtros de estado aplicados
    lista_proyectos = []
    # lista con los proyectos en los que es gerente el usuario
    lista_proyectos_usuario = []
    # lista sin ningún filtro de todos los proyectos del sistema
    lista_todos_proyectos = Proyecto.objects.all()

    """
    # mostrar solo en los que el usuario participa
    for proye in lista_todos_proyectos:
        if proye.es_participante(request.user.id):
            lista_proyectos_usuario.append(proye)
    """
    for proye in lista_todos_proyectos:
        if proye.gerente == request.user.id:
            lista_proyectos_usuario.append(proye)

    # filtrar según estado
    if filtro == 'todos':
        lista_proyectos = lista_proyectos_usuario
    else:
        for proyecto in lista_proyectos_usuario:
            if proyecto.estado == filtro:
                lista_proyectos.append(proyecto)

    return render(request, 'desarrollo/proyecto_ver_todos.html', {'lista_proyectos': lista_proyectos, 'filtro': filtro})


def ver_proyecto(request, id_proyecto):
    """
    Esta vista despliega un proyecto con todos los valores que toman sus atributos, además de sus fases, roles
    y tipos de ítems

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: Se recibe como parámetro el id_del proyecto que se desea ver
    :return: objeto que renderea verProyecto.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render(request, 'desarrollo/proyecto_ver_unico.html', {'proyecto': proyecto})


def adjuntar_archivo(request, id_proyecto, id_item):
    context = {}
    if request.POST:
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            url = handle_uploaded_file(request.FILES['archivo_adjunto'], id_proyecto, request.user)
    else:
        form = ItemForm()
    context['form'] = form
    return render(request, "desarrollo/adjuntar_archivo.html", context)


