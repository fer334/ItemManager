from django.urls import path

from . import views
app_name = 'administracion'
urlpatterns = [
    path('tipo/', views.tipo_item, name='index'),
    path('tipo/<int:id_tipo>', views.ver_tipo, name='verTipoItem'),
    path('<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('<int:id_proyecto>/tipo/registrarEnBase', views.registrarEnBase, name='registrarTipoItemEnBase'),
]
