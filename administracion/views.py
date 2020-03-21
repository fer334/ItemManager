from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import TipoItem, Proyecto, PlantillaAtributo
from .forms import ProyectoForm
from login.models import Usuario


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
    gerente = Usuario.objects.get(localId=proyecto.gerente)
    return render(request, 'administracion/verProyecto.html', {'proyecto': proyecto, 'gerente': gerente})


def mostrar_tipo_item(request):
    tipo_items = TipoItem.objects.all()
    return render(request, 'administracion/tipoItemTest.html', {'lista_tipoitem': tipo_items})


def crear_tipo(request, id_proyecto):
    return render(request, 'administracion/crearTipoItem.html', {'id_proyecto': id_proyecto})


def ver_tipo(request, id_proyecto, id_tipo):
    obj_proyecto = Proyecto.objects.get(pk=id_proyecto)
    obj_tipo_item = TipoItem.objects.get(pk=id_tipo)
    return render(request, 'administracion/verTipoItem.html', {'proyecto': obj_proyecto, 'tipo_item': obj_tipo_item})


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
