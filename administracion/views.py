from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import TipoItem, Proyecto, PlantillaAtributo


def creando_proyecto(request):
    return render(request, 'administracion/crearProyecto.html')


def crear_proyecto(request):
    nombre = request.POST['nombre']
    fecha_inicio = request.POST['fecha_inicio']
    numero_fases = request.POST['numero_fase']
    # fases =
    gerente = request.POST['gerente']
    # comite =
    # participantes =
    nuevo_proyecto = Proyecto(nombre=nombre, fecha_inicio=fecha_inicio, numero_fases=numero_fases, gerente=gerente)
    nuevo_proyecto.save()
    return HttpResponse("Proyecto creado con éxito")


def tipo_item(request):
    return render(request, 'administracion/tipoItemTest.html', {})


def crear_tipo(request, id_proyecto):
    return render(request, 'administracion/crearTipoItem.html', {'id_proyecto':id_proyecto})


def ver_tipo(request, id_proyecto, id_tipo):
    #tipo_item = Proyecto.objects.get(pk=id_proyecto)
    print(id_proyecto)
    obj_proyecto = Proyecto.objects.get(pk=id_proyecto)
    obj_tipo_item = TipoItem.objects.get(pk=id_tipo)
    print(id_tipo)
    return render(request, 'administracion/verTipoItem.html', {'proyecto': obj_proyecto,'tipo_item':obj_tipo_item})


def registrar_tipoitem_en_base(request, id_proyecto):
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    prefijo = request.POST['prefijo']
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    nuevo_tipo_item = TipoItem(nombre=nombre, descripcion=descripcion, prefijo=prefijo)
    nuevo_tipo_item.save()
    nuevo_tipo_item.proyecto.add(proyecto)

    return HttpResponseRedirect(reverse('administracion:verTipoItem',args=(id_proyecto, nuevo_tipo_item.id)))


def crear_atributo(request, id_proyecto, id_tipo):
    nombre = request.POST['nombre']
    tipo = request.POST['tipo']
    tipo_item = TipoItem.objects.get(pk=id_tipo)
    atributo = PlantillaAtributo(nombre=nombre, tipo=tipo, tipo_item=tipo_item)
    atributo.save()
    return HttpResponseRedirect(reverse('administracion:verTipoItem',args=(id_proyecto, tipo_item.id)))

def quitar_atributo(request, id_proyecto, id_tipo):
    return HttpResponse("Quitado")