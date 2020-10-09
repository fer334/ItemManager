from django.urls import path

from configuracion import views

app_name = 'configuracion'
urlpatterns = [
    # URLs de Mati
    path('<str:filtro>', views.index, name='indexConfiguracion'),
    path('proyectos/<int:id_proyecto>/item/<int:id_item>/trazabilidad', views.trazabilidad, name='trazabilidad'),
    path('proyectos/<int:id_proyecto>/item/<int:id_item>/trazabilidad/reporte', views.reporte_trazabilidad, name='reporteTrazabilidad'),

    # URLs de David
    path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    path('proyectos/fase/<int:id_fase>/crearLB', views.crear_linea_base, name='crearLineaBase'),
    path('proyectos/fase/lineabase/<int:id_lineabase>', views.ver_linea_base, name='verLineaBase'),
    path('proyectos/<int:id_proyecto>/comite/', views.comite_index, name='verIndexComite'),
    path('proyectos/<int:id_proyecto>/comite/<int:id_solicitud>/votar/<int:voto>', views.votar_solicitud, name='votarSolicitud'),
    path('proyectos/<int:id_proyecto>/cerrar', views.cerrar_proyecto, name='cerrarProyecto'),
    # URLs de Fer
    path('lineabase/<int:id_lineabase>', views.solicitud_ruptura, name='solicitudRuptura'),

    # URLs de Pao
    path('proyectos/<int:id_proyecto>/item/<int:id_item>/solicitarDesaprobar', views.solicitud_modificacion_estado, name='solicitarModificarEstado'),
    #path('proyectos/<int:id_proyecto>/comite/<int:id_solicitud>/votarItem/<int:voto>', views.votar_solicitud_desaprobacion, name='votarSolicitudDesaprobacion')

]
