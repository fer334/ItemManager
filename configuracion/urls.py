from django.urls import path

from configuracion import views

app_name = 'configuracion'
urlpatterns = [
    # URLs de Mati
    path('<str:filtro>', views.index, name='indexConfiguracion'),

    # URLs de David
    #path('<str:filtro>', views.index, name='indexDesarrollo'),
    #path('proyectos/<int:id_proyecto>/', views.ver_proyecto, name='verProyecto'),
    # URLs de Fer

    # URLs de Pao

]