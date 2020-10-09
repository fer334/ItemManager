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
            if user_x_rol.activo and user_x_rol.rol.crear_item:
                return True
        return False
    if permiso == Rol.MODIFICAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.modificar_item:
                return True
        return False
    if permiso == Rol.DESACTIVAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.desactivar_item:
                return True
        return False
    if permiso == Rol.APROBAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.aprobar_item:
                return True
        return False
    if permiso == Rol.REVERSIONAR_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.reversionar_item:
                return True
        return False
    if permiso == Rol.CREAR_RELACIONES_PH:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.crear_relaciones_ph:
                return True
        return False
    if permiso == Rol.CREAR_RELACIONES_AS:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.crear_relaciones_as:
                return True
        return False
    if permiso == Rol.BORRAR_RELACIONES:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.borrar_relaciones:
                return True
        return False
    if permiso == Rol.VER_ITEM:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.ver_item:
                return True
        return False
    if permiso == Rol.CREAR_LINEA_BASE:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.crear_linea_base:
                return True
        return False
    if permiso == Rol.CERRAR_FASE:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.cerrar_fase:
                return True
        return False
    if permiso == Rol.CERRAR_PROYECTO:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.cerrar_proyecto:
                return True
        return False
    if permiso == Rol.VER_PROYECTO:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.ver_proyecto:
                return True
        return False
    if permiso == Rol.SOLICITAR_RUPTURA_LB:
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.solicitar_ruptura_lb:
                return True
        return False
    return False


def has_permiso_cerrar_proyecto(proyecto, usuario):
    """
    Metodo que comprueba si un usuario tiene un permiso en especifico
    :param fase:
    :param usuario:
    :param permiso:
    :return: Booleano que indica si el usuario tiene o no el permiso
    """
    for fase in proyecto.fase_set.all():
        uxr_list = UsuarioxRol.objects.filter(fase=fase, usuario=usuario)
        for user_x_rol in uxr_list:
            if user_x_rol.activo and user_x_rol.rol.cerrar_proyecto:
                return True
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
        if user_x_rol.activo:
            lista_permisos = lista_permisos + ([Rol.CREAR_ITEM] if user_x_rol.rol.crear_item and Rol.CREAR_ITEM not in lista_permisos else []) + \
            ([Rol.MODIFICAR_ITEM] if user_x_rol.rol.modificar_item and Rol.MODIFICAR_ITEM not in lista_permisos else []) + \
            ([Rol.DESACTIVAR_ITEM] if user_x_rol.rol.desactivar_item and Rol.DESACTIVAR_ITEM not in lista_permisos else []) + \
            ([Rol.APROBAR_ITEM] if user_x_rol.rol.aprobar_item and Rol.APROBAR_ITEM not in lista_permisos else []) + \
            ([Rol.REVERSIONAR_ITEM] if user_x_rol.rol.reversionar_item and Rol.REVERSIONAR_ITEM not in lista_permisos else []) + \
            ([Rol.CREAR_RELACIONES_PH] if user_x_rol.rol.crear_relaciones_ph and Rol.CREAR_RELACIONES_PH not in lista_permisos else []) + \
            ([Rol.CREAR_RELACIONES_AS] if user_x_rol.rol.crear_relaciones_as and Rol.CREAR_RELACIONES_AS not in lista_permisos else []) + \
            ([Rol.BORRAR_RELACIONES] if user_x_rol.rol.borrar_relaciones and Rol.BORRAR_RELACIONES not in lista_permisos else []) + \
            ([Rol.VER_ITEM] if user_x_rol.rol.ver_item and Rol.VER_ITEM not in lista_permisos else []) + \
            ([Rol.CREAR_LINEA_BASE] if user_x_rol.rol.crear_linea_base and Rol.CREAR_LINEA_BASE not in lista_permisos else []) + \
            ([Rol.CERRAR_FASE] if user_x_rol.rol.cerrar_fase and Rol.CERRAR_FASE not in lista_permisos else []) + \
            ([Rol.CERRAR_PROYECTO] if user_x_rol.rol.cerrar_proyecto and Rol.CERRAR_PROYECTO not in lista_permisos else []) + \
            ([Rol.VER_PROYECTO] if user_x_rol.rol.ver_proyecto and Rol.VER_PROYECTO not in lista_permisos else []) + \
            ([Rol.SOLICITAR_RUPTURA_LB] if user_x_rol.rol.solicitar_ruptura_lb and Rol.SOLICITAR_RUPTURA_LB not in lista_permisos else [])
    return lista_permisos
