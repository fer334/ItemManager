from django.test import TestCase, RequestFactory, Client
from administracion.models import Proyecto
from login.models import Usuario
from django.urls import reverse
from django.utils import timezone
import pytest


@pytest.mark.django_db
class TestViews(TestCase):

    def test_crear_proyecto(self):
        """
        Prueba en la cual se confirma que existe el url crearProyecto y que se crea el proyecto

        :return: el primer self.assertEqual() comprueba que existe el url
        """

        proyecto_X = Proyecto(nombre='proyecto_x', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                              gerente=1)
        response = self.client.post(reverse('administracion:crearProyecto'))
        resp = self.client.post(reverse('administracion:verProyecto'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(proyecto_X.nombre, resp.content)

        """  userTest = Usuario.objects.create(id.,username='usertest', email='test@mail.com', password='contrasenha').save()

        #proyecto_X = {
         #   'nombre': 'proyecto_x', 'fecha_inicio': '2020-04-02', 'numero_fases': 5, 'cant_comite': 3,
          #  'gerente': 1}

        
        path = reverse('administracion:crearProyecto')
        request = RequestFactory().get(path)
        response = self.client.post(path)

        self.assertEquals(proyecto_X.nombre, 'proyecto_x')

        # self.assertEquals(self.proyecto_X.firs().nombre,'proyecto_x')"""

        # proyecto_X = Proyecto(nombre='proyecto_x', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
        #                      gerente=1)
        # proyecto_X.save()


    def test_proyectos(self):
            assert False


    def test_ver_proyecto(self):
        assert False


    def test_estado_proyecto(self):
        assert False


    def test_index_administracion(self):
        assert False


def test_editar_proyecto():
    assert False
