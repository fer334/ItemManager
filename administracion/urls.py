from django.urls import path

from . import views
app_name = 'administracion'
urlpatterns = [
    path('tipo/', views.tipo_item, name='index'),
    path('tipo/crear/', views.crear_tipo, name='crearTipoItem'),
]
