"""
Modulo para hacer test sobre el modulo views.py
"""
from django.test import RequestFactory
from django.urls import reverse
from login.views import index
from django.contrib.auth.models import AnonymousUser
from login.models import Usuario
from django.utils import timezone
from administracion.models import Proyecto, Fase, Rol, UsuarioxRol, TipoItem
from administracion.views import crear_proyecto, administrar_participantes, registrar_rol_por_fase, asignar_rol_por_fase, desasignar_rol_al_usuario, administrar_comite, importar_tipo, confirmar_tipo_import, mostrar_tipo_import, administrar_fases_del_proyecto, estado_proyectov2, eliminar_participante_y_comite
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
        cls.fase = Fase.objects.create(nombre='Fase de prueba', proyecto=cls.proyecto)
        cls.rol = Rol.objects.create(nombre='Rol de prueba', proyecto=cls.proyecto)

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

        self.assertEqual(response.status_code, 200, 'La prueba falló porque el usuario no fue registrado')

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
        self.assertEqual(response.status_code,302, 'No se redirecciona a verProyecto, eso implica que el proyecto no '
                                                   'se creó')
        self.assertEqual(p.gerente, request.user.id, 'El gerente no es el usuario que hizo el request')

    def test_administrar_participantes(self):
        """
        CU 06: crear Usuario de Proyecto y CU 16: administrar participantes del proyecto. Iteración 2
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
        self.assertIn(partipante, self.proyecto.participantes.all(), 'participante no fue añadido al proyecto')

    def test_desasignar_rol_al_usuario(self):
        """
                CU 24: Desasignar rol x fase a usuario. Iteración 2
                Este test comprueba que un cierto rol sea desasignado a un participante

                :return: el assert comprueba que el objeto rol por fase quede desactivo
                """
        request = RequestFactory()
        request.user = self.usuario
        uxr = UsuarioxRol.objects.create(usuario=self.usuario, fase=self.fase, rol=self.rol)
        desasignar_rol_al_usuario(request, self.fase.id, self.usuario.id, self.rol.id)
        uxr = UsuarioxRol.objects.get(usuario=self.usuario, fase=self.fase, rol=self.rol)
        self.assertEqual(uxr.activo, False, "La prueba falló no se pudo desasignar el rol")

    def test_registrar_rol_por_fase(self):
        """
        CU 25: Asignar rol x fase a usuario. Iteración 2
        Este test comprueba que un cierto rol sea asignado a un participante

        :return: el assert comprueba que se cree el objeto rol por fase que representa la asignacion
        """
        path = reverse('administracion:asignarRol', args=[self.fase.id, self.usuario.id])
        request = RequestFactory().get(path)
        request.user = self.usuario
        response = asignar_rol_por_fase(request, self.fase.id, self.usuario.id)
        assert response.status_code == 200, 'La prueba falló porque no se pudo mostrar la vista de asignacion'
        request = RequestFactory()
        request.user = self.usuario
        registrar_rol_por_fase(request, self.fase.id, self.usuario.id, self.rol.id)
        assert UsuarioxRol.objects.filter(fase=self.fase, rol=self.rol, usuario=self.usuario), \
            "La prueba falló porque No se asigno rol"

    def test_administrar_comite(self):
            """
            CU 26: Crear comite de aprobacion de cambios
            Este test comprueba que un participante sea efectivamente añadido al comite de un proyecto

            :return: el assert comprueba que en el proyecto exista un participante cuyo id sea igual al nombre del participante que se añadió a proyecto
            """
            # creamos un usuario participante para el proyecto
            participante = Usuario.objects.create_user(
                username='participante1', email='estoes@otraprueba.com', password='password')
            # asignamos al path la vista administrar_comite
            path = reverse('administracion:administrarComite', args=[self.proyecto.id])
            request = RequestFactory().post(path, {'miembro_comite': participante.id})
            request.user = self.usuario
            administrar_comite(request, self.proyecto.id)
            self.assertIn(participante, self.proyecto.comite.all(), "La prueba fallo por que no se pudo asignar a un miembro del comite")

    def test_importar_tipo(self):
        """
        CU 32: Crear tipo de item
        Este test comprueba que un participante sea efectivamente añadido al comite de un proyecto

        :return: el assert comprueba que en el proyecto exista un participante cuyo id sea igual al nombre del participante que se añadió a proyecto
        """
        request = RequestFactory()
        request.user = self.usuario
        tipo_a_importar = TipoItem.objects.create()
        response = confirmar_tipo_import(request, self.proyecto.id, tipo_a_importar.id)
        self.assertEqual(response.status_code, 200, 'La prueba falló porque no se pudo mostrar la vista con la lista de tipos de item')
        response = mostrar_tipo_import(request, self.proyecto.id)
        self.assertEqual(response.status_code, 200, 'La prueba falló porque no se pudo mostrar la vista del tipo de item a importar')
        importar_tipo(request, self.proyecto.id, tipo_a_importar.id)
        self.assertIn(tipo_a_importar, self.proyecto.tipoitem_set.all(),"La prueba fallo por que no se pudo importar el tipo de item")

    def test_administrar_fases_del_proyecto(self):
        """
        CU 19: Editar fases
        Este test comprueba que se editen correctamente las propiedades de la fase
        :return: el assert comprueba que las propiedades hayan cambiado
        """
        path = reverse('administracion:administrarFasesProyecto', args=[self.proyecto.id])
        nuevo_nombre = 'Fase Prueba Editado'
        nueva_descripcion = 'Descripcion editada'
        fase_nueva = Fase.objects.create(nombre='Fase inicial', proyecto=self.proyecto, descripcion='Descripcion inicial')
        request = RequestFactory().post(path, {f'{fase_nueva.id}': [nuevo_nombre], f'd{fase_nueva.id}': [nueva_descripcion]})
        request.user = self.usuario
        administrar_fases_del_proyecto(request, self.proyecto.id)
        fase_nueva = Fase.objects.get(pk=fase_nueva.id)
        self.assertEqual(fase_nueva.nombre, nuevo_nombre, "No se pudo cambiar el nombre de la fase")
        self.assertEqual(fase_nueva.descripcion, nueva_descripcion, "No se pudo cambiar la descripcion de la fase")




    def test_estado_proyecto_iniciado_finalizado(self):
        """
        CU 14: modificar estado del proyecto a finalizado. Iteración 2
        En este test probamos cambiar el estado del proyecto de iniciado a finalizado. Algo que no se permite ya
        que solo puede cambiarse al estado finalizado si el estado actual del proyecto es en ejecución por lo que
        el assert verifica que el cambio de estado no suceda

        :return: el assert retorna True si el estado del proyecto no cambia a finalizado
        """
        proyecto_iniciado = Proyecto.objects.create(nombre='proyectoIniciado', fecha_inicio=timezone.now().date(),
                                                    numero_fases=5, cant_comite=3, gerente=self.usuario.id)
        request = RequestFactory()
        request.user = self.usuario
        estado_proyectov2(request, proyecto_iniciado.id, 'finalizado')
        # sincronizamos el objeto con los nuevos cambios
        proyecto_iniciado = Proyecto.objects.get(pk=proyecto_iniciado.id)
        self.assertNotEqual(proyecto_iniciado.estado, 'finalizado', 'el estado del proyecto cambió a finalizado y '
                                                                    'no debía cambiar de estado')

    def test_estado_proyecto_ejecucion_finalizado(self):
        """
        CU 14: modificar estado del proyecto a finalizado. Iteración 2
        En este test probamos cambiar el estado del proyecto de iniciado a finalizado. Algo que solo se permite si el
        estado actual del proyecto es en ejecución por lo que el assert verifica que el cambio de estado suceda

        :return: el assert retorna True si el estado del proyecto cambia a finalizado
        """
        proyecto_ejecucion = Proyecto.objects.create(nombre='proyectoEjecucion', fecha_inicio=timezone.now().date(),
                                                     estado='en ejecucion', numero_fases=5, cant_comite=3,
                                                     gerente=self.usuario.id)
        request = RequestFactory()
        request.user = self.usuario
        estado_proyectov2(request, proyecto_ejecucion.id, 'finalizado')
        # sincronizamos el objeto con los nuevos cambios
        proyecto_ejecucion = Proyecto.objects.get(pk=proyecto_ejecucion.id)
        self.assertEqual(proyecto_ejecucion.estado, 'finalizado', 'el estado del proyecto no cambió a finalizado')

    def test_eliminar_participante(self):
        """
        CU 16: Administrar Participantes del Proyecto. iteración 2
        Esta prueba primeramente añade un usuario al proyecto y luego lo desasigna del mismo

        :return: el assert comprueba que el usuario no sea participante del proyecto, en caso de ser retorna false
        """
        partipante = Usuario.objects.create_user(username='participante2',
                                                 email='estoes@otraprueba.com', password='password')
        # asignamos al path la vista administrar_participantes
        path = reverse('administracion:administrarParticipantes', args=[self.proyecto.id])
        request = RequestFactory().post(path, {'participante': partipante.id})
        request.user = self.usuario
        # añadimos al participante al proyecto
        administrar_participantes(request, self.proyecto.id)
        # eliminamos al participante del proyecto
        path2 = reverse('administracion:desasignarUsuario', args=[self.proyecto.id, partipante.id, 'participante'])
        request = RequestFactory().get(path2)
        eliminar_participante_y_comite(request, self.proyecto.id, partipante.id, 'participante')
        self.assertNotIn(partipante, self.proyecto.participantes.all(), 'participante no fue quitado del proyecto')

    def test_crear_fases(self):
        """
        CU 16: crear fase. Iteración 2
        Nuestra implementación permite la creación automática de la cantidad de fases que se defina al crear un proyecto
        en numero_fases. Este test verifica que se creen las fases y la cantidad correcta definida al crear proyecto
        :return: el primer assert retorna True si la lista de fases no está vacía y el segundo retorna True si la cantidad correcta de fases fue creada
        """
        path = reverse('administracion:crearProyecto')
        request = RequestFactory().post(path, {'nombre': 'proyectoFases', 'fecha_inicio': timezone.now().date(),
                                               'numero_fases': 3, 'cant_comite': 3})
        request.user = self.usuario
        crear_proyecto(request)
        p = Proyecto.objects.get(nombre='proyectoFases')
        lista_fases = p.fase_set.all()
        self.assertNotEqual(lista_fases, [], 'No se ha creado ninguna fase')
        self.assertEqual(lista_fases.count(), p.numero_fases, 'No se ha creado el número correcto de fases')
