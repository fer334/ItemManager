"""
Modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .SubirArchivos import handle_uploaded_file
from desarrollo.models import Item, AtributoParticular, HistoricalItem
from administracion.models import Proyecto, TipoItem, Fase, Rol
from desarrollo.forms import ItemForm
from desarrollo.getPermisos import has_permiso
from configuracion.models import Solicitud, LineaBase
from login.models import Usuario


def get_numeracion(fase, tipo):
    """
    genera los numeros de item en una fase del mismo tipo de item

    :param fase: fase actual
    :param tipo: tipo del item actual
    :return: entero con el numero de item
    :rtype: int
    """
    items_del_tipo = fase.item_set.filter(tipo_item=tipo, estado__in=(Item.ESTADO_REVISION,
                                                                      Item.ESTADO_APROBADO,
                                                                      Item.ESTADO_LINEABASE,
                                                                      Item.ESTADO_DESARROLLO,
                                                                      Item.ESTADO_PENDIENTE))
    if (items_del_tipo):
        ultimo_numero = items_del_tipo.order_by('numeracion').last().numeracion
        return ultimo_numero + 1
    else:
        return 1


def crear_item(request, id_fase, id_tipo):
    """
    Esta vista se encarga de crear un ítem con sus atributos particulares en una fase, utiliza un form para los
    atributos comunes del ítem y luego con el ítem ya creado crea sus atributos particulares. También se encarga de
    vincular el tipo del ítem creado a la fase.

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_fase: identificador de la fase en la cual será creado el ítem
    :param id_tipo: identificar del tipo del ítem
    :return: objeto que se encarga de renderear item_crear.html o redireccion a proyecto_ver_unico.html en caso de POST
    :rtype: render, redirect
    """
    fase = Fase.objects.get(pk=id_fase)
    # primero verificamos que cumpla con el permiso
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.CREAR_ITEM):
        return redirect('administracion:accesoDenegado', id_proyecto=fase.proyecto.id, caso='permisos')

    tipo = TipoItem.objects.get(pk=id_tipo)
    plantilla_atr = tipo.plantillaatributo_set.all().order_by('id')

    # filtro de tipos de items que aún no fueron usados (para todas las fases)
    tipos_de_items_usados = []
    lista_tipos_disponibles = []
    for f in fase.proyecto.fase_set.all():
        tipos_de_items_usados = tipos_de_items_usados + list(f.tipos_item.all())
        lista_tipos_disponibles = [tipo_restante for tipo_restante in fase.proyecto.tipoitem_set.all() if
                                   tipo_restante not in tipos_de_items_usados]

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # verificamos que el tipo elegido sea valido para la fase
            if tipo in fase.tipos_item.all() or tipo in lista_tipos_disponibles:
                # creamos el ítem
                nombre = form.cleaned_data['nombre']
                complejidad = form.cleaned_data['complejidad']
                descripcion = form.cleaned_data['descripcion']
                nuevo_item = Item(nombre=nombre, complejidad=complejidad, descripcion=descripcion, tipo_item=tipo,
                                  fase=fase, numeracion=get_numeracion(fase, tipo))
                nuevo_item.save()
                # añadimos el id de la primera versión a este campo y se pasará a las versiones posteriores
                nuevo_item.id_version = nuevo_item.id
                nuevo_item.save()

                # registramos para auditoría
                auditoria = HistoricalItem(item=nuevo_item, history_user=request.user,
                                           history_type=HistoricalItem.TIPO_CREAR)
                auditoria.save()

                # vinculamos el tipo a la fase
                if tipo not in fase.tipos_item.all():
                    fase.tipos_item.add(tipo)
                # luego creamos los atributos del ítem
                for atr in plantilla_atr:
                    if atr.tipo == 'file' and request.FILES:
                        valor = handle_uploaded_file(request.FILES[atr.nombre], fase.proyecto.id, request.user)
                    else:
                        valor = request.POST[atr.nombre]
                    nuevo_atributo = AtributoParticular(item=nuevo_item, nombre=atr.nombre, tipo=atr.tipo, valor=valor)
                    nuevo_atributo.save()

                return redirect('desarrollo:verProyecto', id_proyecto=fase.proyecto.id)
            # si el tipo no es válido
            else:
                return redirect('administracion:accesoDenegado', id_proyecto=fase.proyecto.id, caso='tiponovalido')
    else:
        form = ItemForm()

    return render(request, 'desarrollo/item_crear.html', {'fase': fase, 'tipo': tipo, 'form': form,
                                                          'plantilla_atr': plantilla_atr})


def ver_item(request, id_proyecto, id_item):
    """
    vista que se encarga de mostrar un ítem con todos sus datos, atributos comunes y particulares y proyecto y fase
    a la que pertenece

    :param id_proyecto: identificador del proyecto
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_item: identificador del ítem a mostrar
    :return: objeto que se encarga de renderear item_ver.html
    :rtype: render
    """
    item = Item.objects.get(pk=id_item)
    lista_atributos = AtributoParticular.objects.filter(item=item)
    fase = item.fase
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.VER_ITEM):
        return redirect('administracion:accesoDenegado', id_proyecto=fase.proyecto.id, caso='permisos')

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    impacto = calcular_impacto_recursivo(item)
    lista_impacto = calcular_lista_items_impacto_recursivo(item)
    lista_fases_impacto = []
    for items_impacto in lista_impacto:
        lista_fases_impacto.append(items_impacto.fase)
    # convertimos en set para que no hayan repetidos
    lista_fases_impacto = set(lista_fases_impacto)
    # verificamos si la versión es la más actual para emitir un mensaje (solo para items desactivados)
    es_version_actual = False
    if item == Item.objects.filter(id_version=item.id_version).order_by('id').last():
        es_version_actual = True
    return render(request, 'desarrollo/item_ver.html', {'item': item, 'lista_atributos': lista_atributos, 'fase': fase,
                                                        'proyecto': proyecto, 'desarrollo': Item.ESTADO_DESARROLLO,
                                                        'estado': Proyecto.ESTADO_EN_EJECUCION, 'impacto': impacto,
                                                        'lista_impacto': lista_impacto, 'lista_fases_impacto':
                                                            lista_fases_impacto, 'es_vers_actual': es_version_actual})


def historial_versiones_item(request, id_proyecto, id_item):
    """
    Vista que permite ver las versiones que un item tuvo a lo largo del tiempo y las diferencias entre estas versiones

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: Identificador del proyecto actual
    :param id_item: Identificador del ítem del cual se verán sus versiones
    :return: objeto que renderea item_historial_versiones.html
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    item = Item.objects.get(pk=id_item)
    lista_atributos = AtributoParticular.objects.filter(item=item)
    lista_versiones = []
    item_aux = item
    # mientras que el item tenga una referencia a un item anterior
    while item_aux.version_anterior is not None:
        # vamos añadiendo las versiones anteriores a la lista
        lista_versiones.append(item_aux.version_anterior)
        # cambiamos al item de la version anterior
        item_aux = item_aux.version_anterior
    return render(request, 'desarrollo/item_historial_versiones.html', {'lista_versiones': lista_versiones,
                                                                        'item_actual': item, 'proyecto': proyecto,
                                                                        'lista_atributos': lista_atributos,
                                                                        'desarrollo': Item.ESTADO_DESARROLLO})


def validar_reversion(id_item, id_version_anterior):
    """
    Función que se encarga de validar que se cumplan las restricciones para poder reversionar un item

    :param id_item: identificador de la version actual
    :param id_version_anterior: identificador de la versión a reversionar
    :return: variable booleana que retorna true si se cumplen todas las restricciones y false si no
    """
    valido = True
    item_actual = Item.objects.get(pk=id_item)
    # si el estado del ítem no es en desarrollo no se debe poder reversionar
    if item_actual.estado != Item.ESTADO_DESARROLLO:
        valido = False
    return valido


def reversionar_item(request, id_proyecto, id_item, id_version_anterior):
    """
    Vista que se encarga de crear una nueva versión de un ítem restaurando los datos de una versión anterior

    :param id_version_anterior: identificador de la versión a restaurar
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto actual
    :param id_item:  identificador de la versión actual del ítem
    :return: redireccion a item_ver.html
    :rtype: redirect
    """
    it = Item.objects.get(pk=id_item)
    fase = it.fase
    # primero verificamos que cumpla con el permiso
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.REVERSIONAR_ITEM):
        return redirect('administracion:accesoDenegado', id_proyecto=fase.proyecto.id, caso='permisos')

    if validar_reversion(id_item, id_version_anterior):
        item_actual = Item.objects.get(pk=id_item)
        item_version_anterior = Item.objects.get(pk=id_version_anterior)
        # creamos una nueva versión a partir de la version anterior elegida
        nuevo_item = versionar_item(item_version_anterior, request.user)
        # modificamos su version_anterior para que apunte a la ultima versión antes que esta
        nuevo_item.version_anterior = item_actual
        # editamos su versión
        nuevo_item.version = item_actual.version + 1
        # pasamos su estado a En Desarrollo porque la versión no actual siempre está en estado desactivado
        nuevo_item.estado = item_actual.estado
        # guardamos los cambios
        nuevo_item.save()
        # también debemos cambiar el estado de item_actual a desactivado
        item_actual.estado = Item.ESTADO_DESACTIVADO
        item_actual.save()

        # ahora nos encargamos de las relaciones
        # primero reversionamos item actual para actualizar los items en sus listas de relaciones a la versión más nueva
        nuevo_item_actual = versionar_item(item_actual, request.user)
        # desactivamos para que esta versión no cuente como nueva, solo usaremos para las relaciones
        nuevo_item_actual.estado = Item.ESTADO_DESACTIVADO
        nuevo_item_actual.save()
        # para antecesores
        # primero hacemos diferencia para ver los ítems que no estában añadidos en la versión anterior
        lista_antecesores_add = []
        lista_antecesores_add = nuevo_item.antecesores.all().difference(nuevo_item_actual.antecesores.all())
        for item_relacion in lista_antecesores_add:
            item_relacion.sucesores.add(nuevo_item)
        # para la intersección tenemos que desvincular el item actual del ítem relación y vincular al nuevo_item
        lista_antecesores_add = []
        lista_antecesores_add = nuevo_item.antecesores.all().intersection(nuevo_item_actual.antecesores.all())
        for item_relacion in lista_antecesores_add:
            item_relacion.sucesores.remove(item_relacion.sucesores.get(id_version=nuevo_item_actual.id_version))
            item_relacion.sucesores.add(nuevo_item)
        # ahora hacemos la diferencia pero invertida para ver a que items desvincular item actual
        lista_antecesores_add = []
        lista_antecesores_add = nuevo_item_actual.antecesores.all().difference(nuevo_item.antecesores.all())
        for item_relacion in lista_antecesores_add:
            item_relacion.sucesores.remove(item_relacion.sucesores.get(id_version=nuevo_item_actual.id_version))
        # para sucesores
        lista_sucesores_add = []
        lista_sucesores_add = nuevo_item.sucesores.all().difference(nuevo_item_actual.sucesores.all())
        for item_relacion in lista_sucesores_add:
            item_relacion.antecesores.add(nuevo_item)
        lista_sucesores_add = []
        lista_sucesores_add = nuevo_item.sucesores.all().intersection(nuevo_item_actual.sucesores.all())
        for item_relacion in lista_sucesores_add:
            item_relacion.antecesores.remove(item_relacion.antecesores.get(id_version=nuevo_item_actual.id_version))
            item_relacion.antecesores.add(nuevo_item)
        lista_sucesores_add = []
        lista_sucesores_add = nuevo_item_actual.sucesores.all().difference(nuevo_item.sucesores.all())
        for item_relacion in lista_sucesores_add:
            item_relacion.antecesores.remove(item_relacion.antecesores.get(id_version=nuevo_item_actual.id_version))
        # para padres
        lista_padres_add = []
        lista_padres_add = nuevo_item.padres.all().difference(nuevo_item_actual.padres.all())
        for item_relacion in lista_padres_add:
            item_relacion.hijos.add(nuevo_item)
        lista_padres_add = []
        lista_padres_add = nuevo_item.padres.all().intersection(nuevo_item_actual.padres.all())
        for item_relacion in lista_padres_add:
            item_relacion.hijos.remove(item_relacion.hijos.get(id_version=nuevo_item_actual.id_version))
            item_relacion.hijos.add(nuevo_item)
        lista_padres_add = []
        lista_padres_add = nuevo_item_actual.padres.all().difference(nuevo_item.padres.all())
        for item_relacion in lista_padres_add:
            item_relacion.hijos.remove(item_relacion.hijos.get(id_version=nuevo_item_actual.id_version))
        # para hijos
        lista_hijos_add = []
        lista_hijos_add = nuevo_item.hijos.all().difference(nuevo_item_actual.hijos.all())
        for item_relacion in lista_hijos_add:
            item_relacion.padres.add(nuevo_item)
        lista_hijos_add = []
        lista_hijos_add = nuevo_item.hijos.all().intersection(nuevo_item_actual.hijos.all())
        for item_relacion in lista_hijos_add:
            item_relacion.padres.remove(item_relacion.padres.get(id_version=nuevo_item_actual.id_version))
            item_relacion.padres.add(nuevo_item)
        lista_hijos_add = []
        lista_hijos_add = nuevo_item_actual.hijos.all().difference(nuevo_item.hijos.all())
        for item_relacion in lista_hijos_add:
            item_relacion.padres.remove(item_relacion.padres.get(id_version=nuevo_item_actual.id_version))

        # ahora validamos que todas las relaciones creadas para el item reversionado sean con items no desactivados
        validar_relaciones_desactivadas(nuevo_item.antecesores, nuevo_item.antecesores.all())
        validar_relaciones_desactivadas(nuevo_item.sucesores, nuevo_item.sucesores.all())
        validar_relaciones_desactivadas(nuevo_item.padres, nuevo_item.padres.all())
        validar_relaciones_desactivadas(nuevo_item.hijos, nuevo_item.hijos.all())

        # registramos para auditoría
        auditoria = HistoricalItem(item=nuevo_item, history_user=request.user,
                                   history_type=HistoricalItem.TIPO_REVERSIONAR)
        auditoria.save()
        return redirect('desarrollo:verItem', id_proyecto=id_proyecto, id_item=nuevo_item.id)
    else:
        return HttpResponse("No es posible revertir a esta versión porque no cumple con las restricciones")


def validar_relaciones_desactivadas(manytomany, lista_relaciones):
    """
    función que valida que no se reversionen relaciones con items desactivados

    :param manytomany:
    :param lista_relaciones:
    :return:
    """
    for item in lista_relaciones:
        if item.estado == Item.ESTADO_DESACTIVADO:
            manytomany.remove(item)


def menu_aprobacion(request, id_proyecto):
    """
    Vista que se encarga de mostrar un menú en el cual se permite administrar los ítems pendientes de aprobación
    si se tiene los permisos adecuados

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto sobre el cual se administraran los ítems
    :return: objeto que renderea item_menu_aprobacion.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    primera_fase = proyecto.fase_set.all().order_by('id').first()
    lista_items = Item.objects.all()
    # lista de fases en las que el usuario tiene permisos de aprobador
    lista_fases = []
    # si es gerente tendrá permisos en todas las fases
    if request.user.id == proyecto.gerente:
        lista_fases = proyecto.fase_set.all()
    # si no es gerente verificamos en que fases tiene permisos
    else:
        for fase in proyecto.fase_set.all():
            if has_permiso(fase, request.user, Rol.APROBAR_ITEM):
                lista_fases.append(fase)
    return render(request, 'desarrollo/item_menu_aprobacion.html', {'proyecto': proyecto, 'lista_items': lista_items,
                                                                    'estado': Item.ESTADO_PENDIENTE,
                                                                    'lista_fases': lista_fases,
                                                                    'primera_fase': primera_fase})


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

    return render(request, 'desarrollo/proyecto_ver_todos.html', {'lista_proyectos': lista_proyectos, 'filtro': filtro,
                                                                  'cancelado': Proyecto.ESTADO_CANCELADO,
                                                                  'ejecucion': Proyecto.ESTADO_EN_EJECUCION})


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
    # lista de items
    lista_items = Item.objects.all().order_by('numeracion')
    # filtro de tipos de items que aún no fueron usados (para todas las fases)
    tipos_de_items_usados = []
    for fase in proyecto.fase_set.all():
        tipos_de_items_usados = tipos_de_items_usados + list(fase.tipos_item.all())
    lista_tipos = [tipo_restante for tipo_restante in proyecto.tipoitem_set.all() if
                   tipo_restante not in tipos_de_items_usados]
    # condición para mostrar las opciones de aprobación de ítem
    # si es gerente del proyecto
    es_aprobador = False
    if request.user.id == proyecto.gerente:
        es_aprobador = True
    # o si el usuario tiene el permiso de aprobador
    for fases in proyecto.fase_set.all():
        if has_permiso(fases, request.user, Rol.APROBAR_ITEM):
            es_aprobador = True

    # codigo para ver los ítems actuales de un proyecto
    lista_items_actuales = []
    for fase in proyecto.fase_set.all():
        for item in fase.item_set.all():
            if item.estado != Item.ESTADO_DESACTIVADO:
                lista_items_actuales.append(item)

    return render(request, 'desarrollo/proyecto_ver_unico.html', {'proyecto': proyecto, 'lista_tipos': lista_tipos,
                                                                  'lista_items': lista_items,
                                                                  'estado': Proyecto.ESTADO_EN_EJECUCION,
                                                                  'desactivado': Item.ESTADO_DESACTIVADO,
                                                                  'es_aprobador': es_aprobador})


def relacionar_item(request, id_proyecto):
    """
    Metodo que se encarga de renderizar la vista relacionar items,
    recibe como parametro dos atributos, el request que es comun entre todas las
    vistas y el id_proyecto que tiene el numero identificador del proyecto donde
    se encuentran los items a relacionar

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador unico por proyecto
    :return: objeto que renderea relacion_crear.html
    :rtype: render
    """
    # Se filtra los items para solo relacionar items aprobados e hijos en desarrollo
    lista_items_padre = Item.objects.filter(
        fase__proyecto_id=id_proyecto, estado=Item.ESTADO_APROBADO
    ).union(
        Item.objects.filter(
            fase__proyecto_id=id_proyecto, estado=Item.ESTADO_LINEABASE
        )
    )
    lista_items_hijo = Item.objects.filter(
        fase__proyecto_id=id_proyecto, estado=Item.ESTADO_DESARROLLO
    )
    context = {
        'lista_items_hijo': lista_items_hijo,
        'lista_items_padre': lista_items_padre,
        'error': ""
    }

    if request.method == "POST":
        inicio = Item.objects.get(pk=request.POST['inicio'])
        fin = Item.objects.get(pk=request.POST['fin'])
        if inicio.id == fin.id:
            context['error'] = 'No se puede relacionar un item a si mismo'
        if abs(inicio.fase.id - fin.fase.id) > 1:
            context['error'] = 'Solo se puede relacionar items de la misma fase o fases inmediatas'
        if inicio.fase.id - fin.fase.id == 1:
            context['error'] = 'Las relaciones entre fases deben ser hacia fases posteriores'
        if len([x for x in inicio.antecesores.all() if x.id == fin.id] +
               [x for x in fin.antecesores.all() if x.id == inicio.id]) > 0:
            context['error'] = 'Esta relacion ya existe'
        # verificamos que el usuario tenga permisos de crear relaciones padre hijo
        if not has_permiso(fase=inicio.fase, usuario=request.user,
                           permiso=Rol.CREAR_RELACIONES_PH) and inicio.fase == fin.fase:
            context['error'] = 'El Rol del Usuario Actual no tiene permisos para crear Relaciones de tipo Padre-Hijo'
        # verificamos que el usuario tenga permisos de crear relaciones antecesor sucesor
        if not has_permiso(fase=inicio.fase, usuario=request.user,
                           permiso=Rol.CREAR_RELACIONES_AS) and inicio.fase != fin.fase:
            context['error'] = 'El Rol del Usuario Actual no tiene permisos para crear Relaciones de tipo ' \
                               'Antecesor-Sucesor '

        if context['error']:
            return render(request, "desarrollo/relacion_crear.html", context)
        # Si pasa todas las validaciones...
        nuevo_item_inicio = versionar_item(inicio, request.user)
        nuevo_item_fin = versionar_item(fin, request.user)
        # relacionamos las nuevas versiones
        # si son de la misma fase son padre e hijo y si son de fases diferentes son antecesor y sucesor
        if nuevo_item_inicio.fase == nuevo_item_fin.fase:
            nuevo_item_inicio.hijos.add(nuevo_item_fin)
            nuevo_item_fin.padres.add(nuevo_item_inicio)
        else:
            nuevo_item_inicio.sucesores.add(nuevo_item_fin)
            nuevo_item_fin.antecesores.add(nuevo_item_inicio)
        nuevo_item_inicio.save()
        nuevo_item_fin.save()

        # registramos para auditoría
        auditoria1 = HistoricalItem(item=nuevo_item_inicio, history_user=request.user,
                                    history_type=HistoricalItem.TIPO_RELACIONAR)
        auditoria1.save()
        auditoria2 = HistoricalItem(item=nuevo_item_fin, history_user=request.user,
                                    history_type=HistoricalItem.TIPO_RELACIONAR)
        auditoria2.save()

        return redirect('desarrollo:verProyecto', inicio.fase.proyecto.id)
    return render(request, "desarrollo/relacion_crear.html", context)


# Clase auxiliar para adecuar al algoritmo
class Relacion:
    """
    Clase auxiliar que indica una relación
    """
    inicio = Item()
    fin = Item()


def desactivar_relacion_item(request, id_proyecto):
    """
    Metodo que se encarga de renderizar la vista desactivar relacion de items,
    recibe como parametro dos atributos, el request que es comun entre todas las
    vistas y el id_proyecto que tiene el numero identificador del proyecto donde
    se encuentran las relaciones que se van a desactivar

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador unico por proyecto
    :return: objeto que renderea item_des_relacion.html
    :rtype: render
    """
    # relaciones = Relacion.objects.filter(
    #     is_active=True,
    #     inicio__fase__proyecto_id=id_proyecto,
    #     fin__fase__proyecto_id=id_proyecto,
    # )
    mensaje_error = ""

    if request.method == "POST":
        clave = request.POST['desactivar']
        clave = clave.split('-')

        # primero verificamos que cumpla con el permiso
        proy = Proyecto.objects.get(pk=id_proyecto)
        it_ini = Item.objects.get(pk=clave[0])
        if not has_permiso(fase=it_ini.fase, usuario=request.user, permiso=Rol.BORRAR_RELACIONES):
            return redirect('administracion:accesoDenegado', id_proyecto=proy.id, caso='permisos')

        relacion = Relacion()
        relacion.inicio = Item.objects.get(pk=clave[0])
        relacion.fin = Item.objects.get(pk=clave[1])
        if relacion.fin.estado == Item.ESTADO_APROBADO:
            mensaje_error = """
                El item {} esta
                aprobado, por lo cual no se puede desactivar la relacion
                """.format(relacion.fin)
        elif relacion.inicio.estado in (Item.ESTADO_LINEABASE):
            mensaje_error = """
                El item {} esta en linea base, por lo que no se puede desactivar la relacion
            """.format(relacion.inicio)
        else:

            # se añade código para que al desactivar una relación cuente como una nueva versión para ambos items
            item_inicio = Item.objects.filter(id_version=relacion.inicio.id_version).order_by('id').last()
            item_fin = Item.objects.filter(id_version=relacion.fin.id_version).order_by('id').last()

            # versionamos los ítems
            nuevo_item_inicio = versionar_item(item_inicio, request.user)
            nuevo_item_fin = versionar_item(item_fin, request.user)
            # eliminamos la relación
            if nuevo_item_inicio.fase == nuevo_item_fin.fase:
                # como el padre se versiona primero sigue apuntando a item_fin y no a nuevo_item_fin
                nuevo_item_inicio.hijos.remove(item_fin)
                nuevo_item_fin.padres.remove(nuevo_item_inicio)
            else:
                nuevo_item_inicio.sucesores.remove(item_fin)
                nuevo_item_fin.antecesores.remove(nuevo_item_inicio)
            nuevo_item_inicio.save()
            nuevo_item_fin.save()

            # registramos para auditoría
            auditoria1 = HistoricalItem(item=nuevo_item_inicio, history_user=request.user,
                                        history_type=HistoricalItem.TIPO_DESRELACIONAR)
            auditoria1.save()
            auditoria2 = HistoricalItem(item=nuevo_item_fin, history_user=request.user,
                                        history_type=HistoricalItem.TIPO_DESRELACIONAR)
            auditoria2.save()

    relaciones = crear_lista_relaciones_del_proyecto(id_proyecto)

    content = {
        'relaciones': relaciones,
        'id_proyecto': id_proyecto,
        'mensaje_error': mensaje_error,
    }
    return render(request, 'desarrollo/item_des_relacion.html', content)


def crear_lista_relaciones_del_proyecto(id_proyecto):
    """
    función auxiliar que crea una lista de todas las relaciones de un proyecto utilizando la clase auxiliar
    'relaciones'

    :param id_proyecto: identificador del proyecto
    :return: lista de objetos relacion que son las relaciones del proyecto
    """
    # codigo para ver los ítems actuales de un proyecto
    items = []
    proyecto = Proyecto.objects.get(id=id_proyecto)
    for fase in proyecto.fase_set.all():
        for item in fase.item_set.all():
            items.append(item)

    relaciones = []
    for inicio in items:
        todos = [i for i in inicio.sucesores.all()] + [i for i in inicio.hijos.all()]
        if inicio.estado != Item.ESTADO_DESACTIVADO:
            for fin in todos:
                relacion = Relacion()
                relacion.inicio = inicio.get_ultima_version()
                relacion.fin = fin.get_ultima_version()
                relaciones.append(relacion)
    return relaciones


def versionar_item(item, usuario):
    """
    función que se encarga de que al editar un item o sus relaciones se cree un nuevo objeto item que será la versión
    nueva y se encarga de que todas las relaciones, atributos particulares, etc del ítem anterior pasen al nuevo item

    :param usuario: usuario actual para registrar en caso de archivo
    :param item: es el item a versionar
    :return: None
    """
    item_editado = Item(nombre=item.nombre, complejidad=item.complejidad, descripcion=item.descripcion, fase=item.fase,
                        tipo_item=item.tipo_item, numeracion=item.numeracion, estado=item.estado,
                        version=item.version + 1, version_anterior=item, id_version=item.id_version)
    item_editado.save()

    # también nos encargamos de los atributos particulares
    lista_atr = AtributoParticular.objects.filter(item=item).order_by('id')
    for atr in lista_atr:
        nuevo_atributo = AtributoParticular(item=item_editado, nombre=atr.nombre, tipo=atr.tipo, valor=atr.valor)
        nuevo_atributo.save()

    # nos encargamos también de vincular las relaciones del ítem anterior con el actual
    for item_relacionado in item.antecesores.all():
        # primero seleccionamos la versión más actual del ítem y luego añadimos a la lista de la relación
        item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
        item_editado.antecesores.add(item_a_anadir)
    for item_relacionado in item.sucesores.all():
        item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
        item_editado.sucesores.add(item_a_anadir)
    for item_relacionado in item.padres.all():
        item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
        item_editado.padres.add(item_a_anadir)
    for item_relacionado in item.hijos.all():
        item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
        item_editado.hijos.add(item_a_anadir)

    # por ultimo desactivamos la versión anterior (mejorar esta parte)
    item.estado = Item.ESTADO_DESACTIVADO
    item.save()
    return item_editado


def solicitud_aprobacion(request, id_item):
    """
    Vista en la cual se realiza la solicitud de aprobacion de items, el mismo
    debe estar en desarrollo para pasarlo a pendiente de aprobacion
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_item: identificador del item en cuestion
    :return: redirecciona a los detalles del item
    """
    item = Item.objects.get(pk=id_item)
    if item.estado == Item.ESTADO_DESARROLLO:
        item.estado = Item.ESTADO_PENDIENTE
        item.save()

        # registramos para auditoría
        auditoria = HistoricalItem(item=item, history_user=request.user,
                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_PENDIENTE)
        auditoria.save()

    return redirect('desarrollo:verItem', item.fase.proyecto.id, id_item)


def aprobar_item(request, id_item):
    """
    Vista en la cual se aprueban los items, el mismo pasa pendiente de
    aprobacion a aprobado
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_item: identificador del item en cuestion
    :return: redirecciona al menu de aprobacion del item
    """
    item = Item.objects.get(pk=id_item)
    fase = item.fase
    proyecto = fase.proyecto
    # primero verificamos que cumpla con el permiso
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.APROBAR_ITEM):
        return redirect('administracion:accesoDenegado', id_proyecto=proyecto.id, caso='permisos')
    if item.estado == Item.ESTADO_PENDIENTE:
        item.estado = Item.ESTADO_APROBADO
        item.save()
        # registramos para auditoría
        auditoria = HistoricalItem(item=item, history_user=request.user,
                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_APROBADO)
        auditoria.save()
        send_mail_aprobacion(request, item, proyecto, True)
    return redirect('desarrollo:menuAprobacion', item.fase.proyecto_id)


def send_mail_aprobacion(request, item, proyecto, aprobar):
    """
    Funcion utilizada para mandar el mail de aprobacion o desaprobacion al solicitante
    :param request: diccionario del request
    :param item: Item que se esta aprobando
    :param proyecto: Proyecto del item
    :param aprobar: Bandera que indica si se aprobo o no
    :return:
    """
    item_auditoria = HistoricalItem.objects.filter(item=item,
                                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_PENDIENTE).order_by(
        'id').last()
    solicitante = Usuario.objects.get(username=item_auditoria.history_user)
    send_mail('Item aprobado',
              f'El usuario "{request.user.username}" {"no" if not aprobar else ""} ha aprobado su item "{item.nombre}"'
              f'en el proyecto "{proyecto.nombre}"',
              'isteampoli2020@gmail.com',
              [solicitante.email], fail_silently=True)


def desaprobar_item(request, id_item):
    """
    Vista en la cual se desaprueban los items, el mismo pasa pendiente de
    aprobacion a en desarrollo en caso de ser desaprobado
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_item: identificador del item en cuestion
    :return: redirecciona al menu de aprobacion del item
    """
    item = Item.objects.get(pk=id_item)
    fase = item.fase
    proyecto = fase.proyecto
    # primero verificamos que cumpla con el permiso
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.APROBAR_ITEM):
        return redirect('administracion:accesoDenegado', id_proyecto=proyecto.id, caso='permisos')

    if item.estado == Item.ESTADO_PENDIENTE:
        item.estado = Item.ESTADO_DESARROLLO
        item.save()

        # registramos para auditoría
        auditoria = HistoricalItem(item=item, history_user=request.user,
                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_DESARROLLO)
        auditoria.save()
        send_mail_aprobacion(request, item, proyecto, False)
    return redirect('desarrollo:menuAprobacion', item.fase.proyecto_id)


def desactivar_item(request, id_proyecto, id_item):
    """
    Vista en la cual se desactivan los items, el mismo debe estar en desarrollo para
    poder desactivarlo y una vez echo simplemente se quedan especificados en los
    detalles del item

    :param id_proyecto: identificador del proyecto
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_item: identificador del item en cuestion
    :return: redirecciona a los detalles del item
    """
    it = Item.objects.get(pk=id_item)
    fase = it.fase
    # primero verificamos que cumpla con el permiso
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.DESACTIVAR_ITEM):
        return redirect('administracion:accesoDenegado', id_proyecto=id_proyecto, caso='permisos')
    item = versionar_item(it, request.user)
    # se verifica si es antecesor o padre
    if item.sucesores.count() != 0 or item.hijos.count() != 0:
        return redirect('desarrollo:verItem', id_proyecto, id_item)

    if item.estado == Item.ESTADO_DESARROLLO:
        item.estado = Item.ESTADO_DESACTIVADO
        # desvinculamos el item y su tipo de item de la fase (solo si no hay otro item con el mismo tipo)
        fase = Fase.objects.get(pk=item.fase.id)
        # primero consultamos la cantidad de items con ese tipo de item en la fase(que no estén desactivados).
        cantidad_items = Item.objects.filter(fase=fase, estado__regex='^(?!' + Item.ESTADO_DESACTIVADO + ')',
                                             tipo_item=item.tipo_item)
        # si la cantidad es diferente a 1 si se puede desvincular el tipo de item de la fase
        if cantidad_items.count() == 1:
            fase.tipos_item.remove(item.tipo_item)

    # se deben eliminar relaciones donde el item es sucesor o hijo
    for padre in item.padres.all():
        # borramos al item de la lista en el padre
        padre.hijos.remove(padre.hijos.get(id_version=item.id_version))
        # borramos al padre de la lista en el item
        item.padres.remove(item.padres.get(id_version=padre.id_version))

    for antecesor in item.antecesores.all():
        # borramos al item de la lista en el antecesor
        item_remover = antecesor.sucesores.get(id_version=item.id_version)
        antecesor.sucesores.remove(item_remover)
        # borramos al antecesor de la lista en el item
        antecesor_remover = item.antecesores.get(id_version=antecesor.id_version)
        item.antecesores.remove(antecesor_remover)

    item.save()
    # registramos para auditoría
    auditoria = HistoricalItem(item=item, history_user=request.user,
                               history_type=HistoricalItem.TIPO_ELIMINAR)
    auditoria.save()

    return redirect('desarrollo:verItem', id_proyecto, id_item)


def modificar_item(request, id_proyecto, id_item):
    """
    Vista en la cual se modifican los Item, para hacerlo el mismo aún debe
    de estar En Desarrollo, una vez realizados vuelve a los detalles
    correspondientes al item.
    Lo que hace la vista en realidad es crear un nuevo objeto Item el cual
    tendra una referencia a la versipn anterior y heredará sus relaciones.

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_item: identificador del item
    :return: redirecciona a los detalles del item
    :return: renderea a la platilla de edición del item
    """
    item = Item.objects.get(pk=id_item)
    fase = item.fase
    # primero verificamos que cumpla con el permiso
    if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.MODIFICAR_ITEM):
        return redirect('administracion:accesoDenegado', id_proyecto=id_proyecto, caso='permisos')
    lista_atr = AtributoParticular.objects.filter(item=item).order_by('id')
    if Item.ESTADO_DESARROLLO == item.estado:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            complejidad = request.POST['complejidad']
            descripcion = request.POST['descripcion']
            # creamos un nuevo objeto item que guardará una clave a su versión anterior
            item_editado = Item(nombre=nombre, complejidad=complejidad, descripcion=descripcion, fase=item.fase,
                                tipo_item=item.tipo_item, numeracion=item.numeracion, estado=item.estado,
                                version=item.version + 1, version_anterior=item, id_version=item.id_version)
            item_editado.save()

            # también nos encargamos de los atributos particulares
            for atr in lista_atr:
                if atr.tipo == 'file':
                    valor = atr.valor
                    if request.FILES:
                        valor = handle_uploaded_file(request.FILES[atr.nombre], id_proyecto, request.user)
                else:
                    valor = request.POST[atr.nombre]
                nuevo_atributo = AtributoParticular(item=item_editado, nombre=atr.nombre, tipo=atr.tipo, valor=valor)
                nuevo_atributo.save()

            # nos encargamos también de vincular las relaciones del ítem anterior con el actual
            for item_relacionado in item.antecesores.all():
                item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
                item_editado.antecesores.add(item_a_anadir)
            for item_relacionado in item.sucesores.all():
                item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
                item_editado.sucesores.add(item_a_anadir)
            for item_relacionado in item.padres.all():
                item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
                item_editado.padres.add(item_a_anadir)
            for item_relacionado in item.hijos.all():
                item_a_anadir = Item.objects.filter(id_version=item_relacionado.id_version).order_by('id').last()
                item_editado.hijos.add(item_a_anadir)

            # por ultimo desactivamos la versión anterior (mejorar esta parte)
            item.estado = Item.ESTADO_DESACTIVADO
            item.save()

            # registramos para auditoría
            auditoria = HistoricalItem(item=item_editado, history_user=request.user,
                                       history_type=HistoricalItem.TIPO_MODIFICAR)
            auditoria.save()

            return redirect('desarrollo:verItem', id_proyecto, item_editado.id)
    return render(request, 'desarrollo/item_editar.html', {'item': item, 'lista_atr': lista_atr})


def cerrar_fase(request, id_proyecto):
    """
    Metodo que se encarga de renderizar la vista cerrar fase. Las fases se pueden
    cerrar siempre que la fase anterior fue debidamente cerrada, si los items de
    esta fase estan todos dentro de una lb y si los items de la fase estan
    relacionados con items de la fase anterior. El metodo recibe como parametro
    dos atributos, el request que es comun entre todas las vistas y el id_proyecto
    que tiene el numero identificador del proyecto donde se encuentran todas
    las fases para ese proyecto.

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador unico por proyecto
    :return: objeto que renderea item_des_relacion.html
    :rtype: render
    """
    fases = Fase.objects.filter(proyecto=id_proyecto)

    # Para mostrar el numero correcto de la fase
    for i, fase in enumerate(fases):
        fase.nro_de_fase = i + 1
        fase.cerrable = False

    # Ver cual fase se puede cerrar
    for i, fase in enumerate(fases):
        if fase.estado == 'abierta':
            if i == 0 or fases[i - 1].estado == 'cerrada':
                fases[i].cerrable = True
                break

    # Comprobacion de gerencia de proyecto
    gerente_del_proyecto = Proyecto.objects.get(pk=id_proyecto).gerente
    if gerente_del_proyecto == request.user.id:
        es_gerente = True
    else:
        es_gerente = False

    # Dict a ser enviado a la vista
    content = {
        'id_proyecto': id_proyecto,
        'fases': fases,
        'es_gerente': es_gerente,
        'mensaje_error': "",
    }

    # Si el request es POST
    if request.method == "POST":
        clave = int(request.POST['cerrar'])
        fase = Fase.objects.get(id=clave)
        if not has_permiso(fase=fase, usuario=request.user, permiso=Rol.CERRAR_FASE):
            return redirect('administracion:accesoDenegado', id_proyecto=fase.proyecto.id, caso='permisos')

        i = clave - fases[0].id
        items_de_esta_fase = fase.item_set.exclude(estado=Item.ESTADO_DESACTIVADO).all()

        # Comprobacion de que la fase anterior este cerrada
        if not fases[i].cerrable:
            content['mensaje_error'] = "La fase anterior aun no se cerro"
            return render(request, 'desarrollo/fase_cerrar.html', content)

        # Comprobacion de que todos los items esten en LB
        todos_en_lb = True
        for item in items_de_esta_fase:
            if item.estado != Item.ESTADO_LINEABASE:
                todos_en_lb = False
                break
        if not todos_en_lb:
            content['mensaje_error'] = """
            Todos los items de la fase deben estar en Linea Base para poder cerrarlo
            """

            return render(request, 'desarrollo/fase_cerrar.html', content)

        # Si hay una solicitud activa, no se permite cerrar la fase
        lineas_base = fase.lineabase_set.filter(estado=LineaBase.ESTADO_CERRADA)
        if Solicitud.objects.filter(linea_base__in=lineas_base, solicitud_activa=True).count():
            content['mensaje_error'] = """Hay solicitudes activas en la fase"""

            return render(request, 'desarrollo/fase_cerrar.html', content)
        # fase no debe estar vacía
        if items_de_esta_fase.count() == 0:
            content['mensaje_error'] = """
            No se puede cerrar fases que no contengan ningún Ítem
            """
            return render(request, 'desarrollo/fase_cerrar.html', content)
        # Comprobacion de que todos los items dentro de la fase tengan antecedentes
        # se excluye de la condicion a la fase 1
        todos_tienen_antecedentes = True
        items_sin_relacion_directa = []
        for item in items_de_esta_fase:
            if len(item.antecesores.all()) == 0:
                items_sin_relacion_directa.append(item)

        for itema in items_sin_relacion_directa:
            itema.tiene_rel_ind = False
            todos_los_ancestros_del_itema = itema.padres.all()
            for itemb in todos_los_ancestros_del_itema:
                todos_los_ancestros_del_itema.union(itemb.padres.all())
            for itemb in todos_los_ancestros_del_itema:
                if len(itemb.antecesores.all()) != 0:
                    itema.tiene_rel_ind = True
                    break
        for item in items_sin_relacion_directa:
            if not item.tiene_rel_ind:
                todos_tienen_antecedentes = False
        if i == 0:
            todos_tienen_antecedentes = True
        if not todos_tienen_antecedentes:
            content['mensaje_error'] = """
            Todos los items de la fase deben tener una relacion con la fase anterior
            """
            return render(request, 'desarrollo/fase_cerrar.html', content)

        # Si cumple los requisitos de las condiciones anteriores, cerrar las fases
        fase.estado = 'cerrada'
        fase.save()
        return redirect('desarrollo:cerrarFase', id_proyecto)
    return render(request, 'desarrollo/fase_cerrar.html', content)


def votacion_item_en_revision_desarrollo(request, id_item):
    """
    Vista que se encarga de pasar un item del  estado de Revision al estado de Desarrollo,
    si se necesita realizarle cambios.

    :param request:objeto tipo diccionario que permite acceder a datos.
    :param id_item: identificador del item.
    :return: redireccion a los detalles del item
    """
    item = Item.objects.get(pk=id_item)
    proyecto = item.fase.proyecto
    # Se pregunta si el item esta en EN REVISION
    if item.estado == Item.ESTADO_REVISION:
        item.estado = Item.ESTADO_DESARROLLO
        item.save()

        # registramos para auditoría
        auditoria = HistoricalItem(item=item, history_user=request.user,
                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_DESARROLLO)
        auditoria.save()

    def pasar_a_revision(lista_items):
        for item in lista_items:
            item_hijo = Item.objects.filter(id_version=item.id_version,
                                            estado__regex='^(?!' + Item.ESTADO_DESACTIVADO + ')').order_by('id').last()
            if item_hijo.estado == Item.ESTADO_APROBADO:
                item_hijo.estado = Item.ESTADO_REVISION
                item_hijo.save()

                # registramos para auditoría
                audit = HistoricalItem(item=item_hijo, history_user=request.user,
                                       history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_REVISION)
                audit.save()

    # Luego de pasar el item a desarrollo se debe ver como quedan sus hijos y sucesores (En estado aprobado)
    pasar_a_revision(item.hijos.all())
    pasar_a_revision(item.sucesores.all())

    def crear_solicitud(items_hijos_en_lb):
        # Luego junto todas las lb
        lbs = LineaBase.objects.filter(estado=LineaBase.ESTADO_CERRADA, fase__proyecto=proyecto)
        # Recorro todas las lb y voy cruzando la lista de items de la lb, con los items hijos
        if items_hijos_en_lb.count() == 0:
            return
        for lb in lbs:
            if lb.items.count() > 0 and len(lb.solicitud_set.filter(solicitud_activa=True)) == 0:
                items_cruce = [item for item in lb.items.all() if item in items_hijos_en_lb]
                # En items cruce tengo la lista de items que debo solicitar modificar para esa linea base
                if len(items_cruce) > 0:
                    solicitud = Solicitud(linea_base=lb, justificacion='Solicitud generada automaticamente',
                                          solicitado_por=request.user)
                    solicitud.save()
                    # Agrego los resultados del cruce a la lista de la solicitud
                    for item_para_solicitar in items_cruce:
                        solicitud.items_a_modificar.add(item_para_solicitar)

    # Luego de ver los hijos aprobados checkeamos los hijos en LB
    # Primero junto todos los items que estan en lb
    crear_solicitud(item.hijos.filter(estado=Item.ESTADO_LINEABASE))
    crear_solicitud(item.sucesores.filter(estado=Item.ESTADO_LINEABASE))

    return redirect('desarrollo:verItem', item.fase.proyecto_id, id_item)


def votacion_item_en_revision_aprobado(request, id_item):
    """
    Vista que se encarga de pasar un item del  estado de Revision al estado de Aprobado,
    si no necesita realizarle cambios.

    :param request: objeto tipo diccionario que permite acceder a datos.
    :param id_item: identificador del item.
    :return: redireccion a los detalles del item
    """
    item = Item.objects.get(pk=id_item)
    if item.estado == Item.ESTADO_REVISION:
        item.estado = Item.ESTADO_APROBADO
        item.save()

        # registramos para auditoría
        auditoria = HistoricalItem(item=item, history_user=request.user,
                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_APROBADO)
        auditoria.save()

    # TODO Muchas cosas jeje
    for linea_base in item.lineabase_set.all():
        if linea_base.estado == linea_base.ESTADO_CERRADA:
            # Si aprobe todos los items de la LB, todos pasan a estado EN LB
            if len(linea_base.items.filter(estado=Item.ESTADO_APROBADO)) == len(linea_base.items.all()):
                for item in linea_base.items.all():
                    item.estado = Item.ESTADO_LINEABASE
                    item.save()

                    # registramos para auditoría
                    auditoria = HistoricalItem(item=item, history_user=request.user,
                                               history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_LINEABASE)
                    auditoria.save()
    return redirect('desarrollo:verItem', item.fase.proyecto_id, id_item)


def votacion_item_en_revision_lineaBase(request, id_item):
    """
    Vista que se encarga de pasar un item del  estado de Revision al estado de Linea Base,
    cuando quiera pasarse a linea base directo.

    :param request: objeto tipo diccionario que permite acceder a datos.
    :param id_item: identificador del item.
    :return: redireccion a los detalles del item
    """
    item = Item.objects.get(pk=id_item)
    # Se pregunta si el item esta en EN REVISION
    if item.estado == Item.ESTADO_REVISION:
        item.estado = Item.ESTADO_LINEABASE
        item.save()

        # registramos para auditoría
        auditoria = HistoricalItem(item=item, history_user=request.user,
                                   history_type=HistoricalItem.TIPO_ESTADO + Item.ESTADO_LINEABASE)
        auditoria.save()

    return redirect('desarrollo:verItem', item.fase.proyecto_id, id_item)


# en vez de esta vista voy a integrar el calculo de impacto a la vista de ver_item
# def calculo_de_impacto(request, id_item):
#     item = Item.objects.get(pk=id_item)
#     impacto = calcular_impacto_recursivo(item)
#     # return HttpResponse('el calculo de impacto para este Item tiene valor de ' + str(impacto))
#     return render(request, 'desarrollo/item_calculo_impacto_popup.html', {'item': item, 'impacto': impacto})


def calcular_impacto_recursivo(item):
    """
    función recursiva para ir sumando la complejidad de todos los hijos y antecesores directos e indirectos de un ítem.
    Suma su complejidad con la de sus hijos y sucesores y se vuelve a llamar para cada hijo y sucesor

    :param item: el item del cual se sumará su complejidad y la de sus hijos y sucesores
    :return: returna el impacto que es la suma de complejidades
    """
    impacto = item.complejidad
    for hijo in item.hijos.all():
        # nos aseguramos de tener la versión más actual del hijo que no esté desactivada
        hijo_actual = Item.objects.filter(id_version=hijo.id_version,
                                          estado__regex='^(?!' + Item.ESTADO_DESACTIVADO + ')').order_by('id').last()
        # al impacto le sumamos el impacto que retorne la llamada recursiva con el hijo de parametro
        impacto += calcular_impacto_recursivo(hijo_actual)
    for sucesor in item.sucesores.all():
        # regex opcional : ^(((?!Desactivado).)*$)
        sucesor_actual = Item.objects.filter(id_version=sucesor.id_version,
                                             estado__regex='^(?!' + Item.ESTADO_DESACTIVADO + ')').order_by('id').last()
        impacto += calcular_impacto_recursivo(sucesor_actual)
    return impacto


def calcular_lista_items_impacto_recursivo(item):
    """
    esta función se encarga de listar todos los ítems que se suman para el cálculo de impacto

    :param item: el item del cual se sumará su complejidad y la de sus hijos y sucesores
    :return: returna el impacto que es la suma de complejidades
    """
    impacto = [item]
    for hijo in item.hijos.all():
        # al impacto le sumamos el impacto que retorne la llamada recursiva con el hijo de parametro
        impacto += calcular_lista_items_impacto_recursivo(hijo.get_ultima_version())
    for sucesor in item.sucesores.all():
        impacto += calcular_lista_items_impacto_recursivo(sucesor.get_ultima_version())
    return impacto
