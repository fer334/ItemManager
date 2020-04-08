from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse
from desarrollo.models import Item, AtributoParticular
from administracion.models import Proyecto, TipoItem, Fase
from desarrollo.forms import ItemForm


# Create your views here.

def crear_item(request, id_fase, id_tipo):
    fase = Fase.objects.get(pk=id_fase)
    proyecto = fase.proyecto
    tipo = TipoItem.objects.get(pk=id_tipo)
    plantilla_atr = tipo.plantillaatributo_set.all().order_by('id')

    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            # creamos el ítem
            nombre = form.cleaned_data['nombre']
            complejidad = form.cleaned_data['complejidad']
            descripcion = form.cleaned_data['descripcion']
            nuevo_item = Item(nombre=nombre, complejidad=complejidad, descripcion=descripcion, tipo_item=tipo,
                              fase=fase)
            nuevo_item.save()
            # luego creamos los atributos del ítem
            for atr in plantilla_atr:
                valor = request.POST[atr.nombre]
                nuevo_atributo = AtributoParticular(item=nuevo_item, nombre=atr.nombre, tipo=atr.tipo, valor=valor)
                nuevo_atributo.save()
            return HttpResponseRedirect(reverse('desarrollo:verProyecto', args=[proyecto.id]))
    else:
        form = ItemForm()

    return render(request, 'desarrollo/crearItem.html', {'fase': fase, 'tipo': tipo, 'form': form,
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
    # lista de tipos de ítem del proyecto
    lista_tipos = TipoItem.objects.all().filter(proyecto=proyecto)
    # lista de items
    lista_items = Item.objects.all()
    return render(request, 'desarrollo/proyecto_ver_unico.html', {'proyecto': proyecto, 'lista_tipos': lista_tipos,
                                                                  'lista_items': lista_items})
