
from django.http import HttpResponse
from django.shortcuts import render

from .models import Rol


def crear_rol (request):
    return render(request, 'administracion/crearRol.html')

def crear_rol(request):
    Nombre = request.POST['Nombre']
    Permisos = request.POST['Permisos']
    nuevo_rol = Rol(Nombre= Nombre, Permisos= Permisos)
    nuevo_rol.save()
    return HttpResponse("Rol creado")


def asignar_rol_por_fase_al_usuario(request, id_rol):
    return render(request, 'administracion/asignarRol')

def asignar_rol_por_fase(request, id_rol):
    Rol = Rol.objects.get(pk=id_rol)
    nuevo_rol_asignado = Rol(Nombre=Nombre,Permisos=Permisos)
    nuevo_rol_asignado.save()
    return HttpResponse("Rol Asignado")

def desasignar_rol_al_usuario(request, id_rol):
    return render (request, 'admimistracion/desasignarRol.html')

def desasignar_rol_al_usuario(request, id_rol):
    Rol = Rol.objects.get(pk=id_rol)
    rol_desasignado = Rol(Nombre=Nombre, Permisos=Permisos)
    return HttpResponse("Rol sacado")
