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
]