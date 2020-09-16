"""
Modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .SubirArchivos import handle_uploaded_file
from desarrollo.models import Item, AtributoParticular
from administracion.models import Proyecto, TipoItem, Fase, Rol
from desarrollo.forms import ItemForm
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
                # añadimos el id de la primera versión a este campo y se pasará a las versiones posteriores
                nuevo_item.id_version = nuevo_item.id
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
        return redirect('desarrollo:verProyecto', inicio.fase.proyecto.id)
    return render(request, "desarrollo/relacion_crear.html", context)


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

    # Clase auxiliar para adecuar al algoritmo
    class Relacion:
        inicio = Item()
        fin = Item()

    if request.method == "POST":
        clave = request.POST['desactivar']
        clave = clave.split('-')
        relacion = Relacion()
        relacion.inicio = Item.objects.get(pk=clave[0])
        relacion.fin = Item.objects.get(pk=clave[1])
        if relacion.fin.estado == Item.ESTADO_APROBADO:
            mensaje_error = """
                El item {} esta
                aprobado, por lo cual no se puede desactivar la relacion
                """.format(relacion.fin)

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

    relaciones = []
    for inicio in Item.objects.all():
        todos = [i for i in inicio.sucesores.all()] + [i for i in inicio.hijos.all()]
        if inicio.estado != Item.ESTADO_DESACTIVADO:
            for fin in todos:
                relacion = Relacion()
                relacion.inicio = inicio
                relacion.fin = fin
                relaciones.append(relacion)
    content = {
        'relaciones': relaciones,
        'id_proyecto': id_proyecto,
        'mensaje_error': mensaje_error,
    }
    return render(request, 'desarrollo/item_des_relacion.html', content)


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
    it = Item.objects.get(pk=id_item)
    item = versionar_item(it, request.user)
    # se verifica si es antecesor o padre
    if item.sucesores.count() != 0 or item.hijos.count() != 0:
        return redirect('desarrollo:verItem', id_proyecto, id_item)

    if item.estado == Item.ESTADO_DESARROLLO:
        item.estado = Item.ESTADO_DESACTIVADO
        # desvinculamos el item y su tipo de item de la fase
        fase = Fase.objects.get(pk=item.fase.id)
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

        # Comprobacion de que todos los items dentro de la fase tengan antecedentes
        # se excluye de la condicion a la fase 1
        todos_tienen_antecedentes = True
        items_sin_relacion_directa=[]
        for item in items_de_esta_fase:
            if len(item.antecesores.all()) == 0:
                items_sin_relacion_directa.append(item)

        for itema in items_sin_relacion_directa:
            itema.tiene_rel_ind=False
            todos_los_ancestros_del_itema=itema.padres.all()
            for itemb in todos_los_ancestros_del_itema:
                todos_los_ancestros_del_itema.union(itemb.padres.all())
            for itemb in todos_los_ancestros_del_itema:
                if len(itemb.antecesores.all()) != 0:
                    itema.tiene_rel_ind=True
                    break
        for item in items_sin_relacion_directa:
            if not item.tiene_rel_ind:
                todos_tienen_antecedentes=False
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
