"""
Modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
from django.shortcuts import render, redirect
from .SubirArchivos import handle_uploaded_file
from desarrollo.models import Item, AtributoParticular, Relacion
from administracion.models import Proyecto, TipoItem, Fase, Rol
from desarrollo.forms import ItemForm, RelacionForm
from desarrollo.getPermisos import has_permiso


def get_numeracion(fase, tipo):
    items_del_tipo = [item for item in fase.item_set.all() if item.tipo_item == tipo]
    return len(items_del_tipo) + 1


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
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render(request, 'desarrollo/item_ver.html', {'item': item, 'lista_atributos': lista_atributos, 'fase': fase,
                                                        'proyecto': proyecto, 'desarrollo': Item.ESTADO_DESARROLLO,
                                                        'estado': Proyecto.ESTADO_EN_EJECUCION})


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
    for item_a in lista_versiones:
        relacion_inicio = Relacion.objects.filter(inicio=item_a)
        relacion_fin = Relacion.objects.filter(fin=item_a)
        item_a.relacion_inicio = relacion_inicio
        item_a.relacion_fin = relacion_fin
    return render(request, 'desarrollo/item_historial_versiones.html', {'lista_versiones': lista_versiones,
                                                                        'item_actual': item, 'proyecto': proyecto,
                                                                        'lista_atributos': lista_atributos})


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
                                                                    'lista_fases': lista_fases})


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
    lista_items = Item.objects.all()
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
    if request.method == "POST":
        form = RelacionForm(request.POST)
        if form.is_valid():
            form.save()
            proyecto = form.cleaned_data['inicio'].fase.proyecto
            return redirect('desarrollo:verProyecto', proyecto.id)
    else:
        form = RelacionForm()

    lista_items_padre = Item.objects.filter(
        fase__proyecto_id=id_proyecto, estado=Item.ESTADO_APROBADO
    )
    lista_items_hijo = Item.objects.filter(
        fase__proyecto_id=id_proyecto, estado=Item.ESTADO_DESARROLLO
    )
    # Se agrega filtro para solo relacionar items aprobados y hijos en desarrollo
    form.fields["inicio"].queryset = lista_items_padre
    form.fields["fin"].queryset = lista_items_hijo
    return render(request, "desarrollo/relacion_crear.html", {'form': form})


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
    relaciones = Relacion.objects.filter(
        is_active=True,
        inicio__fase__proyecto_id=id_proyecto,
        fin__fase__proyecto_id=id_proyecto,
    )
    mensaje_error = ""

    if request.method == "POST":

        clave = request.POST['desactivar']

        relacion = Relacion.objects.get(id=clave)
        if relacion.fin.estado == Item.ESTADO_APROBADO:
            mensaje_error = """
                El item {} esta 
                aprobado, por lo cual no se puede desactivar la relacion
                """.format(relacion.fin)

        else:
            relacion.is_active = False
            relacion.save()

    content = {
        'relaciones': relaciones,
        'id_proyecto': id_proyecto,
        'mensaje_error': mensaje_error,
    }
    return render(request, 'desarrollo/item_des_relacion.html', content)


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
    if item.estado == Item.ESTADO_PENDIENTE:
        item.estado = Item.ESTADO_APROBADO
        item.save()
    return redirect('desarrollo:menuAprobacion', item.fase.proyecto_id)


def desaprobar_item(request, id_item):
    """
    Vista en la cual se desaprueban los items, el mismo pasa pendiente de
    aprobacion a en desarrollo en caso de ser desaprobado
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_item: identificador del item en cuestion
    :return: redirecciona al menu de aprobacion del item
    """
    item = Item.objects.get(pk=id_item)
    if item.estado == Item.ESTADO_PENDIENTE:
        item.estado = Item.ESTADO_DESARROLLO
        item.save()
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
    item = Item.objects.get(pk=id_item)
    print(Relacion.objects.filter(inicio=item))
    # se verifica si es sucesor o padre
    if Relacion.objects.filter(inicio=item):
        return redirect('desarrollo:verItem', id_proyecto, id_item)

    # se deben eliminar sucesores y hijos
    for relacion_donde_es_ultimo in item.relaciones_this_as_fin.all():
        relacion_donde_es_ultimo.delete()

    if item.estado == Item.ESTADO_DESARROLLO:
        item.estado = Item.ESTADO_DESACTIVADO
        # desvinculamos el item de la fase
        fase = Fase.objects.get(pk=item.fase.id)
        fase.tipos_item.remove(item.tipo_item)

        item.save()
    return redirect('desarrollo:verItem', id_proyecto, id_item)


def modificar_item(request, id_proyecto, id_item):
    """
    Vista en la cual se modifican los Item, para hacerlo el mismo aún debe
    de estar En Desarrollo, una vez realizados vuelve a los detalles
    correspondientes al item.
    Lo que hace la vista en realidad es crear un nuevo objeto Item el cual tendra una referencia a la versipn anterior
    y heredará sus relaciones

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_item: identificador del item
    :return: redirecciona a los detalles del item
    :return: renderea a la platilla de edición del item
    """
    item = Item.objects.get(pk=id_item)
    fase = Item.fase
    lista_atr = AtributoParticular.objects.filter(item=item).order_by('id')
    if Item.ESTADO_DESARROLLO == item.estado:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            complejidad = request.POST['complejidad']
            descripcion = request.POST['descripcion']
            # creamos un nuevo objeto item que guardará una clave a su versión anterior
            item_editado = Item(nombre=nombre, complejidad=complejidad, descripcion=descripcion, fase=item.fase,
                                tipo_item=item.tipo_item, numeracion=item.numeracion, estado=item.estado,
                                version=item.version+1, version_anterior=item)
            item_editado.save()
            # también nos encargamos de los atributos particulares
            for atr in lista_atr:
                if atr.tipo == 'file' and request.FILES:
                    valor = handle_uploaded_file(request.FILES[atr.nombre], fase.proyecto.id, request.user)
                else:
                    valor = request.POST[atr.nombre]
                nuevo_atributo = AtributoParticular(item=item_editado, nombre=atr.nombre, tipo=atr.tipo, valor=valor)
                nuevo_atributo.save()
            # nos encargamos también de vincular las relaciones del ítem anterior con el actual

            # por ultimo desactivamos la versión anterior (mejorar esta parte)
            item.estado = Item.ESTADO_DESACTIVADO
            item.save()
            return redirect('desarrollo:verItem', id_proyecto, item_editado.id)
    return render(request, 'desarrollo/item_editar.html', {'item': item, 'lista_atr': lista_atr})





def cerrar_fase(request, id_proyecto):
    """
    Metodo que se encarga de renderizar la vista cerrar fase,
    recibe como parametro dos atributos, el request que es comun entre todas las
    vistas y el id_proyecto que tiene el numero identificador del proyecto donde
    se encuentran todas las fases para ese proyecto

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador unico por proyecto
    :return: objeto que renderea item_des_relacion.html
    :rtype: render
    """
    fases = Fase.objects.filter(proyecto=id_proyecto)
    mensaje_error = ""

    for i, fase in enumerate(fases):
        fase.nro_de_fase = i + 1
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

    if request.method == "POST":

        clave = int(request.POST['cerrar'])
        fase = Fase.objects.get(id=clave)
        i = clave - fases[0].id
        if fases[i].cerrable:
            fase.estado = 'cerrada'
            fase.save()
        else:
            mensaje_error = "La fase anterior aun no se cerro"
        return redirect('desarrollo:cerrarFase', id_proyecto)
    content = {
        'id_proyecto': id_proyecto,
        'fases': fases,
        'es_gerente': es_gerente,
        'mensaje_error': mensaje_error,
    }
    return render(request, 'desarrollo/fase_cerrar.html', content)
