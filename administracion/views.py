from django.http import HttpResponse
from django.shortcuts import render

from .models import TipoItem, Proyecto

def tipo_item(request):
    return render(request, 'administracion/tipoItemTest.html', {})


def crear_tipo(request, id_proyecto):
    return render(request, 'administracion/crearTipoItem.html', {'id_proyecto':id_proyecto})


def registrarEnBase(request, id_proyecto):
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    prefijo = request.POST['prefijo']
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    nuevo_tipo_item = TipoItem(nombre=nombre, descripcion=descripcion, prefijo=prefijo, proyecto=proyecto)
    nuevo_tipo_item.save()
    return HttpResponse("creado")
