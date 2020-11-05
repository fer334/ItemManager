"""
Vistas del modulo de configuracion
"""
from datetime import datetime, date

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from administracion.models import Proyecto, Fase, Rol
from .models import LineaBase, Solicitud, VotoRuptura
from desarrollo.models import Item, HistoricalItem
from login.models import Usuario
from django.utils.timezone import now
from desarrollo.views import calcular_impacto_recursivo, crear_lista_relaciones_del_proyecto, \
    calcular_lista_items_impacto_recursivo
from desarrollo.getPermisos import has_permiso, has_permiso_cerrar_proyecto
from django.core.mail import send_mail
from .reporte import ReporteProyecto


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
    es_comite = request.user in proyecto.comite.all()
    es_gerente = request.user.id == proyecto.gerente
    puede_cerrar = has_permiso_cerrar_proyecto(proyecto, request.user)
    return render(request, 'configuracion/proyecto_ver_unico.html', {
        'proyecto': proyecto,
        'es_comite': es_comite,
        'es_gerente': es_gerente,
        'puede_cerrar': puede_cerrar
    })


def numeracion_lb_en_proyecto(proyecto):
    """
    retorna el valor para cargar la numeración en la linea base

    :param proyecto: proyecto seleccionado
    :return: entero con la numeración de la linea base
    :rtype: int
    """
    ultima_lb = LineaBase.objects.filter(fase__proyecto=proyecto,
                                         estado__regex='^(?!' + LineaBase.ESTADO_ROTA + ')').order_by(
        'numeracion').last()
    if ultima_lb:
        return ultima_lb.numeracion + 1
    else:
        return 1


def crear_linea_base(request, id_fase):
    """
    Esta vista despliega el template para iniciar la creacion de una linea base y se encarga de la creacion de una en
    caso de recibir un request POST

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_fase: Se recibe como parámetro la fase en la que se creara la linea base
    :return: objeto que renderea lineabase_crear.html
    :rtype: render
    """
    fase = Fase.objects.get(pk=id_fase)
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.CREAR_LINEA_BASE):
        return redirect('administracion:accesoDenegado', id_proyecto=fase.proyecto.id, caso='permisos')
    if request.method == 'POST':
        items = [Item.objects.get(pk=item.split('-')[1]) for item in request.POST if len(item.split('-')) > 1]
        if len(items) > 0:
            nueva_linea_base = LineaBase()
            nueva_linea_base.fase = fase
            nueva_linea_base.creador = Usuario.objects.get(pk=request.user.id)
            nueva_linea_base.numeracion = numeracion_lb_en_proyecto(fase.proyecto)
            if len(items) == len(fase.item_set.all()):
                nueva_linea_base.tipo = LineaBase.TIPO_TOTAL

            nueva_linea_base.save()
            for item in items:
                item.estado = Item.ESTADO_LINEABASE
                item.save()

                # registramos para auditoría
                auditoria = HistoricalItem(item=item, history_user=request.user,
                                           history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_LINEABASE)
                auditoria.save()

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
    # parte para desaprobar items
    desaprobaciones = []
    for solicitud_desaprobar in Solicitud.objects.filter(linea_base=None, solicitud_activa=True):
        # query primero por los items, luego busca la fase, luego el proyecto
        if solicitud_desaprobar.items_a_modificar.last().fase.proyecto.id == id_proyecto:
            solicitud_desaprobar.solicitante_ha_votado = solicitud_desaprobar.ha_votado(request.user)
            desaprobaciones.append(solicitud_desaprobar)
    return render(request, 'configuracion/comite_index.html', {
        'proyecto': proyecto,
        'solicitudes': solicitudes,
        'desaprobaciones': desaprobaciones,
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
    fase = lineabase.fase
    proyecto = fase.proyecto
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.SOLICITAR_RUPTURA_LB):
        return redirect('administracion:accesoDenegado', id_proyecto=proyecto.id, caso='permisos')
    lista_calculo_impacto = []
    for item_en_lb in lineabase.items.all():
        lista_calculo_impacto.append(calcular_impacto_recursivo(item_en_lb))
    if request.POST:
        solicitud = Solicitud(
            solicitado_por=request.user,
            linea_base_id=id_lineabase,
            justificacion=request.POST['mensaje'],
        )
        solicitud.save()
        send_mail('Nueva solicitud de ruptura', f'El usuario {request.user.username} ha solicitado una ruptura de la '
        f'linea base {lineabase.id} en el proyecto {proyecto.nombre}', 'isteampoli2020@gmail.com',
        [integrante.email for integrante in proyecto.comite.all()], fail_silently=False)
        items_seleccionados = [
            Item.objects.get(pk=item.split('-')[1])
            for item in request.POST
            if len(item.split('-')) > 1
        ]

        for item in items_seleccionados:
            solicitud.items_a_modificar.add(item)
        return redirect('configuracion:verLineaBase', id_lineabase)

    return render(request, 'configuracion/solicitud_ruptura.html', {'lineabase': lineabase,
                                                                    'lista_impacto': lista_calculo_impacto})


def votar_solicitud(request, id_proyecto, id_solicitud, voto):
    """
    Metodo que se encarga de registrar un voto en la solicitudes en la base de datos.

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador unico por proyecto
    :param id_solicitud: identificador unico por proyecto
    :param voto: valor numerico que simboliza el voto, 1 para Voto a favor, 0 para voto en contra
    :return: objeto que renderea verIndexComite.html
    :rtype: render
    """
    solicitud = Solicitud.objects.get(pk=id_solicitud)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    nuevo_voto = VotoRuptura(solicitud=solicitud, votante=request.user, valor_voto=(voto == 1))
    nuevo_voto.save()
    votos = len(solicitud.votoruptura_set.all())
    if votos >= proyecto.cant_comite:
        votos_favor = len(solicitud.votoruptura_set.filter(valor_voto=True))
        if votos_favor > proyecto.cant_comite / 2:
            if solicitud.linea_base is not None:
                # print('QUE: ' + solicitud.linea_base)
                # Si es la solicitud de linea base:
                solicitud.linea_base.estado = LineaBase.ESTADO_ROTA
                solicitud.linea_base.save()
                for item in solicitud.linea_base.items.all():
                    if item in solicitud.items_a_modificar.all():
                        item.estado = Item.ESTADO_REVISION

                        # registramos para auditoría
                        auditoria = HistoricalItem(item=item, history_user=request.user,
                                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_REVISION)
                        auditoria.save()

                    else:
                        item.estado = Item.ESTADO_APROBADO

                        # registramos para auditoría
                        auditoria = HistoricalItem(item=item, history_user=request.user,
                                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_APROBADO)
                        auditoria.save()

                    item.save()
            else:
                # Si es una solicitud de desaprobacion de items:
                for item in solicitud.items_a_modificar.all():
                    item.estado = Item.ESTADO_DESARROLLO
                    item.save()

                    # registramos para auditoría
                    auditoria = HistoricalItem(item=item, history_user=request.user,
                                               history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_DESARROLLO)
                    auditoria.save()

        solicitud.solicitud_activa = False
        solicitud.save()
        if solicitud.linea_base.estado == LineaBase.ESTADO_ROTA:
            texto = f'La linea base {solicitud.linea_base.id} en el proyecto {proyecto.nombre} ha sido rota'
        else:
            texto = f'La linea base {solicitud.linea_base.id} en el proyecto {proyecto.nombre} NO ha sido rota'
        send_mail('Solicitud finalizada', texto,
                  'isteampoli2020@gmail.com',
                  [integrante.email for integrante in proyecto.comite.all()], fail_silently=False)
    return redirect('configuracion:verIndexComite', id_proyecto)


def cerrar_proyecto(request, id_proyecto):
    """
    Metodo que se encarga de renderizar la vista cerrar proyecto. El proyecto solo se puede cerrar si lo solicita
    el gerente y si todas las fases estan cerradas. Si recibe un post verifica nuevamente si el proyecto es cerrable y
    lo cierra

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador unico por proyecto
    :return: objeto que renderea item_des_relacion.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = proyecto.fase_set.all()

    # Para mostrar el numero correcto de la fase
    for i, fase in enumerate(fases):
        fase.nro_de_fase = i + 1
        fase.cerrable = False

    # Comprobacion de gerencia de proyecto
    es_cerrable = len(fases.filter(estado=Fase.FASE_ESTADO_CERRADA)) == proyecto.numero_fases
    # Dict a ser enviado a la vista
    content = {
        'proyecto': proyecto,
        'fases': fases,
        'es_cerrable': es_cerrable,
        'mensaje_error': "",
    }

    # Si el request es POST cierra el proyecto
    if request.method == "POST":
        if es_cerrable and has_permiso_cerrar_proyecto(proyecto, request.user):
            proyecto.estado = proyecto.ESTADO_FINALIZADO
            proyecto.fecha_finalizado = now()
            proyecto.save()
            return redirect('login:index')

    return render(request, 'configuracion/proyecto_cerrar.html', content)


def trazabilidad(request, id_proyecto, id_item):
    """
    Vista que se encarga de calcular y mostrar la gráfica de trazabilidad de una determinada variable

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto actual
    :param id_item: identificador del ítem sobre el cual se calculará la trazabilidad
    :return: objeto que renderea item_trazabilidad.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    fases = proyecto.fase_set.all().order_by('id')
    item = Item.objects.get(pk=id_item)
    relaciones = crear_lista_relaciones_del_proyecto(id_proyecto)
    # primero creamos una lista que contiene solo al primer item
    items = [item]
    # luego con funciones recursivas vamos añadiendo los demás elementos a la lista
    items += ramas_recursivas_trazabilidad(item, 'izquierda', item.antecesores.all())
    items += ramas_recursivas_trazabilidad(item, 'izquierda', item.padres.all())
    items += ramas_recursivas_trazabilidad(item, 'derecha', item.sucesores.all())
    items += ramas_recursivas_trazabilidad(item, 'derecha', item.hijos.all())
    # ahora eliminamos elementos duplicados con los sets de python
    setitems = set(items)
    # generamos los datos requeridos para mostrar el cálculo de impacto
    impacto = calcular_impacto_recursivo(item)
    lista_impacto = calcular_lista_items_impacto_recursivo(item)
    lista_fases_impacto = []
    for items_impacto in lista_impacto:
        lista_fases_impacto.append(items_impacto.fase)
    # convertimos en set para que no hayan repetidos
    lista_fases_impacto = set(lista_fases_impacto)

    return render(request, 'configuracion/item_trazabilidad.html', {'item_principal': item, 'fases': fases,
                                                                    'lista_items': setitems, 'proyecto': proyecto,
                                                                    'desactivado': Item.ESTADO_DESACTIVADO,
                                                                    'relaciones': relaciones, 'impacto': impacto,
                                                                    'lista_impacto': lista_impacto,
                                                                    'lista_fases_impacto': lista_fases_impacto})


def ramas_recursivas_trazabilidad(item, caso, lista):
    """
    función recursiva que se va expandiendo y añadiendo items a la lista ya sea hacia la izquierda o hacia
    la derecha del arbol de relaciones de un ítem determinado

    :param item: item sobre el que se calculara sus items relacionado
    :param caso: el caso indica si estamos viendo las ramificaciones de la derecha o las de la izquierda
    :param lista: la lista ya sea de antecesores, sucesores, padres o hijos del ítem elegido
    :return: lista de items
    """
    lista_items = []
    for item_relacionado in lista:
        # nos aseguramos de tener la versión más actual del hijo que no esté desactivada
        item_actual = Item.objects.filter(id_version=item_relacionado.id_version,
                                          estado__regex='^(?!' + Item.ESTADO_DESACTIVADO + ')').order_by('id').last()
        lista_items.append(item_actual)
        # sumamos las listas para luego retornarlas
        if caso == 'izquierda':
            lista_items += ramas_recursivas_trazabilidad(item_actual, caso, item_actual.antecesores.all())
            lista_items += ramas_recursivas_trazabilidad(item_actual, caso, item_actual.padres.all())
        elif caso == 'derecha':
            lista_items += ramas_recursivas_trazabilidad(item_actual, caso, item_actual.sucesores.all())
            lista_items += ramas_recursivas_trazabilidad(item_actual, caso, item_actual.hijos.all())
    return lista_items


# posible implementación para la parte gráfica de ver items en las fases con sus relaciones
# def trazabilidad(request, id_proyecto, id_item):
#     proyecto = Proyecto.objects.get(pk=id_proyecto)
#     fases = proyecto.fase_set.all().order_by('id')
#     item = Item.objects.get(pk=id_item)
#     relaciones = crear_lista_relaciones_del_proyecto(id_proyecto)
#     items = []
#     for fase in proyecto.fase_set.all():
#         for item in fase.item_set.all():
#             items.append(item)
#     return render(request, 'configuracion/item_trazabilidad.html', {'item': item,'fases': fases, 'lista_items': items,
#                                                                     'desactivado': Item.ESTADO_DESACTIVADO,
#                                                                     'relaciones': relaciones})


def reporte_trazabilidad(request, id_proyecto, id_item):
    """
    futura implementación de generar reporte de trazabilidad

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_item: identificador del item
    :param id_proyecto: identificador del proyecto
    :return:
    """

    return render(request, 'configuracion/item_trazabilidad_reporte.html', {'id_proyecto': id_proyecto,
                                                                            'id_item': id_item})


def solicitud_modificacion_estado(request, id_proyecto, id_item):
    """
    Funcion en donde se realiza la solicitud de desaprobación de un item al comite,
    para poder modificar su estado, esto es posible si el item esta en estado APROBADO,
    luego se lleva a votacion por el comite y si se aprueba en su mayoria el item pasa a
    estado EN DESARROLLO, para poder modificarlo a gusto.

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del item
    :param id_item: identificador del proyecto
    :return: redirige a la pagina del proyecto una vez que se haya solicitado la desaprobacion
    """
    item = Item.objects.get(pk=id_item)
    if request.POST:
        solicitud = Solicitud(
            solicitado_por=request.user,
            justificacion=request.POST['mensaje'],
        )
        solicitud.save()
        items_seleccionados = [
            Item.objects.get(pk=item.id)
        ]

        for item in items_seleccionados:
            solicitud.items_a_modificar.add(item)
        return redirect('configuracion:verProyecto', id_proyecto=id_proyecto)


def reporte(request, id_proyecto):
    """
    Vista donde se genera el archivo pdf utilizado en los reportes, recibe a traves
    del request la lista de fases seleccionadas para el reporte y las fechas de inicio
    y fin para el rango de Solicitudes

    :param request: lista de fases y fechas de inicio y fin
    :param id_proyecto: identificador del proyecto
    :return: retorna como respuesta la descarga del archivo pdf
    """
    if request.POST:
        fases = [int(x.split('-')[1]) for x in request.POST if x.__contains__('check')]
        inicio = [int(x) for x in str(request.POST['inicio']).split('-')]
        fin = [int(x) for x in str(request.POST['fin']).split('-')]
        fecha_ini = date(inicio[0], inicio[1], inicio[2])
        fecha_fin = date(fin[0], fin[1], fin[2])
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'
        r = ReporteProyecto()
        response.write(r.run(id_proyecto, fases, fecha_ini, fecha_fin))
        return response
