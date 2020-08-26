from django.urls import path

from configuracion import views

app_name = 'configuracion'
urlpatterns = [
    # URLs de Mati
    path('<str:filtro>', views.index, name='indexConfiguracion'),

    # URLs de David
    path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    path('proyectos/fase/<int:id_fase>/crearLB', views.crear_linea_base, name='crearLineaBase'),
    path('proyectos/fase/lineabase/<int:id_lineabase>', views.ver_linea_base, name='verLineaBase'),
    path('proyectos/<int:id_proyecto>/comite/', views.comite_index, name='verIndexComite'),
    #path('proyectos/<int:id_proyecto>/comite/<int:id_solicitud>', views.ver_solicitud, name='verIndexComite'),
    # URLs de Fer
    path('lineabase/<int:id_lineabase>', views.solicitud_ruptura, name='solicitudRuptura'),

    # URLs de Pao

]