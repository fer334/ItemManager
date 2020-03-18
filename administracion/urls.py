from django.urls import path

from . import views
app_name = 'administracion'
urlpatterns = [
    # no sé si el path de abajo está bien que deje en modadmin o puedo dejar vacio? no van a haber conflictos?
    path('modadmin/',views.index_administracion, name='indexAdmin'),
    path('tipo/', views.tipo_item, name='tipoItem'),
    path('<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('<int:id_proyecto>/tipo/registrarEnBase', views.registrarEnBase, name='registrarEnBase'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('proyectos/crear/', views.creando_proyecto, name='crearProyecto'),
    path('proyectos/registrar/', views.crear_proyecto, name='registrarProyecto'),
]
