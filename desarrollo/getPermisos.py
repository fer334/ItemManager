from administracion.models import UsuarioxRol, Rol


def has_permiso(fase, usuario, permiso):
    """
    Metodo que comprueba si un usuario tiene un permiso en especifico
    :param fase:
    :param usuario:
    :param permiso:
    :return: Booleano que indica si el usuario tiene o no el permiso
    """
    uxr_list = UsuarioxRol.objects.filter(fase=fase, usuario=usuario)
    if permiso == Rol.CREAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.crear_item:
                return True
        return False
    if permiso == Rol.MODIFICAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.modificar_item:
                return True
        return False
    if permiso == Rol.DESACTIVAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.desactivar_item:
                return True
        return False
    if permiso == Rol.APROBAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.aprobar_item:
                return True
        return False
    if permiso == Rol.REVERSIONAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.reversionar_item:
                return True
        return False
    if permiso == Rol.CREAR_RELACIONES_PH:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.crear_relaciones_ph:
                return True
        return False
    if permiso == Rol.CREAR_RELACIONES_AS:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.crear_relaciones_as:
                return True
        return False
    if permiso == Rol.BORRAR_RELACIONES:
        for user_x_rol in uxr_list:
            if user_x_rol.rol.borrar_relaciones:
                return True
        return False
    return False


def get_permisos(fase, usuario):
    """
    Metodo que busca todos los permisos del usuario para una fase y los devuelve en una lista
    :param fase:
    :param usuario:
    :return: Lista con los permisos del usuario para esa fase
    """
    uxr_list = UsuarioxRol.objects.filter(fase=fase, usuario=usuario)
    lista_permisos = []
    for user_x_rol in uxr_list:
        lista_permisos = lista_permisos + ([Rol.CREAR_ITEM] if user_x_rol.rol.crear_item and Rol.CREAR_ITEM not in lista_permisos else []) + \
        ([Rol.MODIFICAR_ITEM] if user_x_rol.rol.modificar_item and Rol.MODIFICAR_ITEM not in lista_permisos else []) + \
        ([Rol.DESACTIVAR_ITEM] if user_x_rol.rol.desactivar_item and Rol.DESACTIVAR_ITEM not in lista_permisos else []) + \
        ([Rol.APROBAR_ITEM] if user_x_rol.rol.aprobar_item and Rol.APROBAR_ITEM not in lista_permisos else []) + \
        ([Rol.REVERSIONAR_ITEM] if user_x_rol.rol.reversionar_item and Rol.REVERSIONAR_ITEM not in lista_permisos else []) + \
        ([Rol.CREAR_RELACIONES_PH] if user_x_rol.rol.crear_relaciones_ph and Rol.CREAR_RELACIONES_PH not in lista_permisos else []) + \
        ([Rol.CREAR_RELACIONES_AS] if user_x_rol.rol.crear_relaciones_as and Rol.CREAR_RELACIONES_AS not in lista_permisos else []) + \
        ([Rol.BORRAR_RELACIONES] if user_x_rol.rol.borrar_relaciones and Rol.BORRAR_RELACIONES not in lista_permisos else [])
    return lista_permisos
