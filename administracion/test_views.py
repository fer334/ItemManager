from .models import Proyecto, Fase, Rol, UsuarioxRol
from login.models import Usuario
from administracion.views import desasignar_rol_al_usuario
from django.test import RequestFactory
from django.urls import reverse
import datetime
import pytest

class TestViews:
    def test_desasignar_rol_al_usuario(self):
        path = reverse('administracion:desasignarRol')
        request = RequestFactory().get(path)
        usuario = Usuario.objects.create_user(
            username='testusuario', email='estoes@unaprueba.com', password='password')
        proyecto = Proyecto.objects.create_proyecto(nombre='Prueba', fecha_inicio=datetime.now, numero_fases=3,
                                                    cant_comite=3)
        assert True
