from django.urls import path

from . import views

app_name = 'administracion'
urlpatterns = [
    # no sé si el path de abajo está bien que deje en modadmin o puedo dejar vacio? no van a haber conflictos?
    # URLs DE MATI
    path('modadmin/', views.index_administracion, name='indexAdmin'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crearProyecto'),
    path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    # URLs de DAVID
    path('tipo/todos', views.mostrar_tipo_item, name='tipoItem'),
    path('<int:id_proyecto>/tipo/', views.ver_tipo_por_proyecto, name='tipoItemPorProyecto'),
    path('<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('<int:id_proyecto>/tipo/registrarEnBase', views.registrar_tipoitem_en_base, name='registrarEnBase'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>', views.ver_tipo, name='verTipoItem'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>/atributo/crear', views.crear_atributo, name='crearAtributo'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>/atributo/<int:id_atributo>/quitar/', views.quitar_atributo, name='quitarAtributo'),
]
