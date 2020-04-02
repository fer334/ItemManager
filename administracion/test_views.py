from django.test import TestCase, RequestFactory, Client
from administracion.models import Proyecto
from login.models import Usuario
from django.urls import reverse
from django.utils import timezone
import pytest


class TestViews(TestCase):

    @pytest.mark.django_db
    def test_crear_proyecto(self):
        """
        Prueba en la cual se prueba que existe el url crearProyecto y que se crea el proyecto

        :return:
        """
        """  userTest = Usuario.objects.create(id.,username='usertest', email='test@mail.com', password='contrasenha').save()

        #proyecto_X = {
         #   'nombre': 'proyecto_x', 'fecha_inicio': '2020-04-02', 'numero_fases': 5, 'cant_comite': 3,
          #  'gerente': 1}

        proyecto_X = Proyecto(nombre='proyecto_x', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                             gerente= 'localId')
        path = reverse('administracion:crearProyecto')
        request = RequestFactory().get(path)
        response = self.client.post(path)

        self.assertEquals(proyecto_X.nombre, 'proyecto_x')

        # self.assertEquals(self.proyecto_X.firs().nombre,'proyecto_x')"""

        # proyecto_X = Proyecto(nombre='proyecto_x', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
        #                      gerente=1)
        # proyecto_X.save()

        response = self.client.post(reverse('administracion:crearProyecto'))
        self.assertEqual(response.status_code, 200)
