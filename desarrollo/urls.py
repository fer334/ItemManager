from django.urls import path

from desarrollo import views

app_name = 'desarrollo'
urlpatterns = [
    # URLs de Mati
    path('fase/<int:id_fase>/tipo/<int:id_tipo>/items/crear', views.crear_item, name='crearItem'),
    path('proyectos/<int:id_proyecto>/items/<int:id_item>', views.ver_item, name='verItem'),
    path('proyectos/<int:id_proyecto>/aprobacion', views.menu_aprobacion, name='menuAprobacion'),
    # URLs de David
    path('<str:filtro>', views.index, name='indexDesarrollo'),
    path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    # URLs de Fer
    path('proyectos/<int:id_proyecto>/relacionar', views.relacionar_item, name='relacionar'),
    path('proyectos/<int:id_proyecto>/desactivar_relacion', views.desactivar_relacion_item, name='desactivarRelacion'),
    path('proyectos/<int:id_proyecto>/cerrar_fase', views.cerrar_fase, name='cerrarFase'),
    # URLs de Pao
    path('items/<int:id_item>/solicitar', views.solicitud_aprobacion, name='solicitarAprobacion'),
    path('proyectos/<int:id_proyecto>/items/<int:id_item>/desactivar', views.desactivar_item, name='desactivarItem'),
    path('items/<int:id_item>/aprobar', views.aprobar_item, name='aprobarItem'),
    path('items/<int:id_item>/desaprobar', views.desaprobar_item, name='desaprobarItem'),
    path('proyectos/<int:id_proyecto>/items/<int:id_item>/editar', views.modificar_item, name='editarItem')
]