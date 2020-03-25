from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import TipoItem, Proyecto, PlantillaAtributo, Rol, Fase, UsuarioxRol
from administracion.forms import ProyectoForm, ParticipanteForm, RolForm
from login.models import Usuario
import datetime


def index_administracion(request):
    return render(request, 'administracion/indexAdmin.html')


def proyectos(request, filtro):
    lista_proyectos = []
    lista_todos_proyectos = Proyecto.objects.all()
    if filtro == 'todos':
        lista_proyectos = lista_todos_proyectos
    else:
        for proyecto in lista_todos_proyectos:
            if proyecto.estado == filtro:
                lista_proyectos.append(proyecto)
    return render(request, 'administracion/proyectos.html', {'lista_proyectos': lista_proyectos, 'filtro':filtro})


def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            # primero registramos los atributos en el proyecto
            nombre = form.cleaned_data['nombre']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            numero_fases = form.cleaned_data['numero_fases']
            cant_comite = form.cleaned_data['cant_comite']
            # establecemos al usuario que crea el proyecto como gerente
            gerente = request.user.localId
            nuevo_proyecto = Proyecto(nombre=nombre, fecha_inicio=fecha_inicio, numero_fases=numero_fases,
                                      cant_comite=cant_comite, gerente=gerente)
            nuevo_proyecto.save()
            # ponemos al gerente como participante en el proyecto
            participante = Usuario.objects.get(localId=gerente)
            nuevo_proyecto.participantes.add(participante)
            # creamos la cantidad de fases para este proyecto
            for x in range(0, nuevo_proyecto.numero_fases):
                nueva_fase = Fase(nombre=f'Nombre Indefinido {x+1}', descripcion='añadir descripción...',
                                  proyecto=nuevo_proyecto)
                nueva_fase.save()
            return HttpResponseRedirect(reverse('administracion:verProyecto', args=[nuevo_proyecto.id]))
    else:
        form = ProyectoForm()
    return render(request, 'administracion/crearProyecto.html', {'form': form})


def ver_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    gerente = Usuario.objects.get(localId=proyecto.gerente)
    tipo_item = proyecto.tipoitem_set.all()
    fases = proyecto.fase_set.all().order_by('id')
    return render(request, 'administracion/verProyecto.html',
                  {'proyecto': proyecto, 'gerente': gerente, 'tipo_item': tipo_item, 'fases': fases})


def administrar_participantes(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST, proyecto)
        if form.is_valid():
            id_usuario = request.POST['participantes']
            participante = Usuario.objects.get(localId=id_usuario)
            proyecto.participantes.add(participante)
            return HttpResponseRedirect(reverse('administracion:administrarParticipantes', args=[proyecto.id]))
    else:
        form = ParticipanteForm()
    return render(request, 'administracion/administrarParticipantes.html', {'proyecto': proyecto, 'form': form})


def editar_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        nombre = request.POST['nombre']
        fecha_inicio = request.POST['fecha_inicio']
        proyecto.nombre = nombre
        proyecto.fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
        proyecto.save()
        return render(request, 'administracion/editarProyecto.html', {'proyecto': proyecto})

    return render(request, 'administracion/editarProyecto.html', {'proyecto': proyecto})


def estado_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    habilitado = True
    lista_fases = proyecto.fase_set.all()
    for fase in lista_fases:
        if fase.nombre.find('Nombre Indefinido') != -1:
            habilitado = False
    if request.method == 'POST':
        estado = request.POST['estado']
        proyecto.estado = estado
        proyecto.save()
        return HttpResponseRedirect(reverse('administracion:estadoProyecto', args=[id_proyecto]))

    return render(request, 'administracion/estadoProyecto.html', {'proyecto': proyecto, 'habilitado': habilitado})


def administrar_fases_del_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
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
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        id_usuario = request.POST['miembro_comite']
        miembro_comite = Usuario.objects.get(localId=id_usuario)
        proyecto.comite.add(miembro_comite)
        return HttpResponseRedirect(reverse('administracion:administrarComite', args=[proyecto.id]))
    return render(request, 'administracion/administrarComite.html', {'proyecto': proyecto})


def eliminar_participante_y_comite(request, id_proyecto, id_usuario, caso):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    usuario = Usuario.objects.get(pk=id_usuario)
    if caso == 'comite':
        proyecto.comite.remove(usuario)
        return HttpResponseRedirect(reverse('administracion:administrarComite', args=[proyecto.id]))
    elif caso == 'participante':
        proyecto.participantes.remove(usuario)
        proyecto.comite.remove(usuario)
        return HttpResponseRedirect(reverse('administracion:administrarParticipantes', args=[proyecto.id]))


def mostrar_tipo_item(request):
    tipo_items = TipoItem.objects.all()
    return render(request, 'administracion/tipoItemTest.html', {'lista_tipoitem': tipo_items})


def mostrar_tipo_import(request, id_proyecto):
    tipo_item_proyecto_actual = Proyecto.objects.get(pk=id_proyecto).tipoitem_set.all()
    tipo_items = [tipo for tipo in TipoItem.objects.all() if not (tipo in tipo_item_proyecto_actual)]
    return render(request, 'administracion/importarTipoItem.html',
                  {'lista_tipoitem': tipo_items, 'id_proyecto': id_proyecto})


def importar_tipo(request, id_proyecto, id_tipo):
    tipo_item = TipoItem.objects.get(pk=id_tipo)
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    tipo_item.proyecto.add(proyecto)
    return HttpResponseRedirect(reverse('administracion:verProyecto', args=(id_proyecto,)))


def crear_tipo(request, id_proyecto):
    return render(request, 'administracion/crearTipoItem.html', {'id_proyecto': id_proyecto})


def ver_tipo(request, id_proyecto, id_tipo):
    obj_proyecto = Proyecto.objects.get(pk=id_proyecto)
    obj_tipo_item = TipoItem.objects.get(pk=id_tipo)
    return render(request, 'administracion/verTipoItem.html', {'proyecto': obj_proyecto, 'tipo_item': obj_tipo_item})


def confirmar_tipo_import(request, id_proyecto, id_tipo):
    obj_proyecto = Proyecto.objects.get(pk=id_proyecto)
    obj_tipo_item = TipoItem.objects.get(pk=id_tipo)
    return render(request, 'administracion/verTipoItemParaImport.html',
                  {'proyecto': obj_proyecto, 'tipo_item': obj_tipo_item})


def ver_tipo_por_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    tipo_item = proyecto.tipoitem_set.all()
    return render(request, 'administracion/tipoItemTest.html', {'lista_tipoitem': tipo_item})


def registrar_tipoitem_en_base(request, id_proyecto):
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    prefijo = request.POST['prefijo']
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    nuevo_tipo_item = TipoItem(nombre=nombre, descripcion=descripcion, prefijo=prefijo)
    nuevo_tipo_item.save()
    nuevo_tipo_item.proyecto.add(proyecto)
    return HttpResponseRedirect(reverse('administracion:verTipoItem', args=(id_proyecto, nuevo_tipo_item.id)))


def crear_atributo(request, id_proyecto, id_tipo):
    nombre = request.POST['nombre']
    tipo = request.POST['tipo']
    tipo_item = TipoItem.objects.get(pk=id_tipo)
    atributo = PlantillaAtributo(nombre=nombre, tipo=tipo, tipo_item=tipo_item)
    atributo.save()
    return HttpResponseRedirect(reverse('administracion:verTipoItem', args=(id_proyecto, tipo_item.id)))


def quitar_atributo(request, id_proyecto, id_tipo, id_atributo):
    atributo = PlantillaAtributo.objects.get(pk=id_atributo)
    atributo.delete()
    return HttpResponseRedirect(reverse('administracion:verTipoItem', args=(id_proyecto, id_tipo)))


def crear_rol(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
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
            nuevo_rol = Rol(nombre=nombre, crear_item=crear_item, modificar_item=modificar_item, desactivar_item=desactivar_item,
                            aprobar_item=aprobar_item, reversionar_item=reversionar_item,
                            crear_relaciones_as=crear_relaciones_as, crear_relaciones_ph=crear_relaciones_ph,
                            borrar_relaciones=borrar_relaciones, proyecto=proyecto)
            nuevo_rol.save()
            return HttpResponseRedirect(reverse('administracion:verProyecto', args=(id_proyecto,)))
    form = RolForm()
    return render(request, 'administracion/crearRol.html', {'form': form})


def ver_roles_usuario(request, id_proyecto, id_usuario):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    participante = Usuario.objects.get(pk=id_usuario)
    lista_roles = [UsuarioxRol.objects.filter(fase=fase, usuario=participante, activo=True) for fase in proyecto.fase_set.all().order_by('id')]
    union_listas = zip(proyecto.fase_set.all().order_by('id'), lista_roles)
    return render(request, 'administracion/verDetallesRol.html', {
        'proyecto': proyecto,
        'participante': participante,
        'listaRol': union_listas
    })


def asignar_rol_por_fase(request, id_fase, id_usuario):
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
    fase = Fase.objects.get(pk=id_fase)
    usuario = Usuario.objects.get(pk=id_usuario)
    rol = Rol.objects.get(pk=id_rol)
    rol_actual = UsuarioxRol.objects.get(fase=fase, usuario=usuario, rol=rol)
    rol_actual.activo = False
    rol_actual.save()
    return HttpResponseRedirect(reverse('administracion:verRolesUsuario', args=(fase.proyecto.id, id_usuario)))
