from django.urls import path

from desarrollo import views

app_name = 'desarrollo'
urlpatterns = [
    # URLs de Mati
    path('desarrollo/<int:id_fase>/<int:id_tipo>', views.crear_item, name='crearItem'),
    path('desarrollo/<int:id_item>', views.ver_item, name='verItem'),
    path('desarrollo/<int:id_proyecto>/aprobacion', views.menu_aprobacion, name='menuAprobacion'),
    # URLs de David
    path('desarrollo/<str:filtro>', views.index, name='indexDesarrollo'),
    path('desarrollo/proyecto/<int:id_proyecto>', views.ver_proyecto, name='verProyecto'),
    path('desarrollo/proyecto/<int:id_proyecto>/item/<int:id_item>/adjuntar', views.adjuntar_archivo, name='adjuntarArchivo'),
    # URLs de Paola
    path('desarrollo/<int:id_item>', views.solicitud_aprobacion, name='solicitudAprobacionItem'),
    path('fases/int:<id_fase>/items/int:<id_item>/aprobar',views.aprobar_item, name= 'aprobarItem'),
    path('fases/int:<id_fase>/items/int:<id_item>/desactivar', views.desactivar_item, name='desactivarItem'),
]