from django.http import HttpResponse
from django.shortcuts import render

from .models import TipoItem, Proyecto


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


def ver_tipo(request, id_tipo):
    tipo_item = Proyecto.objects.get(pk=id_tipo)
    return render(request, 'administracion/verTipoItem.html', {})


def registrar_tipoitem_en_base(request, id_proyecto):
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    prefijo = request.POST['prefijo']
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    nuevo_tipo_item = TipoItem(nombre=nombre, descripcion=descripcion, prefijo=prefijo, proyecto=proyecto)
    nuevo_tipo_item.save()
    return HttpResponse("creado")
