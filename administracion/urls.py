from django.urls import path

from administracion import views

app_name = 'administracion'
urlpatterns = [

    # URL DE PAO
    path('proyectos/<int:id_proyecto>/roles/crear/',views.crear_rol, name='crearRol'),
    path('proyectos/<int:id_proyecto>/roles', views.administrar_roles, name='administrarRoles'),
    path('proyectos/<int:id_proyecto>/roles/<int:id_rol>/desactivar/', views.desactivar_rol_proyecto, name='desactivarRol'),
    path('proyectos/<int:id_proyecto>/usuario/<int:id_usuario>/roles', views.ver_roles_usuario, name='verRolesUsuario'),
    path('fases/<int:id_fase>/usuario/<int:id_usuario>/roles/<int:id_rol>', views.desasignar_rol_al_usuario, name='desasignarRol'),
    path('fases/<int:id_fase>/usuario/<int:id_usuario>', views.asignar_rol_por_fase, name='asignarRol'),
    path('fases/<int:id_fase>/usuario/<int:id_usuario>/rol/<int:id_rol>', views.registrar_rol_por_fase, name='registrarRolPorFase'),
    # URLs DE MATI
    path('proyectos/<str:filtro>', views.proyectos, name='proyectos'),
    path('proyectos/crear/', views.crear_proyecto, name='crearProyecto'),
    path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    path('proyectos/<int:id_proyecto>/participantes', views.administrar_participantes, name='administrarParticipantes'),
    path('proyectos/<int:id_proyecto>/editar', views.editar_proyecto, name='editarProyecto'),
    path('proyectos/<int:id_proyecto>/estado', views.estado_proyectov2, name='estadoProyecto'),
    path('proyectos/<int:id_proyecto>/estado/<str:estado>', views.estado_proyectov2, name='estadoProyecto2'),
    path('proyectos/<int:id_proyecto>/adminfases', views.administrar_fases_del_proyecto, name='administrarFasesProyecto'),
    path('proyectos/<int:id_proyecto>/comite', views.administrar_comite, name='administrarComite'),
    path('proyectos/<int:id_proyecto>/<int:id_usuario>/<str:caso>', views.eliminar_participante_y_comite, name='desasignarUsuario'),
    path('proyectos/<int:id_proyecto>/accesodenegado/<str:caso>', views.acceso_denegado, name='accesoDenegado'),
    # URLs de DAVID
    path('tipo/todos', views.mostrar_tipo_item, name='tipoItem'),
    path('proyectos/<int:id_proyecto>/tipo/showForImport', views.mostrar_tipo_import, name='importarTipoItem'),
    path('proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/mostrarImport', views.confirmar_tipo_import, name='confirmarImportarTipoItem'),
    path('proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/import', views.importar_tipo, name='importarTipoItemAProyecto'),
    path('proyectos/<int:id_proyecto>/tipo/', views.ver_tipo_por_proyecto, name='tipoItemPorProyecto'),
    path('proyectos/<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/editar/', views.editar_tipo, name='editarTipoItem'),
    path('proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/desactivar/', views.desactivar_tipo_item, name='desactivarTipoItem'),
    path('proyectos/<int:id_proyecto>/tipo/registrarEnBase', views.registrar_tipoitem_en_base, name='registrarEnBase'),
    path('proyectos/<int:id_proyecto>/tipo/<int:id_tipo>', views.ver_tipo, name='verTipoItem'),
    path('proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/atributo/crear', views.crear_atributo, name='crearAtributo'),
    path('proyectos/<int:id_proyecto>/tipo/<int:id_tipo>/atributo/<int:id_atributo>/quitar/', views.quitar_atributo, name='quitarAtributo'),
]
