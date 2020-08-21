from django.urls import path

from configuracion import views

app_name = 'configuracion'
urlpatterns = [
    # URLs de Mati
    path('<str:filtro>', views.index, name='indexConfiguracion'),

    # URLs de David
    path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    path('proyectos/fase/<int:id_fase>/crearLB', views.vista_crear_linea_base, name='crearLineaBase'),
    # URLs de Fer

    # URLs de Pao

]