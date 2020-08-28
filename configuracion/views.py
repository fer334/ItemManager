from django.shortcuts import render, redirect

# Create your views here.
from administracion.models import Proyecto, Fase
from .models import LineaBase, Solicitud, VotoRuptura
from desarrollo.models import Item
from login.models import Usuario


def index(request, filtro):
    """
    Vista que despliega la lista de proyectos con su estado actual, también permite filtrar los proyectos según estado.

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
    es_comite = False
    if request.user in proyecto.comite.all():
        es_comite = True

    return render(request, 'configuracion/proyecto_ver_unico.html', {'proyecto': proyecto, 'es_comite': es_comite})


def crear_linea_base(request, id_fase):
    """
    Esta vista despliega el template para iniciar la creacion de una linea base y se encarga de la creacion de una en
    caso de recibir un request POST

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: Se recibe como parámetro la fase en la que se creara la linea base
    :return: objeto que renderea lineabase_crear.html
    :rtype: render
    """
    fase = Fase.objects.get(pk=id_fase)
    if request.method == 'POST':
        items = [Item.objects.get(pk=item.split('-')[1]) for item in request.POST if len(item.split('-')) > 1]
        if len(items) > 0:
            nueva_linea_base = LineaBase()
            nueva_linea_base.fase = fase
            nueva_linea_base.creador = Usuario.objects.get(pk=request.user.id)
            if len(items) == len(fase.item_set.all()):
                nueva_linea_base.tipo = LineaBase.TIPO_TOTAL

            nueva_linea_base.save()
            for item in items:
                item.estado = Item.ESTADO_LINEABASE
                item.save()
                nueva_linea_base.items.add(item)
            nueva_linea_base.save()
        return redirect('configuracion:verProyecto', id_proyecto=fase.proyecto_id)
    return render(request, 'configuracion/lineabase_crear.html', {'fase': fase})


def ver_linea_base(request, id_lineabase):
    """
    Esta vista despliega el template para ver detalles de una linea base

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_lineabase: Se recibe como parámetro el id de la linea base
    :return: objeto que renderea lineabase_ver.html
    :rtype: render
    """
    lineabase = LineaBase.objects.get(pk=id_lineabase)
    return render(request, 'configuracion/lineabase_ver.html', {'lineabase': lineabase})


def comite_index(request, id_proyecto):
    """
    Esta vista despliega el template para ver el index del comite

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: Se recibe como parámetro el id_del proyecto que se desea ver
    :return: objeto que renderea comite_index.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    lbs_del_proyecto = []
    for fase in proyecto.fase_set.all():
        lbs_del_proyecto = lbs_del_proyecto + [lb for lb in fase.lineabase_set.all()]
    solicitudes = []
    for lb in lbs_del_proyecto:
        for solicitud in lb.solicitud_set.all():
            if solicitud.solicitud_activa:
                solicitud.solicitante_ha_votado = solicitud.ha_votado(request.user)
                solicitudes.append(solicitud)
    return render(request, 'configuracion/comite_index.html', {
        'proyecto': proyecto,
        'solicitudes': solicitudes,
        'usuario': request.user
    })


def solicitud_ruptura(request, id_lineabase):
    """
    Vista utilizada para realizar solicitudes de ruptura de LB's

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_lineabase: Se recibe como parámetro el id de la linea base
    :return: objeto que renderea solicitud_ruptura.html
    :rtype: render
    """
    lineabase = LineaBase.objects.get(pk=id_lineabase)
    if request.POST:
        solicitud = Solicitud(
            solicitado_por=request.user,
            linea_base_id=id_lineabase,
            justificacion=request.POST['mensaje'],
        )
        solicitud.save()

        items_seleccionados = [Item.objects.get(pk=item.split('-')[1]) for item in request.POST if len(item.split('-')) > 1]
        for item in items_seleccionados:
            solicitud.items_a_modificar.add(item)
        return redirect('configuracion:verLineaBase', id_lineabase)

    return render(request, 'configuracion/solicitud_ruptura.html', {'lineabase': lineabase})


def votar_solicitud(request, id_proyecto, id_solicitud, voto):
    solicitud = Solicitud.objects.get(pk=id_solicitud)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    nuevo_voto = VotoRuptura(solicitud=solicitud, votante=request.user, valor_voto=(voto == 1))
    nuevo_voto.save()
    votos = len(solicitud.votoruptura_set.all())
    if votos == proyecto.cant_comite:
        votos_favor = len(solicitud.votoruptura_set.filter(valor_voto=True))
        if votos_favor > proyecto.cant_comite / 2:
            solicitud.linea_base.estado = LineaBase.ESTADO_ROTA
            solicitud.linea_base.save()
            for item in solicitud.items_a_modificar.all():
                item.estado = Item.ESTADO_REVISION
                item.save()

        solicitud.solicitud_activa = False
        solicitud.save()

    return redirect('configuracion:verIndexComite', id_proyecto)
