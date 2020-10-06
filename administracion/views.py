"""
Modulo se detalla la logica para las vistas que serán utilizadas por la app
"""
# Django
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
# Models
from administracion.models import TipoItem, Proyecto, PlantillaAtributo, Rol, Fase, UsuarioxRol
from login.models import Usuario
# Forms
from administracion.forms import ProyectoForm, RolForm, EditarTipoItemForm
# Python
import datetime


def acceso_denegado(request, id_proyecto, caso):
    """
    vista que se encarga de desplegar la página de acceso denegado si es que se intenta ingresar
    a un url no permitido.

    :param caso: El caso es la clave para seleccionar el mensaje adecuado a desplegar
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador unico del proyecto
    :return: objeto que se encarga de renderear accesoDenegado.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    posibles_casos = {
        'estado': 'No se permite el ingreso a esta URL porque el proyecto: ' + proyecto.nombre + '  '
                                                                                                 'tiene estado actual: ' + proyecto.estado,
        'gerente': 'El usuario actual no puede acceder a esta URL porque no es el Gerente del Proyecto actual',
        'tiimportado': 'No se puede editar este tipo de ítem porque se utiliza en otros proyectos',
        'tiponovalido': 'El tipo seleccionado no es válido para esta fase',
        'permisos': 'El Rol del usuario actual no cuenta con los permisos necesarios para realizar esta acción'
    }
    mensaje = posibles_casos.get(caso)

    return render(request, 'administracion/accesoDenegado.html', {'proyecto': proyecto, 'mensaje': mensaje})


def proyectos(request, filtro):
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

    return render(request, 'administracion/proyectos.html', {'lista_proyectos': lista_proyectos, 'filtro': filtro})


def crear_proyecto(request):
    """
    esta vista se encarga de la creación del proyecto, primeramente verifica si el metodo del request es POST, de no
    ser retorna un form vacío y de ser pasa el request como parametro al form y el form retorna como 'cleaned_data'
    los datos para crear el proyecto. Para el gerente se guarda el id del usuario que realiza el request y luego se
    guarda al gerente como el primer usuario participante del proyecto. Además se crean la cantidad de fases que
    indica el atributo del proyecto: 'numero_fases', estas fases se crean con datos provisionales que luego pueden
    ser modificados por el usuario. Finalmente, luego de ser creado el proyecto la vista redirecciona a la otra vista
    ver_proyecto.

    :param request: objeto tipo diccionario que permite acceder a datos
    :return: objeto que se encarga de renderear a crearProyecto.html o en caso de POST redireccion a verProyecto.html
    :rtype: render, redirect
    """
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            # primero registramos los atributos en el proyecto
            nombre = form.cleaned_data['nombre']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            numero_fases = form.cleaned_data['numero_fases']
            cant_comite = form.cleaned_data['cant_comite']
            # establecemos al usuario que crea el proyecto como gerente
            gerente = request.user.id
            nuevo_proyecto = Proyecto(nombre=nombre, fecha_inicio=fecha_inicio, numero_fases=numero_fases,
                                      cant_comite=cant_comite, gerente=gerente)
            nuevo_proyecto.save()
            # ponemos al gerente como participante en el proyecto
            participante = Usuario.objects.get(pk=gerente)
            nuevo_proyecto.participantes.add(participante)
            # creamos la cantidad de fases para este proyecto
            for x in range(0, nuevo_proyecto.numero_fases):
                nueva_fase = Fase(nombre='', descripcion='', proyecto=nuevo_proyecto)
                nueva_fase.save()
            return HttpResponseRedirect(reverse('administracion:verProyecto', args=[nuevo_proyecto.id]))
    else:
        form = ProyectoForm()
    return render(request, 'administracion/crearProyecto.html', {'form': form})


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
    gerente = Usuario.objects.get(pk=proyecto.gerente)
    tipo_item = proyecto.tipoitem_set.all()
    fases = proyecto.fase_set.all().order_by('id')
    estados_posibles = {
        'iniciado': 'Iniciado',
        'en ejecucion': 'En Ejecución',
        'finalizado': 'Finalizado',
        'cancelado': 'Cancelado',
    }
    estado = estados_posibles.get(proyecto.estado)
    habilitadofase = True
    habilitadocomite = True
    habilitadotipo = True
    lista_fases = proyecto.fase_set.all()
    for fase in lista_fases:
        if fase.nombre == '':
            habilitadofase = False

    if proyecto.comite.count() != proyecto.cant_comite:
        habilitadocomite = False

    if proyecto.tipoitem_set.all().count() < proyecto.numero_fases:
        habilitadotipo = False
    return render(request, 'administracion/verProyecto.html',
                  {'proyecto': proyecto, 'gerente': gerente, 'tipo_item': tipo_item, 'fases': fases, 'estado': estado,
                   'habilitadofase': habilitadofase, 'habilitadocomite': habilitadocomite,
                   'habilitadotipo': habilitadotipo})


def administrar_participantes(request, id_proyecto):
    """
    Esta vista permite añadir y sacar participantes del proyecto, además también acceder a los roles de un
    participante

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identidficar del proyecto sobre el cual se quiere administrar sus participantes
    :return: objeto que renderea administrarParticipantes.html y en caso de post que redirecciona
    :rtype: render, redirect
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        lista_usuarios = Usuario.objects.all()
        if request.method == 'POST':
            id_usuario = request.POST['participante']
            participante = Usuario.objects.get(pk=id_usuario)
            proyecto.participantes.add(participante)
            return HttpResponseRedirect(reverse('administracion:administrarParticipantes', args=[proyecto.id]))
        return render(request, 'administracion/administrarParticipantes.html', {'proyecto': proyecto,
                                                                                'lista_usuarios': lista_usuarios})


def editar_proyecto(request, id_proyecto):
    """
    Vista que permite editar los datos del proyecto seleccionado

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: proyecto seleccionado para ser modificado
    :return: objeto que se encarga de renderear editarProyecto.html
    :rtype: render
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        if request.method == 'POST':
            nombre = request.POST['nombre']
            fecha_inicio = request.POST['fecha_inicio']
            proyecto.nombre = nombre
            proyecto.fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            proyecto.save()
            return render(request, 'administracion/editarProyecto.html', {'proyecto': proyecto})

        return render(request, 'administracion/editarProyecto.html', {'proyecto': proyecto})


def estado_proyecto(request, id_proyecto):
    """
    vista que permite seleccionar y cambiar el estado de un proyecto. Bloquea el paso a estado de ejecución si las
    fases no están definidas o el comité no está completo

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: id del proyecto el cual se desea administrar su estado
    :return: objeto que renderea estadoProyecto.html o redireccion al mismo html
    :rtype: render, redirect
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        habilitadofase = True
        habilitadocomite = True
        estados_posibles = {
            'iniciado': 'Iniciado',
            'en ejecucion': 'En Ejecución',
            'finalizado': 'Finalizado',
            'cancelado': 'Cancelado',
        }
        estado = estados_posibles.get(proyecto.estado)

        lista_fases = proyecto.fase_set.all()
        for fase in lista_fases:
            if fase.nombre == '':
                habilitadofase = False

        if proyecto.comite.count() != proyecto.cant_comite:
            habilitadocomite = False

        if request.method == 'POST':
            estado = request.POST['estado']
            proyecto.estado = estado
            proyecto.save()
            return HttpResponseRedirect(reverse('administracion:estadoProyecto', args=[id_proyecto]))

    return render(request, 'administracion/estadoProyecto.html',
                  {'proyecto': proyecto, 'habilitadofase': habilitadofase, 'habilitadocomite': habilitadocomite,
                   'estado': estado})


def estado_proyectov2(request, id_proyecto, estado):
    """
    vista que permite seleccionar y cambiar el estado de un proyecto. Bloquea el paso a estado de ejecución si las
    fases no están definidas o el comité no está completo

    :param estado: estado nuevo a asignar
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: id del proyecto el cual se desea administrar su estado
    :return: objeto que renderea estadoProyecto.html o redireccion al mismo html
    :rtype: render, redirect
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        if estado == 'iniciado' or estado == 'en ejecucion' or estado == 'finalizado' or estado == 'cancelado':
            if not (estado == 'finalizado' and proyecto.estado != 'en ejecucion'):
                # se modifica el estado
                proyecto.estado = estado
                # se añade la fecha de modificación
                if estado == 'en ejecucion':
                    proyecto.fecha_ejecucion = timezone.now()
                elif estado == 'finalizado':
                    proyecto.fecha_finalizado = timezone.now()
                elif estado == 'cancelado':
                    proyecto.fecha_cancelado = timezone.now()
                # se guardan cambios en la base de datos
                proyecto.save()
                return HttpResponseRedirect(reverse('administracion:verProyecto', args=[id_proyecto]))

    return redirect('administracion:verProyecto', id_proyecto=id_proyecto)


def administrar_fases_del_proyecto(request, id_proyecto):
    """
    vista que permite modificar los nombres y las descripciones de las fases del proyecto

    :param request: objeto de tipo diccionario que permite acceder a datos
    :param id_proyecto: id del proyecto cuyas fases se quieren editar
    :return: objeto que renderea administrarFasesProyecto.html o redireccion a verProyecto.html
    :rtype: render, redirect
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        fases = proyecto.fase_set.all().order_by('id')
        if request.method == 'POST':
            ids = request.POST
            for id_fase, valor in ids.items():
                if id_fase != 'csrfmiddlewaretoken':
                    if id_fase.isnumeric() or id_fase.split('d')[1].isnumeric():
                        # si encuentra una d antes es una descripcion
                        if id_fase.find('d') == 0:
                            fase = Fase.objects.get(pk=id_fase.split('d')[1])
                            fase.descripcion = valor
                        else:
                            fase = Fase.objects.get(pk=id_fase)
                            fase.nombre = valor
                        fase.save()
            return HttpResponseRedirect(reverse('administracion:verProyecto', args=[proyecto.id]))

    return render(request, 'administracion/administrarFasesProyecto.html', {'proyecto': proyecto, 'fases': fases})


def administrar_comite(request, id_proyecto):
    """
    vista que permite administrar que participantes del proyecto formaran parte del comité de decisión

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: id del proyecto del cual se quiere administrar su comité
    :return: objeto que renderea administrarComite.html o redireción
    :rtype: render, redirect
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        if request.method == 'POST':
            id_usuario = request.POST['miembro_comite']
            miembro_comite = Usuario.objects.get(pk=id_usuario)
            proyecto.comite.add(miembro_comite)
            return HttpResponseRedirect(reverse('administracion:administrarComite', args=[proyecto.id]))
        return render(request, 'administracion/administrarComite.html', {'proyecto': proyecto})


def eliminar_participante_y_comite(request, id_proyecto, id_usuario, caso):
    """
    Vista que permite sacar a un usuario ya sea del proyecto completo o del comité de decisión del proyecto.

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: id del proyecto seleccionado
    :param id_usuario: id del usuario que saldrá del comité o del proyecto
    :param caso: toma los valores 'comite' y 'participante' indica si se desea sacar al usuario del comité o del proyecto completo
    :return: redireccion a administrarComite.html o administrarParticipantes.html dependiendo del caso
    :rtype: redirect
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    usuario = Usuario.objects.get(pk=id_usuario)
    if caso == 'comite':
        proyecto.comite.remove(usuario)
        return HttpResponseRedirect(reverse('administracion:administrarComite', args=[proyecto.id]))
    elif caso == 'participante':
        if proyecto.gerente != usuario.id:
            proyecto.participantes.remove(usuario)
            proyecto.comite.remove(usuario)
        return HttpResponseRedirect(reverse('administracion:administrarParticipantes', args=[proyecto.id]))


def mostrar_tipo_item(request):
    tipo_items = TipoItem.objects.all()
    return render(request, 'administracion/tipoItemTest.html', {'lista_tipoitem': tipo_items})


def mostrar_tipo_import(request, id_proyecto):
    """
    Vista que en la cual se muestra los tipos de item del proyecto

    :return: redirecciona al url imṕortarTipoItem.html
    """

    tipo_item_proyecto_actual = Proyecto.objects.get(pk=id_proyecto).tipoitem_set.all()
    tipo_items = [tipo for tipo in TipoItem.objects.all() if not (tipo in tipo_item_proyecto_actual)]
    return render(request, 'administracion/importarTipoItem.html',
                  {'lista_tipoitem': tipo_items, 'id_proyecto': id_proyecto})


def importar_tipo(request, id_proyecto, id_tipo):
    """
    Vista que permite traer de otro proyecto su tipo de item con sus
    respectivos atributos

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: Identificador del proyecto
    :param id_tipo: identificador del tipo de item
    :return: redireccion a los permisos de acceso, en este caso si el proyecto es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino a verProyecto.
    """
    tipo_item = TipoItem.objects.get(pk=id_tipo)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    tipo_item.proyecto.add(proyecto)
    return redirect('administracion:tipoItemPorProyecto', id_proyecto=id_proyecto)


def crear_tipo(request, id_proyecto):
    """
    Vista en la cual se crean los tipos de item de los proyectos

    :param request:  objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :return: redirecciona a los permisos de acceso si el proyecto  es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino redirecciona a crearTipoItem.html mediante el id_proyecto.
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        return render(request, 'administracion/crearTipoItem.html', {'id_proyecto': id_proyecto})


def editar_tipo(request, id_proyecto, id_tipo):
    """
    Vista en la cual se editan los tipos de item

    :param id_tipo: id del tipo de ítem a editar
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :return: redirecciona a los permisos de acceso si el tipo de item es usado en mas de un proyecto o si el proyecto ya inicio
     """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    tipo = TipoItem.objects.get(pk=id_tipo)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        if tipo.proyecto.all().count() > 1:
            return redirect('administracion:accesoDenegado', id_proyecto=id_proyecto, caso='tiimportado')
        if request.method == 'POST':
            form = EditarTipoItemForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                prefijo = form.cleaned_data['prefijo']
                descripcion = form.cleaned_data['descripcion']
                tipo.nombre = nombre
                tipo.prefijo = prefijo
                tipo.descripcion = descripcion
                tipo.save()
                return redirect('administracion:tipoItemPorProyecto', id_proyecto=id_proyecto)
        form = EditarTipoItemForm()
        form.fields['nombre'].widget.attrs['value'] = tipo.nombre
        form.fields['prefijo'].widget.attrs['value'] = tipo.prefijo
        form.fields['descripcion'].initial = tipo.descripcion
        return render(request, 'administracion/editarTipoItem.html', {'form': form, 'tipo': tipo})


def ver_tipo(request, id_proyecto, id_tipo):
    """
    Vista en la cual se ve los tipos de items del proyecto

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_tipo: identificador del tipo de item
    :return: redirecciona a los permisos de acceso si el proyecto  es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino redirecciona al url verTipoItem.html
    """
    obj_proyecto = Proyecto.objects.get(pk=id_proyecto)
    obj_tipo_item = TipoItem.objects.get(pk=id_tipo)
    return render(request, 'administracion/verTipoItem.html',
                  {'proyecto': obj_proyecto, 'tipo_item': obj_tipo_item})


def desactivar_tipo_item(request, id_proyecto, id_tipo):
    """
    Vista que desactiva los tipos de item del proyecto recibido, solo lo hace si el proyecto aun no esta iniciado
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_tipo: identificador del tipo de item
    :return: redirecciona a la vista de administracion del tipo de item
    """

    tipo_item = TipoItem.objects.get(pk=id_tipo)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.estado == 'iniciado':
        tipo_item.proyecto.remove(proyecto)
    return redirect('administracion:tipoItemPorProyecto', id_proyecto=id_proyecto)


def confirmar_tipo_import(request, id_proyecto, id_tipo):
    """
    Vista en la cual se confirma el tipo de item a utilizar

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_tipo: identificador del tipo de item
    :return: redirecciona a los permisos de acceso si el proyecto  es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino redirecciona al url verTipoItemParaImport.html para ver que tipos de items importar.
    """
    obj_proyecto = Proyecto.objects.get(pk=id_proyecto)
    if obj_proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        obj_tipo_item = TipoItem.objects.get(pk=id_tipo)
        return render(request, 'administracion/verTipoItemParaImport.html',
                      {'proyecto': obj_proyecto, 'tipo_item': obj_tipo_item})


def ver_tipo_por_proyecto(request, id_proyecto):
    """
    Vista que permite ver el tipo de item por proyectos

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :return: redirecciona a los permisos de acceso si el proyecto  es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino redirecciona al url tipoItemTest.html
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        tipo_item = proyecto.tipoitem_set.all()
        return render(request, 'administracion/administrarTipoItem.html', {
            'lista_tipoitem': tipo_item,
            'proyecto': proyecto
        })


def registrar_tipoitem_en_base(request, id_proyecto):
    """
    Vista en la cual se registran los tipos de item a utilizar en el proyecto

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :return: redirecciona a los permisos de acceso si el proyecto  es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino redirecciona a verTipoItem.
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        prefijo = request.POST['prefijo']
        nuevo_tipo_item = TipoItem(nombre=nombre, descripcion=descripcion, prefijo=prefijo)
        nuevo_tipo_item.save()
        nuevo_tipo_item.proyecto.add(proyecto)
        return HttpResponseRedirect(reverse('administracion:verTipoItem', args=(id_proyecto, nuevo_tipo_item.id)))


def crear_atributo(request, id_proyecto, id_tipo):
    """
    Vista en la cual se permite crear los atributos de los tipos de item del proyecto

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_tipo: identificador del tipo de item
    :return: redireccion a verTipoItem
    """
    nombre = request.POST['nombre']
    tipo = request.POST['tipo']
    is_required = True if request.POST.get('required') else False
    tipo_item = TipoItem.objects.get(pk=id_tipo)
    atributo = PlantillaAtributo(nombre=nombre, tipo=tipo, tipo_item=tipo_item, es_requerido=is_required)
    atributo.save()
    return HttpResponseRedirect(reverse('administracion:verTipoItem', args=(id_proyecto, tipo_item.id)))


def quitar_atributo(request, id_proyecto, id_tipo, id_atributo):
    """
    Vista que permite quitar los atributos de los tipos de item

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_tipo: identificador del tipo de item
    :param id_atributo: identificador del atributo
    :return: redirecciona a verTipoItem
    """
    atributo = PlantillaAtributo.objects.get(pk=id_atributo)
    atributo.delete()
    return HttpResponseRedirect(reverse('administracion:verTipoItem', args=(id_proyecto, id_tipo)))


def crear_rol(request, id_proyecto):
    """
    Vista en la cual se crean los roles del proyecto

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :return: redirecciona a los permisos de acceso si el proyecto  es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino redirecciona primeramente a verProyecto si el metodo corresponde a 'POST' y luego va al formulario correspondiente al rol y si es valido crean los roles con sus respectivos permisos y atributos, y retorna al verProyecto, luego va de al formulario para crear el nuevo rol y por ultmo redirecciona a crearRol.html
    """

    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        if request.method == 'POST':
            form = RolForm(request.POST)
            if form.is_valid():
                nombre = form.cleaned_data['nombre']
                crear_item = form.cleaned_data['crear_item']
                modificar_item = form.cleaned_data['modificar_item']
                desactivar_item = form.cleaned_data['desactivar_item']
                aprobar_item = form.cleaned_data['aprobar_item']
                reversionar_item = form.cleaned_data['reversionar_item']
                crear_relaciones_ph = form.cleaned_data['crear_relaciones_ph']
                crear_relaciones_as = form.cleaned_data['crear_relaciones_as']
                borrar_relaciones = form.cleaned_data['borrar_relaciones']
                ver_item = form.cleaned_data['ver_item']
                crear_linea_base = form.cleaned_data['crear_linea_base']
                cerrar_fase = form.cleaned_data['cerrar_fase']
                cerrar_proyecto = form.cleaned_data['cerrar_proyecto']
                ver_el_proyecto = form.cleaned_data['ver_proyecto']
                solicitar_ruptura_lb = form.cleaned_data['solicitar_ruptura_lb']
                nuevo_rol = Rol(nombre=nombre, crear_item=crear_item, modificar_item=modificar_item,
                                desactivar_item=desactivar_item,
                                aprobar_item=aprobar_item, reversionar_item=reversionar_item,
                                crear_relaciones_as=crear_relaciones_as, crear_relaciones_ph=crear_relaciones_ph,
                                borrar_relaciones=borrar_relaciones, proyecto=proyecto, ver_item=ver_item,
                                crear_linea_base=crear_linea_base, cerrar_fase=cerrar_fase,
                                cerrar_proyecto=cerrar_proyecto, ver_el_proyecto=ver_el_proyecto,
                                solicitar_ruptura_lb=solicitar_ruptura_lb)
                nuevo_rol.save()
                return redirect('administracion:administrarRoles', id_proyecto=id_proyecto)
        form = RolForm()
        return render(request, 'administracion/crearRol.html', {'form': form})


def administrar_roles(request, id_proyecto):
    """
    Vista que muestra los datos y acciones relacionadas a los roles
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto:  identificador del proyecto
    :return: render de la vista de administracion de roles
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        return render(request, 'administracion/administrarRoles.html', {'proyecto': proyecto})


def desactivar_rol_proyecto(request, id_proyecto, id_rol):
    """
    Vista que desactiva loroels del proyecto recibido, solo lo hace si el proyecto aun no esta iniciado y
    si no tiene usuarios con ese rol
    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_rol: identificador del rol
    :return: redirecciona a la vista de administracion de roles
    """

    rol = Rol.objects.get(pk=id_rol)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.estado == 'iniciado' and rol.usuarioxrol_set.all().count() == 0:
        rol.activo = False
        rol.save()

    return redirect('administracion:administrarRoles', id_proyecto=id_proyecto)


def ver_roles_usuario(request, id_proyecto, id_usuario):
    """
    Vista en donde se ven los roles del usuario

    :param request:  objeto tipo diccionario que permite acceder a datos
    :param id_proyecto: identificador del proyecto
    :param id_usuario: identificador del usuario
    :return: redirecciona redirecciona a los permisos de acceso si el proyecto  es cancelado, finalizado o en ejecucion, deriva a un acceso denegado sino redirecciona a verDetallesRol.html en donde se ven los detalles de cada, con los proyectos, participantes y los roles que les corresponden.
    """
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if proyecto.gerente != request.user.id:
        return HttpResponseRedirect(reverse('administracion:accesoDenegado', args=[id_proyecto, 'gerente']))
    else:
        participante = Usuario.objects.get(pk=id_usuario)
        lista_roles = [UsuarioxRol.objects.filter(fase=fase, usuario=participante, activo=True) for fase
                       in proyecto.fase_set.all().order_by('id')]
        union_listas = zip(proyecto.fase_set.all().order_by('id'), lista_roles)
        return render(request, 'administracion/verDetallesRol.html', {
            'proyecto': proyecto,
            'participante': participante,
            'listaRol': union_listas
        })


def asignar_rol_por_fase(request, id_fase, id_usuario):
    """
    Vista que permite asignar roles por fase a un participante del proyecto

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_fase: identificador de fase
    :param id_usuario: identificador del participante
    :return: redeirecciona al url asignarRol.html en los cuales se muestran el participante al cual asignar en cierta fase con la lista de roles disponibles en sistema.
    """
    participante = Usuario.objects.get(pk=id_usuario)
    fase = Fase.objects.get(pk=id_fase)
    lista_usr_x_rol = UsuarioxRol.objects.filter(usuario=participante, fase=fase, activo=True)
    roles_fase_actual = [obj.rol for obj in lista_usr_x_rol]
    roles_proyecto = Rol.objects.filter(proyecto=fase.proyecto)
    roles_disponibles = [rol for rol in roles_proyecto if not (rol in roles_fase_actual)]
    return render(request, 'administracion/asignarRol.html', {
        'participante': participante,
        'fase': fase,
        'roles_disponibles': roles_disponibles
    })


def registrar_rol_por_fase(request, id_fase, id_usuario, id_rol):
    """
    Vista en la cual se registran los roles de cada fase

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_fase: identificador de la fase
    :param id_usuario: identificador del participante
    :param id_rol: identificador del rol de la fase
    :return: redirecciona a verRolesUsuario en donde se vera que el rol ha sido asignado correctamente.
    """
    fase = Fase.objects.get(pk=id_fase)
    rol = Rol.objects.get(pk=id_rol)
    usuario = Usuario.objects.get(pk=id_usuario)
    rol_asignado = UsuarioxRol.objects.filter(fase=fase, rol=rol, usuario=usuario)
    if rol_asignado:
        rol_asignado = UsuarioxRol.objects.get(fase=fase, rol=rol, usuario=usuario)
        rol_asignado.activo = True
    else:
        rol_asignado = UsuarioxRol(fase=fase, rol=rol, usuario=usuario)
    rol_asignado.save()
    return HttpResponseRedirect(reverse('administracion:verRolesUsuario', args=(fase.proyecto.id, id_usuario)))


def desasignar_rol_al_usuario(request, id_fase, id_usuario, id_rol):
    """
    Vista en donde se desasignan roles al usuario.

    :param request: objeto tipo diccionario que permite acceder a datos
    :param id_fase: identificador de la fase
    :param id_usuario: identificador del participante
    :param id_rol: identificador del rol
    :return: redirecciona a verRolesUsuario en donde se visualiza que el rol fue desasignado al usuario.'
    """
    fase = Fase.objects.get(pk=id_fase)
    usuario = Usuario.objects.get(pk=id_usuario)
    rol = Rol.objects.get(pk=id_rol)
    rol_actual = UsuarioxRol.objects.get(fase=fase, usuario=usuario, rol=rol)
    rol_actual.activo = False
    rol_actual.save()
    return HttpResponseRedirect(reverse('administracion:verRolesUsuario', args=(fase.proyecto.id, id_usuario)))
