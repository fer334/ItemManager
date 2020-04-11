

from django.shortcuts import render, redirect
from .SubirArchivos import handle_uploaded_file
from desarrollo.models import Item, AtributoParticular
from administracion.models import Proyecto, TipoItem, Fase
from desarrollo.forms import ItemForm


def crear_item(request, id_fase, id_tipo):
    fase = Fase.objects.get(pk=id_fase)
    tipo = TipoItem.objects.get(pk=id_tipo)
    plantilla_atr = tipo.plantillaatributo_set.all().order_by('id')

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
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
                if atr.tipo == 'file':
                    valor = handle_uploaded_file(request.FILES[atr.nombre], fase.proyecto.id, request.user)
                else:
                    valor = request.POST[atr.nombre]
                nuevo_atributo = AtributoParticular(item=nuevo_item, nombre=atr.nombre, tipo=atr.tipo, valor=valor)
                nuevo_atributo.save()

            return redirect('desarrollo:verProyecto', id_proyecto= fase.proyecto.id)
    else:
        form = ItemForm()

    return render(request, 'desarrollo/item_crear.html', {'fase': fase, 'tipo': tipo, 'form': form,
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
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render(request, 'desarrollo/proyecto_ver_unico.html', {'proyecto': proyecto})


def adjuntar_archivo(request, id_proyecto, id_item):
    context = {}
    if request.POST:
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            url = handle_uploaded_file(request.FILES['archivo_adjunto'], id_proyecto, request.user)
            print(url)
    else:
        form = ItemForm()
    context['form'] = form
    return render(request, "desarrollo/item_adjuntar_archivo.html", context)




def solicitud_aprobacion(request, id_item):
    item = Item.objects.get(pk=id_item)
    if item.estado == 'en desarrollo':
        item.estado = 'pendiente de aprobacion'
    return render(request,'desarrollo/item_solicitar_aprobacion.html')


def aprobar_item(request,id_item, id_proyecto):
    item = Item.objects.get(pk=id_item)
    proyecto = Proyecto.objects.get(pk= id_proyecto)
    if proyecto.gerente.rol == 'Aprobador' or proyecto.participante.rol == 'Aprobador' and item.estado == 'pendiente de aprobacion':
       item.estado = 'aprobado'
    return render(request,'desarrollo/item_aprobar.html')


def desactivar_item(request, id_item, id_fase):
    item = Item.objects.get(pk=id_item)
    fase = Fase.objects.get(pk=id_fase)
    if item.estado == 'en desarrollo':
        item.estado ='desactivado'
        item.fase.remove(fase)
    return render(request, 'desarrollo/item_desactivar.html')
