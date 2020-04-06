from django.shortcuts import render, redirect
from django.urls import reverse

from desarrollo.models import Item, AtributoParticular
from administracion.models import  Proyecto, TipoItem
from desarrollo.forms import ItemForm


# Create your views here.

def crear_item(request, id_proyecto, id_tipo):
    proyecto = Proyecto.objects.get(pk=id_proyecto)
    tipo = TipoItem.objects.get(pk=id_tipo)
    plantilla_atr = tipo.plantillaatributo_set.all()
    if request.method == "POST":
        form = ItemForm(request.POST)
        nuevo_item = Item(nombre=tipo.prefijo, tipo_item=tipo, proyecto=proyecto)
        # primero creamos los atributos del ítem
        for atr in plantilla_atr:
            nuevo_atributo = AtributoParticular(item=nuevo_item, nombre=atr.nombre, tipo=atr.tipo,
                                                es_requerido=atr.es_requerido)
            nuevo_atributo.save()
        if form.is_valid():
            form.save()
            return redirect('login:index')
    else:
        form = ItemForm()

    return render(request, 'desarrollo/crearItem.html', {'proyecto': proyecto, 'tipo': tipo, 'form': form,
                                                         'plantilla_atr': plantilla_atr})
