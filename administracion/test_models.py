from django.test import TestCase
from administracion.models import Proyecto, Fase, TipoItem, PlantillaAtributo, Rol, UsuarioxRol
from login.models import Usuario
from django.utils import timezone
import pytest


@pytest.mark.django_db
class TestModels(TestCase):

    def test_Proyecto(self):
        proyecto_X = Proyecto(nombre='nombre', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                              gerente=1)
        assert proyecto_X.gerente == 1
        assert proyecto_X.nombre != 'hola', "falla porque no corresponde al nombre del proyecto"

    def test_Fase(self):
        proyecto_X = Proyecto(nombre='nombre', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                              gerente=1)
        fase_X = Fase(nombre='fase 1', descripcion='Fase que en la cual se incia el analisis del proyecto',
                      estado='abierta', proyecto=proyecto_X)

        assert fase_X.proyecto == proyecto_X
        assert fase_X.estado != 'cerrada', "falla porque la fase recien inicio por lo que es abierta"
        assert fase_X.nombre == 'fase 1'

    def test_tipo_item(self):
        proyecto_X = Proyecto(nombre='nombre', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3, gerente=1)
        proyecto_X.save()
        tipo_item_X = TipoItem(nombre='alfanumerico', descripcion='Se pueden escribir letras y numeros sin distincion',
                               prefijo='TI_1')
        tipo_item_X.save()
        tipo_item_X.proyecto.add(proyecto_X)
        assert tipo_item_X.prefijo != 'TI_2', "falla porque no corresponde"
        # assert tipo_item_X.proyecto ==

    def test_plantilla_atributo(self):
        tipo_item_X = TipoItem(nombre='alfanumerico', descripcion='Se pueden escribir letras y numeros sin distincion',
                               prefijo='TI_1')
        plantilla_X = PlantillaAtributo(nombre='alfanumerico', tipo='tipo_item_X', tipo_item=tipo_item_X)

        assert plantilla_X.tipo != 'tipo_2', "falla porque no corresponde"
        #assert plantilla_X.tipo_item == tipo_item_X

    def test_rol(self):
        proyecto_X = Proyecto(nombre='nombre', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                              gerente=1)
        rol_X = Rol(nombre='aprobador', proyecto=proyecto_X, crear_item=True, modificar_item=False,
                    desactivar_item=True,
                    aprobar_item=True, reversionar_item=True, crear_relaciones_ph=True, crear_relaciones_as=True,
                    borrar_relaciones=True)
        assert rol_X.crear_item == True
        assert rol_X.reversionar_item != False, "Falla porque no coinciden"
        assert rol_X.proyecto == proyecto_X


def test_usuariox_rol(self):
    usuario_X = Usuario.objects.create_user(username="prueba", email="prueba@mail.com", password="contraseña")
    proyecto_X = Proyecto(nombre='nombre', fecha_inicio=timezone.now().date(), numero_fases=5, cant_comite=3,
                          gerente=1)
    rol_X = Rol(nombre='aprobador', proyecto=proyecto_X, crear_item=True, modificar_item=False,
                desactivar_item=True,
                aprobar_item=True, reversionar_item=True, crear_relaciones_ph=True, crear_relaciones_as=True,
                borrar_relaciones=True)
    fase_X = Fase(nombre='fase 1', descripcion='Fase que en la cual se incia el analisis del proyecto',
                  estado='abierta', proyecto=proyecto_X)
    relacion = UsuarioxRol(usuario=usuario_X, rol=rol_X, fase= fase_X, activo=True)

    assert relacion.usuario == usuario_X
    assert relacion.rol == rol_X
    assert relacion.activo != False
