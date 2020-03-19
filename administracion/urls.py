from django.urls import path

from . import views
app_name = 'administracion'
urlpatterns = [
    path('tipo/', views.tipo_item, name='index'),
    path('<int:id_proyecto>/tipo/<int:id_tipo>', views.ver_tipo, name='verTipoItem'),
    path('<int:id_proyecto>/tipo/crear/', views.crear_tipo, name='crearTipoItem'),
    path('<int:id_proyecto>/tipo/registrarEnBase', views.registrar_tipoitem_en_base, name='registrar_tipoitem_en_base'),
    path('proyectos/crear/', views.creando_proyecto, name='crearProyecto'),
    path('proyectos/registrar/', views.crear_proyecto, name='registrarProyecto'),
    path('tipo/<int:id_tipo>/atributo/', views.crear_atributo, name='crearAtributo'),
]
