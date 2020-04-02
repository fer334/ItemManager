"""
Modulo para hacer test sobre el modulo views.py
"""
from django.test import RequestFactory, Client
from django.urls import reverse
from login.views import index
from django.contrib.auth.models import AnonymousUser
from login.models import Usuario
from django.utils import timezone
from administracion.models import Proyecto
from administracion.views import crear_proyecto, administrar_participantes
import pytest
from django.test import TestCase


@pytest.mark.django_db
class TestViews(TestCase):
    """
    Clase para realizar pruebas sobre las vistas del proyecto ItemManager
    """

    @classmethod
    def setUpClass(cls):
        """
        Esta función sobreescribe setUpClass de TestCase y permite definir variables que serán usadas en varias clases
        """
        super(TestViews, cls).setUpClass()
        cls.usuario = Usuario.objects.create_user(
            username='testusuario', email='estoes@unaprueba.com', password='password')
        cls.proyecto = Proyecto.objects.create(nombre='proyectoTestGeneral', fecha_inicio=timezone.now().date(),
                                               numero_fases=5, cant_comite=3, gerente=cls.usuario.id)

    def test_index_usuario_no_autenticado(self):
        """
        CU 01: acceder al sistema. Iteración 1
        La vista index tiene la marca de @login_required por lo que si el usuario no se ha logeado
        se redireccionara a login con el codigo 302 de redireccionamiento

        :return: el assert retornara true si se hace un redireccionamiento y false en otros casos
        """
        path = reverse('login:index')
        request = RequestFactory().get(path)
        # la funcion anonymousUser simula un usuario sin logearse
        request.user = AnonymousUser()

        response = index(request)

        assert response.status_code == 302, 'Prueba falló porque no hubo redirección'

    def test_index_usuario_autenticado(self):
        """
        CU 01: acceder al sistema y CU 02: registrar usuario. Iteración 1
        Prueba parecida a la anterior pero con la diferencia de que se utiliza un usuario autenticado.

        :return: el assert retornara true si se hace un redireccionamiento y false en otros casos
        """
        path = reverse('login:index')
        request = RequestFactory().get(path)
        request.user = self.usuario

        response = index(request)

        assert response.status_code == 200, 'La prueba falló porque el usuario no fue registrado'

    def test_crear_proyecto(self):
        """
        CU 04: crear gerente de proyectos. Iteración 2
        Nuestra implementación de creación de proyecto asigna al usuario que crea el proyecto como el gerente del mismo
        por lo que este test primeramente crea un request que apunta crear_proyecto (view), luego crea un post para
        crear un proyecto y asigna un usuario logueado al request. Finalmente comprueba que se cree el proyecto y que el
        gerente del proyecto sea el usuario que hizo el request.

        :return: el primer assert retorna True si el codigo de respuesta es una redirección, en este caso a verProyecto.html. El segundo assert retorna True si el id del gerente es el mismo que el id del usuario que hizo el request
        """
        # primero definimos la direccion del view a probar en el test
        path = reverse('administracion:crearProyecto')
        # creamos un request de tipo post al que asignamos el path y los datos del proyecto a crear
        request = RequestFactory().post(path, {'nombre': 'proyectoTest', 'fecha_inicio': timezone.now().date(),
                                               'numero_fases': 3, 'cant_comite': 3})
        # asignamos el usuario al request
        request.user = self.usuario
        # llamamos al view que queramos probar y le pasamos el request y los otros parametros que necesite en otros
        # casos
        response = crear_proyecto(request)
        # asignamos a p el proyecto que se creó
        p = Proyecto.objects.get(nombre='proyectoTest')
        assert response.status_code == 302, 'No se redirecciona a verProyecto, eso implica que el proyecto no se creó'
        assert p.gerente == request.user.id, 'El gerente no es el usuario que hizo el request'

    def test_administrar_participantes(self):
        """
        CU 06: crear Usuario de Proyecto. Iteración 2
        Este test comprueba que un participante sea efectivamente añadido a un proyecto

        :return: el assert comprueba que en el proyecto exista un participante cuyo id sea igual al nombre del participante que se añadió a proyecto
        """
        # creamos un usuario participante para el proyecto
        partipante = Usuario.objects.create_user(
            username='participante1', email='estoes@otraprueba.com', password='password')
        # asignamos al path la vista administrar_participantes
        path = reverse('administracion:administrarParticipantes', args=[self.proyecto.id])
        request = RequestFactory().post(path, {'participante': partipante.id})
        request.user = self.usuario
        # llamamos a la vista a ser probada
        administrar_participantes(request, self.proyecto.id)
        assert self.proyecto.participantes.get(username='participante1').id == partipante.id, \
            'participante no fue añadido al proyecto'
