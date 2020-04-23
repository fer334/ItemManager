"""
Modulo para hacer test sobre el modulo models.py
"""
from desarrollo.models import Item, Relacion
from login.models import Usuario
from administracion.models import Proyecto, Fase, Rol, TipoItem, UsuarioxRol, PlantillaAtributo
from django.utils import timezone
import pytest
from django.test import TestCase


@pytest.mark.django_db
class TestModels(TestCase):
    """
    Esta clase se utiliza para probar las clases que implementan o utilizan modelos django en el proyecto ItemManager
    """

    def test_usr(self):
        """
        CU 05: crear usuarios. Iteración 1
        Se probará la creación de un usuario con la implementacion Usuario

        :return: los asserts devuelven true si el usuario fue correctamente creado
        """
        usuario = Usuario.objects.create_user(username="prueba", email="prueba@mail.com", password="contraseña")

        self.assertEqual(usuario.username, 'prueba', 'Proyecto no fue creado correctamente')
        self.assertEqual(usuario.email, 'prueba@mail.com', 'Proyecto no fue creado correctamente')
        # obs: la contraseña estará encriptada por lo que no será igual a la guardada
        self.assertNotEqual(usuario.password, 'contraseña', "falla porque esta encriptado")

    def test_Proyecto(self):
        """
        CU 10: Crear Proyectos. Iteración 2

        Se prueban que los proyectos se crean correctamente.

        :return: Las afirmaciones devuelven true  si fueron creados correctamente, false en caso contrario.
        """
        proyecto_X = Proyecto(nombre='n', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                              gerente=1)
        assert proyecto_X.gerente == 1
        # obs: El nombre es distinto con que se pretende comparar
        assert proyecto_X.nombre != 'hola', "falla porque no corresponde al nombre del proyecto"

    def test_Fase(self):
        """
        CU 18: Crear Fase. Iteración 2.

        Se prueban que las fases se crean correctamente.
        :return: Las afirmaciones devuelven si la creacion fue realizada correctamente, envia un mensaje en caso
        contrario.
        """
        proyecto = Proyecto(nombre='nombre', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                            gerente=1)
        fase_X = Fase(nombre='fase 1', descripcion='Fase que en la cual se incia el analisis del proyecto',
                      estado='abierta', proyecto=proyecto)

        assert fase_X.proyecto == proyecto
        assert fase_X.estado != 'cerrada', "falla porque la fase recien inicio por lo que es abierta"
        assert fase_X.nombre == 'fase 1'

    def test_tipo_item(self):
        """
        CU 29:	Crear tipo de item. Iteración 2

        Se prueban que los tipos de item se crean correctamente.
        :return: La afirmacion devuelve si la creacion fue realizada correctamente, envia un mensaje en caso
        contrario
        """
        proyecto_X = Proyecto(nombre='no', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                              gerente=1)
        proyecto_X.save()
        tipo_item_X = TipoItem(nombre='alfanumerico',
                               descripcion='Se pueden escribir letras y numeros sin distincion',
                               prefijo='TI_1')
        tipo_item_X.save()
        tipo_item_X.proyecto.add(proyecto_X)
        assert tipo_item_X.prefijo != 'TI_2', "falla porque no corresponde"

    def test_plantilla_atributo(self):
        """
        Plantilla que ayuda a los tipos de item.

        :return: Demuestra que funciona el modelo
        """
        tipo_item_X = TipoItem(nombre='alfan',
                               descripcion='Se pueden escribir letras y numeros sin distincion',
                               prefijo='TI_1')
        plantilla_X = PlantillaAtributo(nombre='alfanumericO', tipo='tipo_item_X', tipo_item=tipo_item_X)

        assert plantilla_X.tipo != 'tipo_2', "falla porque no corresponde"
        # assert plantilla_X.tipo_item == tipo_item_X

    def test_rol(self):
        """
        CU 22:	Crear rol. Iteración 2

        Se prueban que crean los roles correctamente.
        :return: Las afirmaciones devuelven correctamente los parametros, envia un mensaje en caso contrario
        """
        proyecto_x = Proyecto(nombre='nombre', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                              gerente=1)
        role = Rol(nombre='aprobador', proyecto=proyecto_x, crear_item=True, modificar_item=False,
                   desactivar_item=True,
                   aprobar_item=True, reversionar_item=True, crear_relaciones_ph=True, crear_relaciones_as=True,
                   borrar_relaciones=True)
        assert role.crear_item == True
        assert role.reversionar_item != False, "Falla porque no coinciden"
        assert role.proyecto == proyecto_x

    def test_usuariox_rol(self):
        """
        Modelo en el cual se unen los roles, fases, y los proyectos.
        """
        usuario_X = Usuario.objects.create_user(username="PPP", email="TEST@mail.com", password="contra")
        proyect = Proyecto(nombre='nomB', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                           gerente=1)
        r = Rol(nombre='aprobador', proyecto=proyect, crear_item=True, modificar_item=False,
                desactivar_item=False, aprobar_item=True, reversionar_item=True, crear_relaciones_ph=True,
                crear_relaciones_as=True, borrar_relaciones=True)
        fase_X = Fase(nombre='fase 1', descripcion='Fase que en la cual se incia el analisis del proyecto',
                      estado='abierta', proyecto=proyect)
        relacion = UsuarioxRol(usuario=usuario_X, rol=r, fase=fase_X, activo=True)

        assert relacion.usuario == usuario_X
        assert relacion.rol == r
        assert relacion.activo != False

    def test_Item(self):
        """
        CU 33: Agregar Items. Iteración 3
        Test que prueba la creación de manera correcta de un objeto Item

        :return: los asserts verifican que se haya creado con el nombre correcto, que tenga el tipo de ítem correcto y que haya sido asignado a la fase correcta
        """
        proy = Proyecto(nombre='testProyect', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                        gerente=1)
        proy.save()
        tipo = TipoItem(nombre='tipoTest', descripcion='tipo de prueba', prefijo='TT')
        tipo.save()
        tipo.proyecto.add(proy)
        fase = Fase(nombre='faseTest', descripcion='fase de prueba', estado='abierta', proyecto=proy)
        item = Item(nombre='itemTest', complejidad=5, descripcion='descripcion del ítem', tipo_item=tipo, fase=fase)

        self.assertEqual(item.nombre, 'itemTest', 'No se ha creado el ítem')
        self.assertEqual(item.fase, fase, 'no se añadió a la fase correcta')
        self.assertEqual(item.tipo_item, tipo, 'no tiene el tipo correcto')

    def test_Item_complejidad(self):
        """
        CU 33: Agregar Items. Iteración 3
        Test que prueba la creación de un ítem cuya complejidad no está definida y le agrega un valor por defecto

        :return: el assert retorna true si la complejidad por defecto es asignada
        """
        pro = Proyecto(nombre='otroProy', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                       gerente=1)
        pro.save()
        tipo = TipoItem(nombre='tipoTest', descripcion='tipo de prueba', prefijo='TT')
        tipo.save()
        tipo.proyecto.add(pro)
        fase = Fase(nombre='faseTest', descripcion='fase de prueba', estado='abierta', proyecto=pro)
        item = Item(nombre='itemTest', descripcion='descripcion del ítem', tipo_item=tipo, fase=fase)

        self.assertEqual(item.complejidad, 5, 'La complejidad no fue asignada')

    def test_Relacion(self):
        """
        CU 42: Crear Relaciones. Iteracion 3
        Test que prueba la creacion de Relaciones entre dos items

        :return: True, si se creo la relacion de forma correcta
        """

        item1 = Item(
            nombre='itemTest',
            complejidad=5,
            descripcion='descripcion del ítem',
            # tipo_item=tipo,
            # fase=fase
        )
        item2 = Item(
            nombre='itemTest',
            complejidad=5,
            descripcion='descripcion del ítem',
            # tipo_item=tipo,
            # fase=fase
        )

        rel = Relacion(inicio=item1, fin=item2)

        self.assertEqual(rel.inicio, item1, 'No se ha creado correctamente la relacion izquierda')
        self.assertEqual(rel.fin, item2, 'No se ha creado correctamente la relacion derecha')
        self.assertEqual(rel.is_active, True, 'La relacion se creo pero esta desactivado')
