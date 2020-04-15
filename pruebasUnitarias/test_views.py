"""
Modulo para hacer test sobre el modulo views.py
"""
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from login.views import index, user_register, users_access, user_update
from login.models import Usuario
from administracion.models import Proyecto, Fase, Rol, UsuarioxRol, TipoItem
from administracion.views import crear_proyecto, administrar_participantes, registrar_rol_por_fase, \
    asignar_rol_por_fase, desasignar_rol_al_usuario, administrar_comite, importar_tipo, confirmar_tipo_import, \
    mostrar_tipo_import, administrar_fases_del_proyecto, eliminar_participante_y_comite, crear_rol, \
    proyectos, estado_proyectov2

from administracion.views import estado_proyectov2, eliminar_participante_y_comite, crear_proyecto, \
    administrar_participantes, registrar_rol_por_fase, asignar_rol_por_fase, desasignar_rol_al_usuario, \
    administrar_comite, importar_tipo, confirmar_tipo_import, mostrar_tipo_import, administrar_fases_del_proyecto, \
    desactivar_tipo_item, editar_tipo

from desarrollo.models import Item
from desarrollo.views import solicitud_aprobacion, aprobar_item, desaprobar_item, desactivar_item
import pytest


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
        cls.tipo = TipoItem.objects.create(nombre='Tipo de item de prueba', prefijo='TIP')

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
        self.assertEqual(response.status_code, 302, 'No se redirecciona a verProyecto, eso implica que el proyecto no '
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
        self.assertIn(participante, self.proyecto.comite.all(),
                      "La prueba fallo por que no se pudo asignar a un miembro del comite")

    def test_importar_tipo(self):
        """
        CU 32: Crear tipo de item. Iteracion 2
        Este test comprueba que un participante sea efectivamente añadido al comite de un proyecto

        :return: el assert comprueba que en el proyecto exista un participante cuyo id sea igual al nombre del participante que se añadió a proyecto
        """
        request = RequestFactory()
        request.user = self.usuario
        tipo_a_importar = TipoItem.objects.create()
        response = confirmar_tipo_import(request, self.proyecto.id, tipo_a_importar.id)
        self.assertEqual(response.status_code, 200,
                         'La prueba falló porque no se pudo mostrar la vista con la lista de tipos de item')
        response = mostrar_tipo_import(request, self.proyecto.id)
        self.assertEqual(response.status_code, 200,
                         'La prueba falló porque no se pudo mostrar la vista del tipo de item a importar')
        importar_tipo(request, self.proyecto.id, tipo_a_importar.id)
        self.assertIn(tipo_a_importar, self.proyecto.tipoitem_set.all(),
                      "La prueba fallo por que no se pudo importar el tipo de item")

    def test_administrar_fases_del_proyecto(self):
        """
        CU 19: Editar fases. Iteracion 2
        Este test comprueba que se editen correctamente las propiedades de la fase
        :return: el assert comprueba que las propiedades hayan cambiado
        """
        path = reverse('administracion:administrarFasesProyecto', args=[self.proyecto.id])
        nuevo_nombre = 'Fase Prueba Editado'
        nueva_descripcion = 'Descripcion editada'
        fase_nueva = Fase.objects.create(nombre='Fase inicial', proyecto=self.proyecto,
                                         descripcion='Descripcion inicial')
        request = RequestFactory().post(path,
                                        {f'{fase_nueva.id}': [nuevo_nombre], f'd{fase_nueva.id}': [nueva_descripcion]})
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
        self.assertEqual(proyecto_iniciado.estado, 'finalizado', 'el estado del proyecto cambió a finalizado y '
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
        self.assertEqual(lista_fases.count(), p.numero_fases, 'No se ha creado el número correcto de fases')

    def test_verificar_proyecto(self):
        """
        CU 10: Crear Proyectos. Iteración 2
        Se verifica que el proyecto es creado correctamente y que tambien el url redirecciona a donde debe ir

        :return: el primer assert indica que el proyecto fue creado correctamente, envia un mensaje en caso contrario, y el segundo que el url redirecciona correctamente
        """
        ppp = Proyecto.objects.create(nombre='ppp', fecha_inicio=timezone.now().date(),
                                      numero_fases=5, cant_comite=3, gerente=self.usuario.id)
        response = self.client.post(reverse('administracion:crearProyecto'))
        self.assertEqual(ppp.nombre, 'ppp', 'indica que el proyecto no creado')
        self.assertEqual(response.status_code, 302)

    def test_proyectos(self):
        """
        CU 11: Listar proyectos por estado. Iteración 2
        Se listan los proyectos segun su estado actual, los cuales pueden ser iniciado, en ejecucion, finalizado o
        cancelado o por defecto todos, si no se hizo ningun filtro.

        :return: Retorna que se realiza correctamente el filtro
        """
        proyecto = Proyecto.objects.create(nombre='proyecto_T', fecha_inicio=timezone.now().date(),
                                           numero_fases=5, cant_comite=3, gerente=self.usuario.id)
        proy = Proyecto.objects.create(nombre='proyecto_x', fecha_inicio=timezone.now().date(),
                                       numero_fases=5, cant_comite=3, gerente=self.usuario.id)
        request = RequestFactory()
        request.user = self.usuario
        resp = proyectos(request, 'todos')
        assert resp.status_code == 200

    def test_estado_proyecto_cancelado(self):
        """
        CU 12: Gestionar estados del proyecto. Iteración 2
        Gestión correcta del estado del proyecto, en este estado se pasa algun proyecto a estado de cancelado

        :return: Se verifica que el cambio de estado se realizo correctamente, envia un mensaje en caso contrario
        """
        pl = Proyecto.objects.create(nombre='proyecto_turu', fecha_inicio=timezone.now().date(),
                                     numero_fases=5, cant_comite=3, gerente=self.usuario.id)
        request = RequestFactory()
        request.user = self.usuario
        estado_proyectov2(request, pl.id, 'cancelado')
        pl = Proyecto.objects.get(pk=pl.id)
        self.assertEqual(pl.estado, 'cancelado', 'no se logro cambiar de estado')

    def test_estado_proyecto_en_ejecucion(self):
        """
        CU 13: Modificar el estado del proyecto a en ejecución. Iteración 2
        Se modifica el estado del proyecto de iniciado a en ejecucion.

        :return: Se verifica que el cambio de estado se realizo correctamente, envia un mensaje en caso contrario
        """
        proyecto_iniciado = Proyecto.objects.create(nombre='proyectoEnEjecucion', fecha_inicio=timezone.now().date(),
                                                    numero_fases=5, cant_comite=3, gerente=self.usuario.id)
        request = RequestFactory()
        request.user = self.usuario
        estado_proyectov2(request, proyecto_iniciado.id, 'en ejecucion')
        proyecto_iniciado = Proyecto.objects.get(pk=proyecto_iniciado.id)
        self.assertEqual(proyecto_iniciado.estado, 'en ejecucion', 'el proyecto cambio de estado')

    def test_crear_admin_sistema(self):
        """
        CU 07: Crear Administrador del sistema. Iteracion 2

        :return: True si se crea correctamente el usuario administrador
        """

        # variable auxiliar para email random para arreglar el error de
        # email repetido en la bd de firebase
        aux = str(timezone.now()).split(' ')[1].split('.')[1].split('+')[0]

        # primero definimos la direccion del view a probar en el test
        path = reverse('login:register')
        # creamos un request de tipo post al que asignamos el path y los datos del proyecto a crear
        request = RequestFactory().post(path, {
            'username': 'AdminPrueba',
            'email': 'admin' + aux + '@admin.com',
            'password': 'admin123',
            'pass_confirmation': 'admin123',
            'first_name': 'Juan',
            'last_name': 'Perez',
        })
        response = user_register(request)
        usuario = Usuario.objects.get(username='AdminPrueba')
        self.assertTrue(usuario.is_superuser, 'No se pudo crear el usuario Administrador')
        self.assertEqual(response.status_code, 302, 'No se pudo crear el usuario Administrador')

    def test_desactivar_usuarios(self):
        """
        CU 08: Desactivar usuarios. Iteracion 2.

        :return: True, si desactiva al usuario
        """
        # Creo un usuario que con cuenta activa
        Usuario(username="Prueba", email="prueba@prueba.com", is_active=True).save()

        path = reverse('login:administrarAccesos')

        # hago el request para desactivar al usuario con id 2
        request = RequestFactory().post(path, {
            '2': 'False',
        })

        users_access(request)
        usuario = Usuario.objects.get(username='Prueba')

        self.assertFalse(usuario.is_active, "No se  pudo desactivar al usuario")

    def test_modificar_usuarios(self):
        """
        CU 09: Modificar usuarios. Iteracion 2.

        :return: Passed si se modifica correcta los datos de los usuarios
        """
        # self.usuario.username tiene como valor testusuario
        path = reverse("login:userUpdate", args=[self.usuario.username])

        request = RequestFactory().post(path, {
            'username': 'userModificado',
            'first_name': 'Juan',
            'last_name': 'Perez',
        })
        user_update(request, self.usuario.username)

        # Obtengo el usuario desde la base de datos
        usuario = Usuario.objects.get(id=self.usuario.id)

        self.assertEqual(usuario.username, 'userModificado', "Modificacion de username exitosa")
        self.assertEqual(usuario.first_name, 'Juan', "Modificacion de nombre exitosa")
        self.assertEqual(usuario.last_name, 'Perez', "Modificacion de apellido exitosa")

    def test_crear_rol(self):
        """
        CU 22: Crear rol. Iteracion 2.

        :return: Passed, si el Rol se creo de forma correcta
        """
        # Se agrega un nuevo proyecto
        proyecto = Proyecto(
            nombre='proyectoTest',
            fecha_inicio=timezone.now().date(),
            gerente=self.usuario.id,
            numero_fases=3,
            cant_comite=3,
        )

        proyecto.save()
        path = reverse('administracion:crearRol', args=[proyecto.id])
        request = RequestFactory().post(path, {
            'nombre': 'Aprobador',
            'crear_item': 'True',
            'modificar_item': 'True',
            'desactivar_item': 'True',
            'aprobar_item': 'True',
            'reversionar_item': 'False',
            'crear_relaciones_ph': 'True',
            'crear_relaciones_as': 'True',
            'borrar_relaciones': 'True',
        })
        request.user = self.usuario

        response = crear_rol(request, proyecto.id)

        rol = Rol.objects.get(nombre='Aprobador')

        self.assertEqual(rol.nombre, 'Aprobador', 'Se crea el rol correctamente')
        self.assertEqual(response.status_code, 302, 'Se crea el rol correctamente')

    def test_estado_proyecto_iniciado_cancelado(self):
        """
        CU 15: Modificar estado del proyecto a cancelado. Iteración 2

        :return: Passed, si el proyecto pasa a estado cancelado
        """
        proyecto_cancelado = Proyecto.objects.create(
            nombre='proyectoCancelado',
            fecha_inicio=timezone.now().date(),
            numero_fases=5,
            cant_comite=3,
            gerente=self.usuario.id
        )
        request = RequestFactory()
        request.user = self.usuario
        estado_proyectov2(request, proyecto_cancelado.id, 'cancelado')
        # sincronizamos el objeto con los nuevos cambios        proyecto_cancelado = Proyecto.objects.get(pk=proyecto_cancelado.id)
        self.assertEqual(proyecto_cancelado.estado, 'cancelado', 'El estado no puede cambiar a cancelado')

    def test_desactivar_tipo_item(self):
        """
        CU 31: Desactivar tipo de item
        :return: Passed en caso de que el tipo item quede fuera de la lista de los tipo items del proyecto
        """
        # se asigna el tipo al proyecto:
        self.tipo.proyecto.add(self.proyecto)
        request = RequestFactory()
        request.user = self.usuario
        desactivar_tipo_item(request, self.proyecto.id, self.tipo.id)
        self.assertNotIn(self.tipo, self.proyecto.tipoitem_set.all(), "El proyecto sigue con el tipo de item activo")

    def test_editar_tipo(self):
        """
        CU 30: Editar el tipo de item
        :return: Passed en caso de que el tipo item quede con los valores cambiados
        """
        # se asigna el tipo al proyecto:
        self.tipo.proyecto.add(self.proyecto)
        NOMBRE_EDITADO = 'nombre nuevo'
        PREFIJO_EDITADO = 'PRE'
        DESCRIPCION_EDITADA = 'descripcion nueva'
        path = reverse('administracion:editarTipoItem', args=[self.proyecto.id, self.tipo.id])
        request = RequestFactory().post(path, {
            'nombre': NOMBRE_EDITADO,
            'prefijo': PREFIJO_EDITADO,
            'descripcion': DESCRIPCION_EDITADA
        })
        request.user = self.usuario
        editar_tipo(request, self.proyecto.id, self.tipo.id)
        tipo_editado = TipoItem.objects.get(pk=self.tipo.id)
        self.assertEqual(NOMBRE_EDITADO, tipo_editado.nombre, "No se edito el nombre")
        self.assertEqual(PREFIJO_EDITADO, tipo_editado.prefijo, "No se edito el prefijo")
        self.assertEqual(DESCRIPCION_EDITADA, tipo_editado.descripcion, "No se edito la descripcion")

    def test_solicitud_aprobacion(self):
        """
        CU 38: Solicitar aprobación de ítems. Iteracion 3
        Se envia una solicitud para aprobar cierto item, el mismo debe tener un estado de en desarrollo
        para poder pasar a Pendiente de Aprobacion
        :return: Indica que se realizo correctamente la solicitud, envia un mensaje en caso contrario
        """
        pr = Proyecto.objects.create(nombre='proyecTest', fecha_inicio=timezone.now().date(),
                                     gerente=self.usuario.id, numero_fases=3, cant_comite=3)
        tipor = TipoItem.objects.create(nombre='CasoU', descripcion='fndmsn', prefijo='cu')
        fas = Fase.objects.create(nombre='Fasex', descripcion='dskjalñ', estado='abierta',
                                  proyecto=Proyecto.objects.get(pk=pr.id))
        cu_38 = Item.objects.create(nombre='cu_38', estado='en desarrollo', version=1, complejidad=5,
                                    descripcion='solicitar aprobacion', tipo_item=TipoItem.objects.get(pk=tipor.id),
                                    fase=Fase.objects.get(pk=fas.id))
        request = RequestFactory()
        request.user = self.usuario
        solicitud_aprobacion(request, id_item=cu_38.id)
        cu_38 = Item.objects.get(pk=cu_38.id)
        self.assertEqual(cu_38.estado, 'Pendiente de Aprobacion', 'No se puede realizar la solicitud')

    def test_aprobar_item(self):
        """
        CU 39: Aprobar ítems. Iteracion 3
        Una vez hecha la solicitud de aprobacion, el item queda en un estado de Pendiente de Aprobacion,
        de ahi, si esta correcto se aprueba y su estado pasa a ser Aprobado
        :return: Indica que el item fue correctamente aprobado, envia un mensaje en caso contrario
        """
        px = Proyecto.objects.create(nombre='projectTest', fecha_inicio=timezone.now().date(),
                                     gerente=self.usuario.id, numero_fases=3, cant_comite=3)
        tipox = TipoItem.objects.create(nombre='Casox', descripcion='uto', prefijo='cx')
        fasx = Fase.objects.create(nombre='Fasx', descripcion='dshh', estado='abierta',
                                   proyecto=Proyecto.objects.get(pk=px.id))
        cu_39_1 = Item.objects.create(nombre='cu_39_1', estado='Pendiente de Aprobacion', version=1, complejidad=5,
                                      descripcion='aprobar item', tipo_item=TipoItem.objects.get(pk=tipox.id),
                                      fase=Fase.objects.get(pk=fasx.id))
        request = RequestFactory()
        request.user = self.usuario
        aprobar_item(request, id_item=cu_39_1.id)
        cu_39_1 = Item.objects.get(pk=cu_39_1.id)
        self.assertEqual(cu_39_1.estado, 'Aprobado', 'No se puede realizar la accion')

    def test_desaprobar_item(self):
        """
        CU 39: Aprobar ítems. Iteracion 3
        En caso de que el item no se encuentre con los requerimientos pertinentes, se desaprueba y tal como
        indica el RF-127, el estado del item pasa de Pendiente de Aprobacion a en desarrollo nuevamente
        :return: Indica que el item fue desaprobado, caso contrario envia un mensaje
        """
        pp = Proyecto.objects.create(nombre='proTest', fecha_inicio=timezone.now().date(),
                                     gerente=self.usuario.id, numero_fases=3, cant_comite=3)
        tipop = TipoItem.objects.create(nombre='Casop', descripcion='bkdls', prefijo='cp')
        fasep = Fase.objects.create(nombre='Fasep', descripcion='shh', estado='abierta',
                                    proyecto=Proyecto.objects.get(pk=pp.id))
        cu_39_2 = Item.objects.create(nombre='cu_39_2', estado='Pendiente de Aprobacion', version=1, complejidad=5,
                                      descripcion='desaprobar item', tipo_item=TipoItem.objects.get(pk=tipop.id),
                                      fase=Fase.objects.get(pk=fasep.id))
        request = RequestFactory()
        request.user = self.usuario
        desaprobar_item(request, id_item=cu_39_2.id)
        cu_39_2 = Item.objects.get(pk=cu_39_2.id)
        self.assertEqual(cu_39_2.estado, 'en desarrollo', 'No se puede realizar la accion')

    def test_desactivar_item(self):
        """
        CU 40: Desactivar ítems. Iteracion 3
        Existe la posibilidad en la cual un item creado sea innecesario, por ello requiere ser desactivado,
        para realizar esta accion el mismo debe esta en el estado de en desarrollo y una vez desactivado
        su estado pasa a Desactivado
        :return: Indica que el item fue desactivado sin inconvenientes, envia un mensaje en caso contrario
        """
        pm = Proyecto.objects.create(nombre='proTest', fecha_inicio=timezone.now().date(),
                                     gerente=self.usuario.id, numero_fases=3, cant_comite=3)
        tipom = TipoItem.objects.create(nombre='Casom', descripcion='uuuto', prefijo='cm')
        fasem = Fase.objects.create(nombre='Fasem', descripcion='cdshh', estado='abierta',
                                   proyecto=Proyecto.objects.get(pk=pm.id))
        cu_40 = Item.objects.create(nombre='cu_40', estado='en desarrollo', version=1, complejidad=5,
                                      descripcion='desactivar item', tipo_item=TipoItem.objects.get(pk=tipom.id),
                                      fase=Fase.objects.get(pk=fasem.id))
        request = RequestFactory()
        request.user = self.usuario
        desactivar_item(request, id_item=cu_40.id)
        cu_40 = Item.objects.get(pk=cu_40.id)
        self.assertEqual(cu_40.estado, 'Desactivado', "No se puede realizar la accion")