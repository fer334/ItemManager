from django.urls import path

from administracion import views

app_name = 'administracion'
urlpatterns = [

    # URL DE PAO
    path('administracion/proyectos/<int:id_proyecto>/roles/crear/',views.crear_rol, name='crearRol'),
    path('administracion/proyectos/<int:id_proyecto>/roles', views.administrar_roles, name='administrarRoles'),
    path('administracion/proyectos/<int:id_proyecto>/roles/<int:id_rol>/desactivar/', views.desactivar_rol_proyecto, name='desactivarRol'),
    path('administracion/proyectos/<int:id_proyecto>/usuario/<int:id_usuario>/roles', views.ver_roles_usuario, name='verRolesUsuario'),
    path('administracion/fases/<int:id_fase>/usuario/<int:id_usuario>/roles/<int:id_rol>', views.desasignar_rol_al_usuario, name='desasignarRol'),
    path('administracion/fases/<int:id_fase>/usuario/<int:id_usuario>', views.asignar_rol_por_fase, name='asignarRol'),
    path('administracion/fases/<int:id_fase>/usuario/<int:id_usuario>/rol/<int:id_rol>', views.registrar_rol_por_fase, name='registrarRolPorFase'),
    # URLs DE MATI
    path('administracion/proyectos/<str:filtro>', views.proyectos, name='proyectos'),
    path('administracion/proyectos/crear/', views.crear_proyecto, name='crearProyecto'),
    path('administracion/proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    path('administracion/proyectos/<int:id_proyecto>/participantes', views.administrar_participantes, name='administrarParticipantes'),
    path('administracion/proyectos/<int:id_proyecto>/editar', views.editar_proyecto, name='editarProyecto'),
    path('administracion/proyectos/<int:id_proyecto>/estado', views.estado_proyectov2, name='estadoProyecto'),
    path('administracion/proyectos/<int:id_proyecto>/estado/<str:estado>', views.estado_proyectov2, name='estadoProyecto2'),
    path('administracion/proyectos/<int:id_proyecto>/adminfases', views.administrar_fases_del_proyecto, name='administrarFasesProyecto'),
    path('administracion/proyectos/<int:id_proyecto>/comite', views.administrar_comite, name='administrarComite'),
    path('administracion/proyectos/<int:id_proyecto>/<int:id_usuario>/<str:caso>', views.eliminar_participante_y_comite, name='desasignarUsuario'),
    path('administracion/proyectos/<int:id_proyecto>/accesodenegado/<str:caso>', views.acceso_denegado, name='accesoDenegado'),
    # URLs de DAVID
    path('administracion/tipo/todos', views.mostrar_tipo_item, name='tipoItem'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/showForImport', views.mostrar_tipo_import, name='importarTipoItem'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/mostrarImport', views.confirmar_tipo_import, name='confirmarImportarTipoItem'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/import', views.importar_tipo, name='importarTipoItemAProyecto'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/', views.ver_tipo_por_proyecto, name='tipoItemPorProyecto'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/editar/', views.editar_tipo, name='editarTipoItem'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/desactivar/', views.desactivar_tipo_item, name='desactivarTipoItem'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/registrarEnBase', views.registrar_tipoitem_en_base, name='registrarEnBase'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/<int:id_tipo>', views.ver_tipo, name='verTipoItem'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/atributo/crear', views.crear_atributo, name='crearAtributo'),
    path('administracion/proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/atributo/<int:id_atributo>/quitar/', views.quitar_atributo, name='quitarAtributo'),
]
