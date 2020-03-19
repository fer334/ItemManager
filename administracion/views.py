from django.http import HttpResponse
from django.shortcuts import render

from .models import TipoItem, Proyecto
from .forms import ProyectoForm

def index_administracion(request):
    return render(request,'administracion/indexAdmin.html')


def proyectos(request):
    lista_proyectos = Proyecto.objects.all()
    return render(request, 'administracion/proyectos.html', {'lista_proyectos' : lista_proyectos})


def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            fecha_inicio = request.POST['fecha_inicio']
            numero_fases = request.POST['numero_fases']
            # fases =
            gerente = request.POST['gerente']
            # comite =
            # participantes =
            nuevo_proyecto = Proyecto(nombre=nombre, fecha_inicio=fecha_inicio, numero_fases=numero_fases,
                                      gerente=gerente)
            nuevo_proyecto.save()

            return HttpResponse("Proyecto creado con éxito")
    else:
        form = ProyectoForm()

    return render(request, 'administracion/crearProyecto.html', {'form': form})


def ver_proyecto(request, id_proyecto):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    return render(request, 'administracion/verProyecto.html', {'proyecto': proyecto})


def tipo_item(request):
    return render(request, 'administracion/tipoItemTest.html', {})


def crear_tipo(request, id_proyecto):
    return render(request, 'administracion/crearTipoItem.html', {'id_proyecto': id_proyecto})


def registrarEnBase(request, id_proyecto):
    nombre = request.POST['nombre']
    descripcion = request.POST['descripcion']
    prefijo = request.POST['prefijo']
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    nuevo_tipo_item = TipoItem(nombre=nombre, descripcion=descripcion, prefijo=prefijo, proyecto=proyecto)
    nuevo_tipo_item.save()
    return HttpResponse("creado")
