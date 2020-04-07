from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from administracion.models import Proyecto
from django.urls import reverse

from desarrollo.models import Item, AtributoParticular
from administracion.models import  Proyecto, TipoItem
from desarrollo.forms import ItemForm


# Create your views here.

def crear_item(request, id_proyecto, id_tipo):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    tipo = TipoItem.objects.get(pk=id_tipo)
    plantilla_atr = tipo.plantillaatributo_set.all()
    if request.method == "POST":
        form = ItemForm(request.POST)
        nuevo_item = Item(nombre=tipo.prefijo, tipo_item=tipo, proyecto=proyecto)
        # primero creamos los atributos del ítem
        for atr in plantilla_atr:
            nuevo_atributo = AtributoParticular(item=nuevo_item, nombre=atr.nombre, tipo=atr.tipo,
                                                es_requerido=atr.es_requerido)
            nuevo_atributo.save()
        if form.is_valid():
            form.save()
            return redirect('login:index')
    else:
        form = ItemForm()

    return render(request, 'desarrollo/crearItem.html', {'proyecto': proyecto, 'tipo': tipo, 'form': form,
                                                         'plantilla_atr': plantilla_atr})


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
    proyecto = Proyecto.objects.get(pk= id_proyecto)
    return render(request, 'desarrollo/proyecto_ver_unico.html', {'proyecto': proyecto})
