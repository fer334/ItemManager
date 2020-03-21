from django.urls import path

from administracion import views

app_name = 'administracion'
urlpatterns = [

    #URL DE PAO vamo a ver si me sale
    path('roles/',views.Rol, name = 'roles' ),
    path('roles/crear/',views.crear_rol, name='crearRol'),
    path('roles/<id_rol>/',views.asignar_rol_por_fase, name='asignarRol'),
    path('roles/<id_rol>/',views.desasignar_rol_al_usuario, name='desasignarRol'),
    # no sé si el path de abajo está bien que deje en modadmin o puedo dejar vacio? no van a haber conflictos?
    # URLs DE MATI
    path('modadmin/', views.index_administracion, name='indexAdmin'),
    path('proyectos/', views.proyectos, name='proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crearProyecto'),
    path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    # URLs de DAVID
    path('tipo/todos', views.mostrar_tipo_item, name='tipoItem'),
    path('<int:id_proyecto>/tipo/showForImport', views.mostrar_tipo_import, name='importarTipoItem'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>/mostrarImport', views.confirmar_tipo_import, name='confirmarImportarTipoItem'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>/import', views.importar_tipo, name='importarTipoItemAProyecto'),
    path('<int:id_proyecto>/tipo/', views.ver_tipo_por_proyecto, name='tipoItemPorProyecto'),
    path('<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('<int:id_proyecto>/tipo/registrarEnBase', views.registrar_tipoitem_en_base, name='registrarEnBase'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>', views.ver_tipo, name='verTipoItem'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>/atributo/crear', views.crear_atributo, name='crearAtributo'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>/atributo/<int:id_atributo>/quitar/', views.quitar_atributo, name='quitarAtributo'),
]
