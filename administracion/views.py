from django.shortcuts import render

# Create your views here.


def tipo_item(request):
    return render(request, 'administracion/tipoItemTest.html', {})


def crear_tipo(request):
    return render(request, 'administracion/crearTipoItem.html', {})
