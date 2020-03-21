
from django.urls import path

from . import views

app_name = 'administracion'
urlpatterns = [
#vamo a ver si me sale

path('roles/',views.Rol, name = 'roles' ),
path('roles/crear/',views.crear_rol, name='crearRol'),
path('roles/<id_rol>/',views.asignar_rol_por_fase, name='asignarRol'),
path('roles/<id_rol>/',views.desasignar_rol_al_usuario, name='desasignarRol')
]