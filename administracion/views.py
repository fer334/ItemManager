from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import TipoItem, Proyecto, PlantillaAtributo, Rol
from administracion.forms import ProyectoForm, ParticipanteForm
from login.models import Usuario
import datetime


def index_administracion(request):
    return render(request, 'administracion/indexAdmin.html')


def proyectos(request):
    lista_proyectos = Proyecto.objects.all()
    return render(request, 'administracion/proyectos.html', {'lista_proyectos': lista_proyectos})


def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            fecha_inicio = form.cleaned_data['fecha_inicio']
            numero_fases = form.cleaned_data['numero_fases']
            # fases =
            gerente = form.cleaned_data['gerente']
            # comite =
            nuevo_proyecto = Proyecto(nombre=nombre, fecha_inicio=fecha_inicio, numero_fases=numero_fases,
                                      gerente=gerente)
            nuevo_proyecto.save()
            participante = Usuario.objects.get(localId=gerente)
            nuevo_proyecto.participantes.add(participante)

            return HttpResponseRedirect(reverse('administracion:verProyecto', args=[nuevo_proyecto.id]))
    else:
        form = ProyectoForm()

    return render(request, 'administracion/crearProyecto.html', {'form': form})


def ver_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    gerente = Usuario.objects.get(localId=proyecto.gerente)
    tipo_item = proyecto.tipoitem_set.all()
    return render(request, 'administracion/verProyecto.html', {'proyecto': proyecto, 'gerente': gerente, 'tipo_item': tipo_item})


def administrar_participantes(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
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
            return render(request, 'administracion/editarProyecto.html', {'proyecto':proyecto})

    return render(request, 'administracion/editarProyecto.html', {'proyecto': proyecto})


def estado_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    if request.method == 'POST':
        estado = request.POST['estado']
        proyecto.estado = estado
        proyecto.save()
        return HttpResponseRedirect(reverse('administracion:estadoProyecto', args=[id_proyecto]))

    return render(request, 'administracion/estadoProyecto.html', {'proyecto': proyecto})


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


def crear_rol(request):
    return render(request, 'administracion/crearRol.html')


def crear_rol(request):
    Nombre = request.POST['Nombre']
    Permisos = request.POST['Permisos']
    nuevo_rol = Rol(Nombre=Nombre, Permisos=Permisos)
    nuevo_rol.save()
    return HttpResponse("Rol creado")


def asignar_rol_por_fase_al_usuario(request, id_rol):
    return render(request, 'administracion/asignarRol')


def asignar_rol_por_fase(request, id_rol):
    rol = Rol.objects.get(pk=id_rol)
    # nuevo_rol_asignado = rol(Nombre=Nombre,Permisos=Permisos)
    # nuevo_rol_asignado.save()
    return HttpResponse("Rol Asignado")


def desasignar_rol_al_usuario(request, id_rol):
    return render(request, 'admimistracion/desasignarRol.html')


def desasignar_rol_al_usuario(request, id_rol):
    rol = Rol.objects.get(pk=id_rol)
    # rol_desasignado = Rol(Nombre=Nombre, Permisos=Permisos)
    return HttpResponse("Rol sacado")
