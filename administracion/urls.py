from django.urls import path

from . import views
app_name = 'administracion'
urlpatterns = [
    path('tipo/', views.tipo_item, name='index'),
    path('<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('<int:id_proyecto>/tipo/registrarEnBase', views.registrarEnBase, name='registrarEnBase'),
    path('proyectos/crear/', views.creando_proyecto, name='crearProyecto'),
    path('proyectos/registrar/', views.crear_proyecto, name='registrarProyecto'),
]
