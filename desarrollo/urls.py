from django.urls import path

from desarrollo import views

app_name = 'desarrollo'
urlpatterns = [
    # URLs de Mati
    path('desarrollo/<int:id_fase>/<int:id_tipo>', views.crear_item, name='crearItem'),
    # URLs de David
    path('desarrollo/<str:filtro>', views.index, name='indexDesarrollo'),
    path('desarrollo/proyecto/<int:id_proyecto>', views.ver_proyecto, name='verProyecto'),
]