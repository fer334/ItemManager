from django.shortcuts import render

# Create your views here.
from administracion.models import Proyecto
from desarrollo.models import Item


def index(request, filtro):
    """
    añadir doc

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

    # mostrar solo en los que el usuario participa
    for proye in lista_todos_proyectos:
        if proye.es_participante(request.user.id):
            lista_proyectos_usuario.append(proye)

    # filtrar según estado
    if filtro == 'todos':
        lista_proyectos = lista_proyectos_usuario
    else:
        for proyecto in lista_proyectos_usuario:
            if proyecto.estado == filtro:
                lista_proyectos.append(proyecto)

    return render(request, 'configuracion/proyecto_ver_todos.html', {'lista_proyectos': lista_proyectos,
                                                                     'filtro': filtro,
                                                                     'cancelado': Proyecto.ESTADO_CANCELADO,
                                                                     'ejecucion': Proyecto.ESTADO_EN_EJECUCION})


def ver_proyecto(request, id_proyecto):
    """
    Esta vista despliega un proyecto con todas sus fases e items

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: Se recibe como parámetro el id_del proyecto que se desea ver
    :return: objeto que renderea verProyecto.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    # lista de items
    lista_items = Item.objects.all()
    # filtro de tipos de items que aún no fueron usados (para todas las fases)

    es_aprobador = False
    if request.user.id == proyecto.gerente:
        es_aprobador = True

    return render(request, 'configuracion/proyecto_ver_unico.html', {'proyecto': proyecto})