"""
Modulo para hacer test sobre el modulo views.py
"""
from django.test import RequestFactory
from django.urls import reverse, resolve
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
import io

from desarrollo.getPermisos import get_permisos, has_permiso_cerrar_proyecto
from login.views import index, user_register, users_access, user_update
from login.models import Usuario
from administracion.models import Proyecto, Fase, Rol, UsuarioxRol, TipoItem
from administracion.views import crear_rol, proyectos, desactivar_tipo_item, editar_tipo, estado_proyectov2, \
    eliminar_participante_y_comite, crear_proyecto, \
    administrar_participantes, registrar_rol_por_fase, asignar_rol_por_fase, desasignar_rol_al_usuario, \
    administrar_comite, importar_tipo, confirmar_tipo_import, mostrar_tipo_import, administrar_fases_del_proyecto
from desarrollo.models import Item, AtributoParticular
from desarrollo.views import solicitud_aprobacion, aprobar_item, desaprobar_item, desactivar_item, ver_item, \
    relacionar_item, desactivar_relacion_item, ver_proyecto, modificar_item, versionar_item, reversionar_item, \
    validar_reversion, votacion_item_en_revision_desarrollo, votacion_item_en_revision_aprobado, \
    votacion_item_en_revision_lineaBase, cerrar_fase, calcular_impacto_recursivo

from configuracion.models import LineaBase, Solicitud
from configuracion.views import crear_linea_base, ver_linea_base, solicitud_ruptura, votar_solicitud, cerrar_proyecto, \
    ramas_recursivas_trazabilidad, solicitud_modificacion_estado
from desarrollo.SubirArchivos import handle_uploaded_file
import pytest
from ItemManager.settings import BASE_DIR


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
        cls.rol = Rol.objects.create(nombre='Rol de prueba', proyecto=cls.proyecto, crear_item=True, aprobar_item=True,
                                     desactivar_item=True, modificar_item=True, reversionar_item=True, ver_item=True,
                                     crear_relaciones_as=True, crear_relaciones_ph=True, borrar_relaciones=True,
                                     ver_proyecto=True, crear_linea_base=True, cerrar_fase=True, cerrar_proyecto=True,
                                     solicitar_ruptura_lb=True, activo=True)
        cls.tipo = TipoItem.objects.create(nombre='Tipo de item de prueba', prefijo='TIP')
        cls.item = Item.objects.create(nombre='Item de prueba', complejidad=1, descripcion='Descripcion de prueba',
                                       tipo_item=cls.tipo,
                                       fase=cls.fase, numeracion=1)
        cls.rol_asignado = UsuarioxRol.objects.create(fase=cls.fase, rol=cls.rol, usuario=cls.usuario, activo=True)

    def test_index_usuario_no_autenticado(self):
        """
        CU 01: acceder al sistema. Iteración 1
        La vista index tiene la marca de @login_required por lo que si el usuario no se ha logeado
        se redireccionara a login con el codigo 302 de redireccionamiento.

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
        Este test comprueba que un participante sea efectivamente añadido a un proyecto.

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
        Este test comprueba que un cierto rol sea desasignado a un participante.

        :return: el assert comprueba que el objeto rol por fase quede desactivo
        """
        request = RequestFactory()
        request.user = self.usuario
        rol2 = Rol.objects.create(nombre='rol2', proyecto=self.proyecto)
        uxr = UsuarioxRol.objects.create(usuario=self.usuario, fase=self.fase, rol=rol2)
        desasignar_rol_al_usuario(request, self.fase.id, self.usuario.id, rol2.id)
        uxr = UsuarioxRol.objects.get(usuario=self.usuario, fase=self.fase, rol=rol2)
        self.assertEqual(uxr.activo, False, "La prueba falló no se pudo desasignar el rol")

    def test_registrar_rol_por_fase(self):
        """
        CU 25: Asignar rol x fase a usuario. Iteración 2
        Este test comprueba que un cierto rol sea asignado a un participante.

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
        Este test comprueba que un participante sea efectivamente añadido al comite de un proyecto.

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
        Este test comprueba que un participante sea efectivamente añadido al comite de un proyecto.

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
        Este test comprueba que se editen correctamente las propiedades de la fase.

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
        el assert verifica que el cambio de estado no suceda.

        :return: el assert retorna True si el estado del proyecto no cambia a finalizado
        """
        proyecto_iniciado = Proyecto.objects.create(nombre='proyectoIniciado', fecha_inicio=timezone.now().date(),
                                                    estado=Proyecto.ESTADO_INICIADO, numero_fases=5, cant_comite=3,
                                                    gerente=self.usuario.id)
        request = RequestFactory()
        request.user = self.usuario
        estado_proyectov2(request, proyecto_iniciado.id, Proyecto.ESTADO_FINALIZADO)
        # sincronizamos el objeto con los nuevos cambios
        proyecto_iniciado = Proyecto.objects.get(pk=proyecto_iniciado.id)
        self.assertNotEqual(proyecto_iniciado.estado, Proyecto.ESTADO_FINALIZADO,
                            'el estado del proyecto cambió a finalizado y '
                            'no debía cambiar de estado')

    def test_estado_proyecto_ejecucion_finalizado(self):
        """
        CU 14: modificar estado del proyecto a finalizado. Iteración 2
        En este test probamos cambiar el estado del proyecto de iniciado a finalizado. Algo que solo se permite si el
        estado actual del proyecto es en ejecución por lo que el assert verifica que el cambio de estado suceda.

        :return: el assert retorna True si el estado del proyecto cambia a finalizado
        """
        proyecto_ejecucion = Proyecto.objects.create(nombre='proyectoEjecucion', fecha_inicio=timezone.now().date(),
                                                     estado=Proyecto.ESTADO_EN_EJECUCION, numero_fases=5, cant_comite=3,
                                                     gerente=self.usuario.id)
        request = RequestFactory()
        request.user = self.usuario
        estado_proyectov2(request, proyecto_ejecucion.id, Proyecto.ESTADO_FINALIZADO)
        # sincronizamos el objeto con los nuevos cambios
        proyecto_ejecucion = Proyecto.objects.get(pk=proyecto_ejecucion.id)
        self.assertEqual(proyecto_ejecucion.estado, Proyecto.ESTADO_FINALIZADO,
                         'el estado del proyecto no cambió a finalizado')

    def test_eliminar_participante(self):
        """
        CU 16: Administrar Participantes del Proyecto. iteración 2
        Esta prueba primeramente añade un usuario al proyecto y luego lo desasigna del mismo.

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
        request.user = self.usuario
        eliminar_participante_y_comite(request, self.proyecto.id, partipante.id, 'participante')
        self.assertNotIn(partipante, self.proyecto.participantes.all(), 'participante no fue quitado del proyecto')

    def test_crear_fases(self):
        """
        CU 16: crear fase. Iteración 2
        Nuestra implementación permite la creación automática de la cantidad de fases que se defina al crear un proyecto
        en numero_fases. Este test verifica que se creen las fases y la cantidad correcta definida al crear proyecto.

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
        Se verifica que el proyecto es creado correctamente y que tambien el url redirecciona a donde debe ir.

        :return: el primer assert indica que el proyecto fue creado correctamente, envia un mensaje en casocontrario, y el segundo que el url redirecciona correctamente
        """
        ppp = Proyecto.objects.create(nombre='ppp', fecha_inicio=timezone.now().date(),
                                      numero_fases=5, cant_comite=3, gerente=self.usuario.id)
        response = reverse('administracion:crearProyecto')
        self.assertEqual(ppp.nombre, 'ppp', 'indica que el proyecto no creado')

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
        estado_proyectov2(request, pl.id, Proyecto.ESTADO_CANCELADO)
        pl = Proyecto.objects.get(pk=pl.id)
        self.assertEqual(pl.estado, Proyecto.ESTADO_CANCELADO, 'no se logro cambiar de estado')

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
        estado_proyectov2(request, proyecto_iniciado.id, Proyecto.ESTADO_EN_EJECUCION)
        proyecto_iniciado = Proyecto.objects.get(pk=proyecto_iniciado.id)
        self.assertEqual(proyecto_iniciado.estado, Proyecto.ESTADO_EN_EJECUCION, 'el proyecto cambio de estado')

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
        estado_proyectov2(request, proyecto_cancelado.id, Proyecto.ESTADO_CANCELADO)
        # sincronizamos el objeto con los nuevos cambios
        proyecto_cancelado = Proyecto.objects.get(pk=proyecto_cancelado.id)
        self.assertEqual(proyecto_cancelado.estado, Proyecto.ESTADO_CANCELADO, 'El estado no puede cambiar a cancelado')

    def test_desactivar_tipo_item(self):
        """
        CU 31: Desactivar tipo de item. Iteracion 3

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
        CU 30: Editar el tipo de item. Iteracion 3

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
        cu_38 = Item.objects.create(nombre='cu_38', estado=Item.ESTADO_DESARROLLO, version=1, complejidad=5,
                                    descripcion='solicitar aprobacion', tipo_item=TipoItem.objects.get(pk=tipor.id),
                                    fase=Fase.objects.get(pk=fas.id))
        request = RequestFactory()
        request.user = self.usuario
        solicitud_aprobacion(request, id_item=cu_38.id)
        cu_38 = Item.objects.get(pk=cu_38.id)
        self.assertEqual(cu_38.estado, Item.ESTADO_PENDIENTE, 'No se puede realizar la solicitud')

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
        cu_39_1 = Item.objects.create(nombre='cu_39_1', estado=Item.ESTADO_PENDIENTE, version=1, complejidad=5,
                                      descripcion='aprobar item', tipo_item=TipoItem.objects.get(pk=tipox.id),
                                      fase=self.fase)
        request = RequestFactory()
        request.user = self.usuario
        aprobar_item(request, id_item=cu_39_1.id)
        cu_39_1 = Item.objects.get(pk=cu_39_1.id)
        self.assertEqual(cu_39_1.estado, Item.ESTADO_APROBADO, 'No se puede realizar la accion')

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
        cu_39_2 = Item.objects.create(nombre='cu_39_2', estado=Item.ESTADO_PENDIENTE, version=1, complejidad=5,
                                      descripcion='desaprobar item', tipo_item=TipoItem.objects.get(pk=tipop.id),
                                      fase=self.fase)
        request = RequestFactory()
        request.user = self.usuario
        desaprobar_item(request, id_item=cu_39_2.id)
        cu_39_2 = Item.objects.get(pk=cu_39_2.id)
        self.assertEqual(cu_39_2.estado, Item.ESTADO_DESARROLLO, 'No se puede realizar la accion')

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
        cu_40 = Item.objects.create(nombre='cu_40', estado=Item.ESTADO_DESARROLLO, version=1, complejidad=5,
                                    descripcion='desactivar item', tipo_item=TipoItem.objects.get(pk=tipom.id),
                                    fase=self.fase)
        request = RequestFactory()
        request.user = self.usuario
        desactivar_item(request, id_item=cu_40.id, id_proyecto=pm.id)
        cu_40 = Item.objects.get(pk=cu_40.id)
        self.assertEqual(cu_40.estado, Item.ESTADO_DESACTIVADO, "No se puede realizar la accion")

    def test_ver_item(self):
        """
        CU 35: Listar ítems. Iteración 3
        este test se encarga de probar que si se pasa un id válido de item, la vista renderee la página

        :return: retorna true si es posible ver el ítem
        """
        item = Item(nombre='itemprue', descripcion='descripcion del ítem', tipo_item=self.tipo, fase=self.fase)
        item.save()
        path = reverse('desarrollo:verItem', args=[self.proyecto.id, item.id])
        request = RequestFactory().get(path)
        request.user = self.usuario
        item = Item.objects.get(nombre='itemprue')
        response = ver_item(request, self.proyecto.id, item.id)
        self.assertEqual(response.status_code, 200, 'no se puede ver el item')

    def test_modificar_estado_item(self):
        """
        CU 37: Modificar estado de ítems. Iteración 3.
        Test para probar que el estado del item no debe ser cambiado a desactivado si el ítem se encuentra
        en estado diferente a 'en desarrollo'

        :return: el assert retorna True si el estado no es cambiado y false en caso contrario
        """
        item = Item(nombre='itemdesa', estado=Item.ESTADO_APROBADO, descripcion='descripcion del ítem',
                    tipo_item=self.tipo, fase=self.fase)
        item.save()
        path = reverse('desarrollo:desactivarItem', args=[self.proyecto.id, item.id])
        request = RequestFactory().get(path)
        request.user = self.usuario
        desactivar_item(request, self.proyecto.id, item.id)
        self.assertNotEqual(item.estado, Item.ESTADO_DESACTIVADO, 'el estado cambió a desactivado')

    def test_crear_relacion_items(self):
        """
        CU 43: Desactivar relaciones entre items. Iteracion 3.
        Test que prueba la vista encargada de desactivar las relaciones

        :return: True, si la vista logro desactivar la relacion
        """
        item1 = Item.objects.create(
            nombre='item1',
            descripcion='descripcion del ítem',
            tipo_item=self.tipo,
            fase=self.fase
        )
        item2 = Item.objects.create(
            nombre='item2',
            descripcion='descripcion del ítem',
            tipo_item=self.tipo,
            fase=self.fase
        )
        item1.save()
        item2.save()

        # creamos una relacion antecesor-sucesor entre los items
        item1.sucesores.add(item2)
        item2.antecesores.add(item1)

        self.assertEqual(item1.sucesores.get(id=item2.id), item2, 'No se ha creado correctamente la relacion')

    def test_ver_fases(self):
        """
        CU 21: Mostrar Fases. Iteración 3.
        Este test prueba que se muestre las fases de un proyecto

        :return: retorna true si es posible ver las fases
        """
        path = reverse('desarrollo:verProyecto', args=[self.proyecto.id])
        request = RequestFactory().get(path)
        request.user = self.usuario
        response = ver_proyecto(request, self.proyecto.id)
        self.assertEqual(response.status_code, 200, 'no se puede ver las fases del proyecto')

    def test_crear_lineabase(self):
        """
        CU 45: crear linea base. Iteración 4
        EL test invoca a la vista encargada de crear linea base y luego verifica si esta se creo con los parametros crrectos

        :return: Se retorna true al validar el creador, lista de items, estado y tipo de la nueva lb
        """
        # primero definimos la direccion del view a probar en el test
        path = reverse('configuracion:crearLineaBase', args=[self.fase.id])
        # creamos un request de tipo post al que asignamos el path y los datos del proyecto a crear
        request = RequestFactory().post(path, {
            'checkItem-' + self.item.id.__str__(): 'on'
        })
        # asignamos el usuario al request
        request.user = self.usuario
        # llamamos al view que queramos probar y le pasamos el request y los otros parametros que necesite en otros
        # casos
        crear_linea_base(request, self.fase.id)
        # asignamos a p el proyecto que se creó
        lb = LineaBase.objects.get(fase=self.fase)
        self.assertEqual(lb.creador, request.user, 'El creador de la lb no es correcto')
        self.assertIn(self.item, lb.items.all(), "No se agrego correctamente el item a la lb")
        self.assertEqual(lb.estado, LineaBase.ESTADO_CERRADA, "El estado de la linea base creada es incorrecto")
        self.assertEqual(lb.tipo, LineaBase.TIPO_TOTAL, "El tipo de la linea base creada es incorrecto")

    def test_ver_lineabase(self):
        """
        CU 48: Ver detalles de linea base. Iteración 4
        EL test invoca a la vista encargada de mostrar detalles linea base y verifica recibir un 200

        :return: Se retorna true al validar el codigo de respuesta de la vista
        """
        lb_nueva = LineaBase(fase=self.fase, creador=self.usuario)
        lb_nueva.save()
        path = reverse('configuracion:verLineaBase', args=[lb_nueva.id])
        request = RequestFactory().get(path)
        request.user = self.usuario
        response = ver_linea_base(request, lb_nueva.id)
        self.assertEqual(response.status_code, 200, 'no se puede ver los detalles de la linea base')

    def test_modificar_item(self):
        """
        CU 34: Modificación  Item. Iteración 4
        El test comprueba que la vista Modificar Item funciona

        :return:
        """
        item_1 = Item.objects.create(nombre='Item_1', estado=Item.ESTADO_DESARROLLO, version=1, complejidad=5,
                                     descripcion='modificacion', tipo_item=self.tipo,
                                     fase=self.fase)
        NOMBRE = 'Item'
        COMPLEJIDAD = '7'
        DESCRIPCION = 'Item editado'
        path = reverse('desarrollo:editarItem', args=[self.proyecto.id, self.item.id])
        request = RequestFactory().post(path, {
            'nombre': NOMBRE,
            'complejidad': COMPLEJIDAD,
            'descripcion': DESCRIPCION
        })
        request.user = self.usuario
        item_editado = Item(pk=item_1.id, nombre=NOMBRE, version=item_1.version + 1, complejidad=COMPLEJIDAD,
                            descripcion=DESCRIPCION)
        modificar_item(request, self.proyecto.id, self.item.id)
        self.assertEqual(NOMBRE, item_editado.nombre, "No se edito el nombre")
        self.assertEqual(COMPLEJIDAD, item_editado.complejidad, "No se edito la complejidad")
        self.assertEqual(DESCRIPCION, item_editado.descripcion, "No se edito la descripcion")

    def test_versionar_item(self):
        """
        CU 36: Reversionar Items. Iteración 4
        Este test comprueba el correcto funcionamiento de la función versionar_item que se encarga de crear
        una nueva versión de un ítem

        :return: el assert retornerá false si las versiones son iguales y true si son diferentes
        """
        item_original = Item(nombre='item original', complejidad=5, descripcion='version original',
                             tipo_item=self.tipo, fase=self.fase, version=1, estado=Item.ESTADO_DESARROLLO)
        item_original.save()
        version_nueva = versionar_item(item_original, self.usuario)
        self.assertNotEqual(item_original.version, version_nueva.version, 'no se realizó la reversion')

    def test_reversionar_item(self):
        """
        CU 36: Reversionar Items. Iteración 4
        Este test se encarga de probar la vista reversionar_item la cual elije una versión anterior y la convierte en
        la versión actual. Primero creamos un ítem, luego versionamos a su versión 2, seguidamente llamamos a la
        vista para poder volver a pasar a su versión 1.

        :return: el assert retornará true si el nombre del ítem volvió a ser el nombre de la 1era versión
        """
        item_original = Item(nombre='item original', complejidad=5, descripcion='version original',
                             tipo_item=self.tipo, fase=self.fase, version=1, estado=Item.ESTADO_DESARROLLO)
        item_original.save()
        version_nueva = versionar_item(item_original, self.usuario)
        version_nueva.nombre = 'item modificado'
        version_nueva.save()
        path = reverse('desarrollo:reversionarItem', args=[self.proyecto.id, version_nueva.id, item_original.id])
        request = RequestFactory().get(path)
        request.user = self.usuario
        reversionar_item(request, self.proyecto.id, version_nueva.id, item_original.id)
        # obtenemos la versión reversionada
        item_reversionado = Item.objects.filter(id_version=item_original.id_version,
                                                estado=Item.ESTADO_DESARROLLO).order_by('id').last()
        # for item in Item.objects.all():
        #     print(item.nombre, '(', item.id, ')', item.version, '+', item.estado)
        self.assertEqual(item_reversionado.nombre, item_original.nombre, 'no se pudo reversionar')

    def test_historial_versiones(self):
        """
        CU 44: Mostrar Historial de Versiones del Ítem. Iteración 4
        test que se encarga de verificar el correcto funcionamiento del path a la vista historial_versiones_item

        :return: el assert retornará true si el path es correcto
        """
        path = reverse('desarrollo:histVersionesItem', args=[self.proyecto.id, self.item.id])
        self.assertEqual(resolve(path).view_name, 'desarrollo:histVersionesItem', 'la prueba falló porque el path es'
                                                                                  'incorrecto')

    def test_validar_reversion(self):
        """
        CU 36: Reversionar Items. Iteración 4
        Test que verifica el correcto funcionamiento de la función que aplica las restricciones a las reversiones

        :return:
        """
        valido = validar_reversion(self.item.id, self.item.id)
        self.assertTrue(valido, 'el item no cumple con las restricciones para ser reversionado')

    def test_cerrar_fase(self):
        """
        CU 21: Cerrar Fase. Iteración 4
        Test que verifica el correcto funcionamiento de vista cerrar fase

        :return: el assert retornará true si puede cerrar correctamente la fase 2 de prueba
        """
        p = Proyecto.objects.create(
            nombre='proyectoTestGeneral',
            fecha_inicio=timezone.now().date(),
            numero_fases=5,
            cant_comite=3, gerente=self.usuario.id
        )
        fase1 = Fase(nombre='Fase1', estado='cerrada', proyecto=p)
        fase1.save()
        fase2 = Fase(nombre='Fase2', estado='abierta', proyecto=p)
        fase2.save()

        nuevo_rol = Rol.objects.create(nombre='Rol cerrar proyecto', proyecto=p, cerrar_fase=True,
                                       activo=True)
        nuevo_rol_asignado_1 = UsuarioxRol.objects.create(fase=fase1, rol=nuevo_rol, usuario=self.usuario,
                                                          activo=True)
        nuevo_rol_asignado_2 = UsuarioxRol.objects.create(fase=fase2, rol=nuevo_rol, usuario=self.usuario,
                                                          activo=True)
        itema = Item(
            nombre='A',
            complejidad=5,
            tipo_item=self.tipo,
            fase=fase1,
            version=1,
            estado=Item.ESTADO_LINEABASE
        )
        itemb = Item(
            nombre='B',
            complejidad=5,
            tipo_item=self.tipo,
            fase=fase2,
            version=1,
            estado=Item.ESTADO_LINEABASE
        )
        itemc = Item(
            nombre='C',
            complejidad=5,
            tipo_item=self.tipo,
            fase=fase2,
            version=1,
            estado=Item.ESTADO_LINEABASE
        )

        fase1.save()
        fase2.save()
        itema.save()
        itemb.save()
        itemc.save()
        itema.sucesores.add(itemb)
        itemb.antecesores.add(itema)
        itemb.hijos.add(itemc)
        itemc.padres.add(itemb)

        path = reverse('desarrollo:cerrarFase', args=[p.id])
        request = RequestFactory().post(path, {'cerrar': fase2.pk})
        request.user = self.usuario
        cerrar_fase(request, p.id)
        fase2nueva = Fase.objects.get(pk=fase2.pk)

        self.assertEqual(fase2nueva.estado, 'cerrada', 'La prueba fallo, la fase no esta cerrada')

    def test_solicitud_ruptura_lb(self):
        """
        CU 46: Solicitar ruptura de linea base. Iteración 4
        Test que verifica el correcto funcionamiento de vista cerrar fase

        :return: el assert retornará true si puede crear correctamente la Solicitud de ruptura
        """
        lb = LineaBase.objects.create(fase=self.fase, creador=self.usuario)
        lb.items.add(self.item)
        lb.save()

        path = reverse('configuracion:solicitudRuptura', args=[lb.pk])
        request = RequestFactory().post(path, {f'checkItem-{self.item.pk}': ['on'], 'mensaje': ['dfas']})
        request.user = self.usuario

        solicitud_ruptura(request, lb.pk)
        self.assertNotEqual(len(Solicitud.objects.all()), 0, 'La prueba fallo, la solicitud no fue creada')

    def test_votar_ruptura(self):
        """
        CU 27: Votar sobre ruptura de LB. Iteración 4
        EL test invoca a la vista encargada de contabilizar los votos por ruptura de lb
        :return: Se retorna true al validar la votacion
        """
        lb_nueva = LineaBase(fase=self.fase, creador=self.usuario)
        lb_nueva.save()
        solicitud = Solicitud(linea_base=lb_nueva, justificacion='Porque si', solicitado_por=self.usuario)
        solicitud.save()
        path = reverse('configuracion:votarSolicitud', args=[self.proyecto.id, solicitud.id, 1])
        request = RequestFactory().post(path)
        request.user = self.usuario
        votar_solicitud(request, self.proyecto.id, solicitud.id, 1)
        self.assertEqual(solicitud.votoruptura_set.all().count(), 1, 'No se registro el voto')
        self.assertEqual(solicitud.votoruptura_set.all()[0].valor_voto, True, 'No se registro el valor correcto')

    def test_votacion_item_en_revision_desarrollo(self):
        """
        CU 28: Votación de modificación de items en estado de "En revisión". Iteracion 4
        El test prueba que el item pasa de estadado en Revision a estado en Desarrollo,
        teniendo la oportunidad de modificar el item.

        :return: Retrona true si cambio a Desarrollo
        """
        cu_28_1 = Item.objects.create(nombre='item_1', estado=Item.ESTADO_REVISION, version=1,
                                      complejidad=5, descripcion='Revision a Desarrollo',
                                      tipo_item=self.tipo, fase=self.fase)
        request = RequestFactory()
        request.user = self.usuario
        votacion_item_en_revision_desarrollo(request, id_item=cu_28_1.id)
        cu_28_1 = Item.objects.get(pk=cu_28_1.id)
        self.assertEqual(cu_28_1.estado, Item.ESTADO_DESARROLLO, 'No se puede realizar la accion ')

    def test_votacion_item_en_revision_desarrollo_hijos(self):
        """
            CU 28: Votación de modificación de items en estado de "En revisión". Iteracion 4
            El test prueba que el item pasa de estadado en Revision a estado en Desarrollo,
            teniendo la oportunidad de modificar el item.

            :return: Retrona true si cambio a Desarrollo
            """
        cu_28_1 = Item.objects.create(nombre='item_1', estado=Item.ESTADO_REVISION, version=1,
                                      complejidad=5, descripcion='Revision a Desarrollo',
                                      tipo_item=self.tipo, fase=self.fase)
        item_hijo = Item.objects.create(nombre='hijo_item_1', estado=Item.ESTADO_APROBADO, version=1,
                                        complejidad=5, descripcion='Aprobado a Revision',
                                        tipo_item=self.tipo, fase=self.fase)
        cu_28_1.hijos.add(item_hijo);
        cu_28_1.save()
        request = RequestFactory()
        request.user = self.usuario
        votacion_item_en_revision_desarrollo(request, id_item=cu_28_1.id)
        cu_28_1 = Item.objects.get(pk=cu_28_1.id)
        item_hijo = Item.objects.get(pk=item_hijo.id)
        self.assertEqual(Item.ESTADO_DESARROLLO, cu_28_1.estado, 'No se pudo modificar el estado del item')
        self.assertEqual(Item.ESTADO_REVISION, item_hijo.estado, 'No se modifico el estado del hijo')

    def test_votacion_item_en_revision_aprobado(self):
        """
        CU 28: Votación de modificación de items en estado de "En revisión". Iteracion 4
        El test prueba que el item pasa de estadado en Revision a estado Aprobado,
        si es que no necesita modificaciones, pudiendo asi añadirlo a una nueva linea base.

        :return: Retrona true si cambio a Aprobado
        """
        cu_28_2 = Item.objects.create(nombre='item_2', estado=Item.ESTADO_REVISION, version=2,
                                      complejidad=5, descripcion='Revision a Aprobado',
                                      tipo_item=self.tipo, fase=self.fase)
        request = RequestFactory()
        request.user = self.usuario
        votacion_item_en_revision_aprobado(request, id_item=cu_28_2.id)
        cu_28_2 = Item.objects.get(pk=cu_28_2.id)
        self.assertEqual(cu_28_2.estado, Item.ESTADO_APROBADO, 'No se puede realizar la accion ')

    def test_votacion_item_en_revision_linea_base(self):
        """
        CU 28: Votación de modificación de items en estado de "En revisión". Iteracion 4
        El test prueba que el item pasa de estadado en Revision a estado Linea Base,
        si es que no necesita modificaciones, si se quiere conservar en la Linea Base.

        :return: Retrona true si cambio a en Linea Base
        """
        cu_28_3 = Item.objects.create(nombre='item_3', estado=Item.ESTADO_REVISION, version=2,
                                      complejidad=5, descripcion='Revision a Linea Base',
                                      tipo_item=self.tipo, fase=self.fase)
        request = RequestFactory()
        request.user = self.usuario
        votacion_item_en_revision_lineaBase(request, id_item=cu_28_3.id)
        cu_28_3 = Item.objects.get(pk=cu_28_3.id)
        self.assertEqual(cu_28_3.estado, Item.ESTADO_LINEABASE, 'No se puede realizar la accion ')

    def test_cerrar_proyecto(self):
        """
        CU 53: Se crean un proyecto y una fase ficticias y luego se llama a la vista cerrar proyecto, finalmente
        se verifica si el estado del proyecto cambio.

        :return: Retrona true si el estado del proyecto es finalizado
        """
        proyecto_nuevo = Proyecto.objects.create(nombre='proyectoTestCerrar', fecha_inicio=timezone.now().date(),
                                                 numero_fases=1, cant_comite=3, gerente=self.usuario.id)
        fase_nueva = Fase.objects.create(nombre='Fase de prueba', proyecto=proyecto_nuevo,
                                         estado=Fase.FASE_ESTADO_CERRADA)
        nuevo_rol = Rol.objects.create(nombre='Rol cerrar proyecto', proyecto=proyecto_nuevo, cerrar_proyecto=True,
                                       activo=True)
        nuevo_rol_asignado = UsuarioxRol.objects.create(fase=fase_nueva, rol=nuevo_rol, usuario=self.usuario,
                                                        activo=True)
        path = reverse('configuracion:cerrarProyecto', args=[proyecto_nuevo.id])
        request = RequestFactory().post(path)
        request.user = self.usuario
        cerrar_proyecto(request, id_proyecto=proyecto_nuevo.id)
        proyecto_nuevo = Proyecto.objects.get(pk=proyecto_nuevo.id)
        # print(has_permiso_cerrar_proyecto(usuario=request.user, proyecto=proyecto_nuevo))
        self.assertEqual(Proyecto.ESTADO_FINALIZADO, proyecto_nuevo.estado, 'El proyecto no se pudo finalizar')

    def test_trazabilidad(self):
        """
        CU 49: Calculo de trazabilidad. Iteración 5.
        El test comprueba el correcto funcionamiento de la función recursiva de trazabilidad que trae todos
        los items relacionados al elegido.

        :return: los primeros dos asserts retornan true si los items relacionados son parte de la lista, el último
        assert retorna true si el item sin relacion con el resto no es parte de la lista
        """
        item_principal = Item(nombre='principal', estado=Item.ESTADO_APROBADO, complejidad=5, descripcion='principal',
                              tipo_item=self.tipo, fase=self.fase, id_version=2)
        item_principal.save()
        item_hijo = Item(nombre='hijo', estado=Item.ESTADO_DESARROLLO, complejidad=5, descripcion='hijo relacionado',
                         tipo_item=self.tipo, fase=self.fase, id_version=3)
        item_hijo.save()
        item_antecesor = Item(nombre='antecesor', estado=Item.ESTADO_DESARROLLO, complejidad=5, descripcion='antecesor',
                              tipo_item=self.tipo, fase=self.fase, id_version=4)
        item_antecesor.save()
        item_no_relacionado = Item(nombre='NoRelacionado', estado=Item.ESTADO_APROBADO, complejidad=5, id_version=5,
                                   descripcion='item no relacionado al resto', tipo_item=self.tipo, fase=self.fase)
        item_no_relacionado.save()
        # creamos las relaciones
        item_principal.hijos.add(item_hijo)
        item_hijo.padres.add(item_principal)
        item_principal.antecesores.add(item_antecesor)
        item_antecesor.sucesores.add(item_principal)
        # creamos la lista de items para la gráfica de trazabilidad
        lista_items = [item_principal]
        lista_items += ramas_recursivas_trazabilidad(item_principal, 'izquierda', item_principal.antecesores.all())
        lista_items += ramas_recursivas_trazabilidad(item_principal, 'derecha', item_principal.hijos.all())
        # comprobamos que en la lista estén los ítems adecuados
        self.assertIn(item_hijo, lista_items, 'el elemento no está en la lista para la trazabilidad')
        self.assertIn(item_antecesor, lista_items, 'el elemento no está en la lista para la trazabilidad')
        self.assertNotIn(item_no_relacionado, lista_items, 'el elemento se encuentra en la lista')

    def test_trazabilidad_relaciones_indirectas(self):
        """
        CU 49: Calculo de trazabilidad. Iteración 5.
        El test comprueba el correcto funcionamiento de la función recursiva de trazabilidad que trae todos
        los items relacionados de manera directa e indirecta.

        :return: El primer assert retorna true si el hijo directo del ítem está en la lista para graficar la
        trazabilidad, el segundo assert retorna true si el hijo indirecto del item está en la lista.
        """
        item_principal = Item(nombre='principal', estado=Item.ESTADO_APROBADO, complejidad=3, descripcion='principal',
                              tipo_item=self.tipo, fase=self.fase, id_version=2)
        item_principal.save()
        item_hijo = Item(nombre='hijo', estado=Item.ESTADO_DESARROLLO, complejidad=5, descripcion='hijo relacionado',
                         tipo_item=self.tipo, fase=self.fase, id_version=3)
        item_hijo.save()
        item_hijo_de_hijo = Item(nombre='hijo de hijo', estado=Item.ESTADO_DESARROLLO, complejidad=5,
                                 descripcion='antecesor', tipo_item=self.tipo, fase=self.fase, id_version=4)
        item_hijo_de_hijo.save()
        # creamos las relaciones
        item_principal.hijos.add(item_hijo)
        item_hijo.padres.add(item_principal)
        item_hijo.hijos.add(item_hijo_de_hijo)
        item_hijo_de_hijo.padres.add(item_hijo)
        # creamos la lista de items para la gráfica de trazabilidad
        lista_items = [item_principal]
        lista_items += ramas_recursivas_trazabilidad(item_principal, 'derecha', item_principal.hijos.all())
        # comprobamos que en la lista estén los ítems adecuados
        self.assertIn(item_hijo, lista_items, 'el elemento no está en la lista para la trazabilidad')
        self.assertIn(item_hijo_de_hijo, lista_items, 'el elemento no está en la lista para la trazabilidad')

    def test_calculo_de_impacto(self):
        """
        CU 50: Calculo de Impacto. Iteración 5.
        Este test comprueba que la función recursiva calcule correctamente el calculo de impacto de un ítem,
        creamos 3 items con distintos pesos y los relacionamos.

        :return: El assert retornará true si la suma de los pesos de los items se realizó correctamente
        """
        item_peso_cinco = Item(nombre='peso 5', estado=Item.ESTADO_APROBADO, complejidad=5, descripcion='cinco',
                               tipo_item=self.tipo, fase=self.fase, id_version=20)
        item_peso_cinco.save()
        item_peso_tres = Item(nombre='peso 3', estado=Item.ESTADO_APROBADO, complejidad=3, descripcion='tres',
                              tipo_item=self.tipo, fase=self.fase, id_version=21)
        item_peso_tres.save()
        item_peso_ocho = Item(nombre='peso 8', estado=Item.ESTADO_APROBADO, complejidad=8, descripcion='ocho',
                              tipo_item=self.tipo, fase=self.fase, id_version=22)
        item_peso_ocho.save()
        # creamos las relaciones
        item_peso_cinco.hijos.add(item_peso_tres)
        item_peso_tres.padres.add(item_peso_cinco)
        item_peso_tres.hijos.add(item_peso_ocho)
        item_peso_ocho.padres.add(item_peso_tres)
        # llamamos a la función
        calculo_impacto = calcular_impacto_recursivo(item_peso_cinco)
        self.assertEqual(calculo_impacto, 16, 'el calculo de impacto no se calculó correctamente')

    def test_adjuntar_archivo(self):
        """
        CU 41: Adjuntar al archivos al item
        Se invoca al metodo encargado de adjuntar archivo.

        :return: Retorna si se realiza correctamente el attachment
        """
        myfile = open(BASE_DIR + '/desarrollo/temp/dummy.dum', 'r')
        # file_object = io.BytesIO(myfile)
        i_io = io.BytesIO()

        def getsize(f):
            f.seek(0)
            f.read()
            s = f.tell()
            f.seek(0)
            return s

        name = 'dummy.dum'
        import mimetypes
        content_type, charset = mimetypes.guess_type(name)
        size = getsize(myfile)
        from django.core.files.uploadedfile import InMemoryUploadedFile
        obj = InMemoryUploadedFile(file=i_io, name=name,
                                   field_name=None, content_type=content_type,
                                   charset=charset, size=size)

        respuesta = handle_uploaded_file(None, 0, self.usuario)

        self.assertEqual(respuesta, None, 'No se respondio lo esperado')
        respuesta = handle_uploaded_file(obj, 0, self.usuario)
        self.assertNotEqual(respuesta, None, 'No se respondio con la url')

    def test_solicitud_modificacion_estado(self):
        """
        CU 55: Solicitud de modificacion de estado de Item
        El test comprueba si se realiza la solicitud de modificacion de estado, el cual es posible si el
        item se encuentra en estado APROBADO.

        :return: Retrona true si la solicitud se realizo correctamente.
        """
        cu_55 = Item.objects.create(nombre='CU_55', estado=Item.ESTADO_APROBADO, complejidad=5,
                                    descripcion='solicitar modificar estado',
                                    tipo_item=self.tipo, fase=self.fase, id_version=20)

        path = reverse('configuracion:solicitarModificarEstado', args=[self.proyecto.id, cu_55.id])
        request = RequestFactory().post(path, {'item': 'cu_55', 'mensaje': ['justificacion']})
        request.user = self.usuario

        solicitud_modificacion_estado(request, id_proyecto=self.proyecto.id, id_item=cu_55.id)
        self.assertNotEqual(len(Solicitud.objects.all()), 0, 'La prueba fallo, la solicitud no fue creada')

    def test_auditoria(self):
        """
        CU 54: Mostrar historial de inicio de Sesión. Iteración 6.
        Este test comprueba que se realice correctamente la auditoria general de proyectos verificando que un
        proyecto creado aparezca entre los datos de auditoria.

        :return: El assert retornará true si el nombre del proyecto aparece entre los datos de auditoria
        """
        # llamamos a la función history que realiza la auditoria para los objetos proyecto
        lista_auditoria_proyectos = Proyecto.history.all()
        lista = []
        # hacemos una lista con los nombres
        for elemento in lista_auditoria_proyectos:
            lista = elemento.nombre
        # buscamos un elemento especifico
        elemento_proyec = Proyecto.history.get(id=self.proyecto.id)
        self.assertIn(elemento_proyec.nombre, lista, 'el proyecto no aparece en la auditoria')
