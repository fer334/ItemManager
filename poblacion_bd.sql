PGDMP     (    7                x         
   itemmanagerdb    10.12    12.4 S   �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    136328 
   itemmanagerdb    DATABASE        CREATE DATABASE itemmanagerdb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'es_PY.UTF-8' LC_CTYPE = 'es_PY.UTF-8';
    DROP DATABASE itemmanagerdb;
                postgres    false            �            1259    136489    administracion_fase    TABLE     �   CREATE TABLE public.administracion_fase (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    descripcion character varying(400),
    estado character varying(200) NOT NULL,
    proyecto_id integer NOT NULL
);
 '   DROP TABLE public.administracion_fase;
       public            postgres    false            �            1259    136487    administracion_fase_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_fase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.administracion_fase_id_seq;
       public          postgres    false    215            �           0    0    administracion_fase_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.administracion_fase_id_seq OWNED BY public.administracion_fase.id;
          public          postgres    false    214            �            1259    136599    administracion_fase_tipos_item    TABLE     �   CREATE TABLE public.administracion_fase_tipos_item (
    id integer NOT NULL,
    fase_id integer NOT NULL,
    tipoitem_id integer NOT NULL
);
 2   DROP TABLE public.administracion_fase_tipos_item;
       public            postgres    false            �            1259    136597 %   administracion_fase_tipos_item_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_fase_tipos_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 <   DROP SEQUENCE public.administracion_fase_tipos_item_id_seq;
       public          postgres    false    233            �           0    0 %   administracion_fase_tipos_item_id_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public.administracion_fase_tipos_item_id_seq OWNED BY public.administracion_fase_tipos_item.id;
          public          postgres    false    232            �            1259    136500     administracion_plantillaatributo    TABLE     �   CREATE TABLE public.administracion_plantillaatributo (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    tipo character varying(100) NOT NULL,
    es_requerido boolean NOT NULL,
    tipo_item_id integer NOT NULL
);
 4   DROP TABLE public.administracion_plantillaatributo;
       public            postgres    false            �            1259    136498 '   administracion_plantillaatributo_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_plantillaatributo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 >   DROP SEQUENCE public.administracion_plantillaatributo_id_seq;
       public          postgres    false    217            �           0    0 '   administracion_plantillaatributo_id_seq    SEQUENCE OWNED BY     s   ALTER SEQUENCE public.administracion_plantillaatributo_id_seq OWNED BY public.administracion_plantillaatributo.id;
          public          postgres    false    216            �            1259    136508    administracion_proyecto    TABLE     �  CREATE TABLE public.administracion_proyecto (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    fecha_inicio date NOT NULL,
    fecha_ejecucion timestamp with time zone,
    fecha_finalizado timestamp with time zone,
    fecha_cancelado timestamp with time zone,
    estado character varying(200) NOT NULL,
    numero_fases integer NOT NULL,
    cant_comite integer NOT NULL,
    gerente integer NOT NULL
);
 +   DROP TABLE public.administracion_proyecto;
       public            postgres    false            �            1259    136573    administracion_proyecto_comite    TABLE     �   CREATE TABLE public.administracion_proyecto_comite (
    id integer NOT NULL,
    proyecto_id integer NOT NULL,
    usuario_id integer NOT NULL
);
 2   DROP TABLE public.administracion_proyecto_comite;
       public            postgres    false            �            1259    136571 %   administracion_proyecto_comite_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_proyecto_comite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 <   DROP SEQUENCE public.administracion_proyecto_comite_id_seq;
       public          postgres    false    229            �           0    0 %   administracion_proyecto_comite_id_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public.administracion_proyecto_comite_id_seq OWNED BY public.administracion_proyecto_comite.id;
          public          postgres    false    228            �            1259    136506    administracion_proyecto_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_proyecto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.administracion_proyecto_id_seq;
       public          postgres    false    219            �           0    0    administracion_proyecto_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.administracion_proyecto_id_seq OWNED BY public.administracion_proyecto.id;
          public          postgres    false    218            �            1259    136581 %   administracion_proyecto_participantes    TABLE     �   CREATE TABLE public.administracion_proyecto_participantes (
    id integer NOT NULL,
    proyecto_id integer NOT NULL,
    usuario_id integer NOT NULL
);
 9   DROP TABLE public.administracion_proyecto_participantes;
       public            postgres    false            �            1259    136579 ,   administracion_proyecto_participantes_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_proyecto_participantes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 C   DROP SEQUENCE public.administracion_proyecto_participantes_id_seq;
       public          postgres    false    231            �           0    0 ,   administracion_proyecto_participantes_id_seq    SEQUENCE OWNED BY     }   ALTER SEQUENCE public.administracion_proyecto_participantes_id_seq OWNED BY public.administracion_proyecto_participantes.id;
          public          postgres    false    230            �            1259    136516    administracion_rol    TABLE     �  CREATE TABLE public.administracion_rol (
    id integer NOT NULL,
    nombre character varying(150) NOT NULL,
    crear_item boolean NOT NULL,
    modificar_item boolean NOT NULL,
    desactivar_item boolean NOT NULL,
    aprobar_item boolean NOT NULL,
    reversionar_item boolean NOT NULL,
    crear_relaciones_ph boolean NOT NULL,
    crear_relaciones_as boolean NOT NULL,
    borrar_relaciones boolean NOT NULL,
    activo boolean NOT NULL,
    proyecto_id integer
);
 &   DROP TABLE public.administracion_rol;
       public            postgres    false            �            1259    136514    administracion_rol_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_rol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 0   DROP SEQUENCE public.administracion_rol_id_seq;
       public          postgres    false    221            �           0    0    administracion_rol_id_seq    SEQUENCE OWNED BY     W   ALTER SEQUENCE public.administracion_rol_id_seq OWNED BY public.administracion_rol.id;
          public          postgres    false    220            �            1259    136524    administracion_tipoitem    TABLE     �   CREATE TABLE public.administracion_tipoitem (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    descripcion character varying(800) NOT NULL,
    prefijo character varying(5) NOT NULL
);
 +   DROP TABLE public.administracion_tipoitem;
       public            postgres    false            �            1259    136522    administracion_tipoitem_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_tipoitem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.administracion_tipoitem_id_seq;
       public          postgres    false    223            �           0    0    administracion_tipoitem_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.administracion_tipoitem_id_seq OWNED BY public.administracion_tipoitem.id;
          public          postgres    false    222            �            1259    136560     administracion_tipoitem_proyecto    TABLE     �   CREATE TABLE public.administracion_tipoitem_proyecto (
    id integer NOT NULL,
    tipoitem_id integer NOT NULL,
    proyecto_id integer NOT NULL
);
 4   DROP TABLE public.administracion_tipoitem_proyecto;
       public            postgres    false            �            1259    136558 '   administracion_tipoitem_proyecto_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_tipoitem_proyecto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 >   DROP SEQUENCE public.administracion_tipoitem_proyecto_id_seq;
       public          postgres    false    227            �           0    0 '   administracion_tipoitem_proyecto_id_seq    SEQUENCE OWNED BY     s   ALTER SEQUENCE public.administracion_tipoitem_proyecto_id_seq OWNED BY public.administracion_tipoitem_proyecto.id;
          public          postgres    false    226            �            1259    136535    administracion_usuarioxrol    TABLE     �   CREATE TABLE public.administracion_usuarioxrol (
    id integer NOT NULL,
    activo boolean NOT NULL,
    fase_id integer NOT NULL,
    rol_id integer NOT NULL,
    usuario_id integer NOT NULL
);
 .   DROP TABLE public.administracion_usuarioxrol;
       public            postgres    false            �            1259    136533 !   administracion_usuarioxrol_id_seq    SEQUENCE     �   CREATE SEQUENCE public.administracion_usuarioxrol_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 8   DROP SEQUENCE public.administracion_usuarioxrol_id_seq;
       public          postgres    false    225            �           0    0 !   administracion_usuarioxrol_id_seq    SEQUENCE OWNED BY     g   ALTER SEQUENCE public.administracion_usuarioxrol_id_seq OWNED BY public.administracion_usuarioxrol.id;
          public          postgres    false    224            �            1259    136360 
   auth_group    TABLE     f   CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);
    DROP TABLE public.auth_group;
       public            postgres    false            �            1259    136358    auth_group_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.auth_group_id_seq;
       public          postgres    false    203            �           0    0    auth_group_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;
          public          postgres    false    202            �            1259    136370    auth_group_permissions    TABLE     �   CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
 *   DROP TABLE public.auth_group_permissions;
       public            postgres    false            �            1259    136368    auth_group_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.auth_group_permissions_id_seq;
       public          postgres    false    205            �           0    0    auth_group_permissions_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;
          public          postgres    false    204            �            1259    136352    auth_permission    TABLE     �   CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
 #   DROP TABLE public.auth_permission;
       public            postgres    false            �            1259    136350    auth_permission_id_seq    SEQUENCE     �   CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.auth_permission_id_seq;
       public          postgres    false    201            �           0    0    auth_permission_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;
          public          postgres    false    200            �            1259    136803    configuracion_lineabase    TABLE     �   CREATE TABLE public.configuracion_lineabase (
    id integer NOT NULL,
    fecha_creacion date NOT NULL,
    tipo character varying(100) NOT NULL,
    estado character varying(100) NOT NULL,
    creador_id integer,
    fase_id integer NOT NULL
);
 +   DROP TABLE public.configuracion_lineabase;
       public            postgres    false            �            1259    136801    configuracion_lineabase_id_seq    SEQUENCE     �   CREATE SEQUENCE public.configuracion_lineabase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.configuracion_lineabase_id_seq;
       public          postgres    false    247            �           0    0    configuracion_lineabase_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.configuracion_lineabase_id_seq OWNED BY public.configuracion_lineabase.id;
          public          postgres    false    246            �            1259    136866    configuracion_lineabase_items    TABLE     �   CREATE TABLE public.configuracion_lineabase_items (
    id integer NOT NULL,
    lineabase_id integer NOT NULL,
    item_id integer NOT NULL
);
 1   DROP TABLE public.configuracion_lineabase_items;
       public            postgres    false            �            1259    136864 $   configuracion_lineabase_items_id_seq    SEQUENCE     �   CREATE SEQUENCE public.configuracion_lineabase_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.configuracion_lineabase_items_id_seq;
       public          postgres    false    255            �           0    0 $   configuracion_lineabase_items_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.configuracion_lineabase_items_id_seq OWNED BY public.configuracion_lineabase_items.id;
          public          postgres    false    254            �            1259    136811    configuracion_solicitud    TABLE        CREATE TABLE public.configuracion_solicitud (
    id integer NOT NULL,
    fecha_solicitud date NOT NULL,
    justificacion character varying(200) NOT NULL,
    solicitud_activa boolean NOT NULL,
    linea_base_id integer,
    solicitado_por_id integer
);
 +   DROP TABLE public.configuracion_solicitud;
       public            postgres    false            �            1259    136809    configuracion_solicitud_id_seq    SEQUENCE     �   CREATE SEQUENCE public.configuracion_solicitud_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 5   DROP SEQUENCE public.configuracion_solicitud_id_seq;
       public          postgres    false    249            �           0    0    configuracion_solicitud_id_seq    SEQUENCE OWNED BY     a   ALTER SEQUENCE public.configuracion_solicitud_id_seq OWNED BY public.configuracion_solicitud.id;
          public          postgres    false    248            �            1259    136838 )   configuracion_solicitud_items_a_modificar    TABLE     �   CREATE TABLE public.configuracion_solicitud_items_a_modificar (
    id integer NOT NULL,
    solicitud_id integer NOT NULL,
    item_id integer NOT NULL
);
 =   DROP TABLE public.configuracion_solicitud_items_a_modificar;
       public            postgres    false            �            1259    136836 0   configuracion_solicitud_items_a_modificar_id_seq    SEQUENCE     �   CREATE SEQUENCE public.configuracion_solicitud_items_a_modificar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 G   DROP SEQUENCE public.configuracion_solicitud_items_a_modificar_id_seq;
       public          postgres    false    253            �           0    0 0   configuracion_solicitud_items_a_modificar_id_seq    SEQUENCE OWNED BY     �   ALTER SEQUENCE public.configuracion_solicitud_items_a_modificar_id_seq OWNED BY public.configuracion_solicitud_items_a_modificar.id;
          public          postgres    false    252            �            1259    136819    configuracion_votoruptura    TABLE     �   CREATE TABLE public.configuracion_votoruptura (
    id integer NOT NULL,
    valor_voto boolean NOT NULL,
    fecha_voto date NOT NULL,
    solicitud_id integer NOT NULL,
    votante_id integer NOT NULL
);
 -   DROP TABLE public.configuracion_votoruptura;
       public            postgres    false            �            1259    136817     configuracion_votoruptura_id_seq    SEQUENCE     �   CREATE SEQUENCE public.configuracion_votoruptura_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.configuracion_votoruptura_id_seq;
       public          postgres    false    251            �           0    0     configuracion_votoruptura_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.configuracion_votoruptura_id_seq OWNED BY public.configuracion_votoruptura.id;
          public          postgres    false    250            �            1259    136712    desarrollo_atributoparticular    TABLE     �   CREATE TABLE public.desarrollo_atributoparticular (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    tipo character varying(100) NOT NULL,
    valor character varying(300) NOT NULL,
    item_id integer NOT NULL
);
 1   DROP TABLE public.desarrollo_atributoparticular;
       public            postgres    false            �            1259    136710 $   desarrollo_atributoparticular_id_seq    SEQUENCE     �   CREATE SEQUENCE public.desarrollo_atributoparticular_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ;   DROP SEQUENCE public.desarrollo_atributoparticular_id_seq;
       public          postgres    false    245            �           0    0 $   desarrollo_atributoparticular_id_seq    SEQUENCE OWNED BY     m   ALTER SEQUENCE public.desarrollo_atributoparticular_id_seq OWNED BY public.desarrollo_atributoparticular.id;
          public          postgres    false    244            �            1259    136667    desarrollo_item    TABLE     %  CREATE TABLE public.desarrollo_item (
    id integer NOT NULL,
    nombre character varying(200) NOT NULL,
    estado character varying(100) NOT NULL,
    numeracion integer NOT NULL,
    version integer NOT NULL,
    complejidad integer NOT NULL,
    descripcion character varying(200),
    id_version integer,
    fase_id integer,
    tipo_item_id integer NOT NULL,
    version_anterior_id integer,
    CONSTRAINT desarrollo_item_complejidad_check CHECK ((complejidad >= 0)),
    CONSTRAINT desarrollo_item_version_check CHECK ((version >= 0))
);
 #   DROP TABLE public.desarrollo_item;
       public            postgres    false            �            1259    136680    desarrollo_item_antecesores    TABLE     �   CREATE TABLE public.desarrollo_item_antecesores (
    id integer NOT NULL,
    from_item_id integer NOT NULL,
    to_item_id integer NOT NULL
);
 /   DROP TABLE public.desarrollo_item_antecesores;
       public            postgres    false            �            1259    136678 "   desarrollo_item_antecesores_id_seq    SEQUENCE     �   CREATE SEQUENCE public.desarrollo_item_antecesores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 9   DROP SEQUENCE public.desarrollo_item_antecesores_id_seq;
       public          postgres    false    237            �           0    0 "   desarrollo_item_antecesores_id_seq    SEQUENCE OWNED BY     i   ALTER SEQUENCE public.desarrollo_item_antecesores_id_seq OWNED BY public.desarrollo_item_antecesores.id;
          public          postgres    false    236            �            1259    136688    desarrollo_item_hijos    TABLE     �   CREATE TABLE public.desarrollo_item_hijos (
    id integer NOT NULL,
    from_item_id integer NOT NULL,
    to_item_id integer NOT NULL
);
 )   DROP TABLE public.desarrollo_item_hijos;
       public            postgres    false            �            1259    136686    desarrollo_item_hijos_id_seq    SEQUENCE     �   CREATE SEQUENCE public.desarrollo_item_hijos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.desarrollo_item_hijos_id_seq;
       public          postgres    false    239            �           0    0    desarrollo_item_hijos_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.desarrollo_item_hijos_id_seq OWNED BY public.desarrollo_item_hijos.id;
          public          postgres    false    238            �            1259    136665    desarrollo_item_id_seq    SEQUENCE     �   CREATE SEQUENCE public.desarrollo_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.desarrollo_item_id_seq;
       public          postgres    false    235            �           0    0    desarrollo_item_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.desarrollo_item_id_seq OWNED BY public.desarrollo_item.id;
          public          postgres    false    234            �            1259    136696    desarrollo_item_padres    TABLE     �   CREATE TABLE public.desarrollo_item_padres (
    id integer NOT NULL,
    from_item_id integer NOT NULL,
    to_item_id integer NOT NULL
);
 *   DROP TABLE public.desarrollo_item_padres;
       public            postgres    false            �            1259    136694    desarrollo_item_padres_id_seq    SEQUENCE     �   CREATE SEQUENCE public.desarrollo_item_padres_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.desarrollo_item_padres_id_seq;
       public          postgres    false    241            �           0    0    desarrollo_item_padres_id_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.desarrollo_item_padres_id_seq OWNED BY public.desarrollo_item_padres.id;
          public          postgres    false    240            �            1259    136704    desarrollo_item_sucesores    TABLE     �   CREATE TABLE public.desarrollo_item_sucesores (
    id integer NOT NULL,
    from_item_id integer NOT NULL,
    to_item_id integer NOT NULL
);
 -   DROP TABLE public.desarrollo_item_sucesores;
       public            postgres    false            �            1259    136702     desarrollo_item_sucesores_id_seq    SEQUENCE     �   CREATE SEQUENCE public.desarrollo_item_sucesores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.desarrollo_item_sucesores_id_seq;
       public          postgres    false    243            �           0    0     desarrollo_item_sucesores_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.desarrollo_item_sucesores_id_seq OWNED BY public.desarrollo_item_sucesores.id;
          public          postgres    false    242            �            1259    136465    django_admin_log    TABLE     �  CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
 $   DROP TABLE public.django_admin_log;
       public            postgres    false            �            1259    136463    django_admin_log_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.django_admin_log_id_seq;
       public          postgres    false    213            �           0    0    django_admin_log_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;
          public          postgres    false    212            �            1259    136342    django_content_type    TABLE     �   CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
 '   DROP TABLE public.django_content_type;
       public            postgres    false            �            1259    136340    django_content_type_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.django_content_type_id_seq;
       public          postgres    false    199            �           0    0    django_content_type_id_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;
          public          postgres    false    198            �            1259    136331    django_migrations    TABLE     �   CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);
 %   DROP TABLE public.django_migrations;
       public            postgres    false            �            1259    136329    django_migrations_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.django_migrations_id_seq;
       public          postgres    false    197            �           0    0    django_migrations_id_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;
          public          postgres    false    196                        1259    136905    django_session    TABLE     �   CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);
 "   DROP TABLE public.django_session;
       public            postgres    false                       1259    136917    django_site    TABLE     �   CREATE TABLE public.django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);
    DROP TABLE public.django_site;
       public            postgres    false                       1259    136915    django_site_id_seq    SEQUENCE     �   CREATE SEQUENCE public.django_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.django_site_id_seq;
       public          postgres    false    258            �           0    0    django_site_id_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.django_site_id_seq OWNED BY public.django_site.id;
          public          postgres    false    257            �            1259    136404 
   login_usuario    TABLE     X  CREATE TABLE public.login_usuario (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    "localId" character varying(200) NOT NULL,
    id_token character varying(100),
    is_gerente boolean NOT NULL
);
 !   DROP TABLE public.login_usuario;
       public            postgres    false            �            1259    136419    login_usuario_groups    TABLE     �   CREATE TABLE public.login_usuario_groups (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    group_id integer NOT NULL
);
 (   DROP TABLE public.login_usuario_groups;
       public            postgres    false            �            1259    136417    login_usuario_groups_id_seq    SEQUENCE     �   CREATE SEQUENCE public.login_usuario_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 2   DROP SEQUENCE public.login_usuario_groups_id_seq;
       public          postgres    false    209            �           0    0    login_usuario_groups_id_seq    SEQUENCE OWNED BY     [   ALTER SEQUENCE public.login_usuario_groups_id_seq OWNED BY public.login_usuario_groups.id;
          public          postgres    false    208            �            1259    136402    login_usuario_id_seq    SEQUENCE     �   CREATE SEQUENCE public.login_usuario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.login_usuario_id_seq;
       public          postgres    false    207            �           0    0    login_usuario_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.login_usuario_id_seq OWNED BY public.login_usuario.id;
          public          postgres    false    206            �            1259    136427    login_usuario_user_permissions    TABLE     �   CREATE TABLE public.login_usuario_user_permissions (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    permission_id integer NOT NULL
);
 2   DROP TABLE public.login_usuario_user_permissions;
       public            postgres    false            �            1259    136425 %   login_usuario_user_permissions_id_seq    SEQUENCE     �   CREATE SEQUENCE public.login_usuario_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 <   DROP SEQUENCE public.login_usuario_user_permissions_id_seq;
       public          postgres    false    211            �           0    0 %   login_usuario_user_permissions_id_seq    SEQUENCE OWNED BY     o   ALTER SEQUENCE public.login_usuario_user_permissions_id_seq OWNED BY public.login_usuario_user_permissions.id;
          public          postgres    false    210            <           2604    136492    administracion_fase id    DEFAULT     �   ALTER TABLE ONLY public.administracion_fase ALTER COLUMN id SET DEFAULT nextval('public.administracion_fase_id_seq'::regclass);
 E   ALTER TABLE public.administracion_fase ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    215    214    215            E           2604    136602 !   administracion_fase_tipos_item id    DEFAULT     �   ALTER TABLE ONLY public.administracion_fase_tipos_item ALTER COLUMN id SET DEFAULT nextval('public.administracion_fase_tipos_item_id_seq'::regclass);
 P   ALTER TABLE public.administracion_fase_tipos_item ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    233    232    233            =           2604    136503 #   administracion_plantillaatributo id    DEFAULT     �   ALTER TABLE ONLY public.administracion_plantillaatributo ALTER COLUMN id SET DEFAULT nextval('public.administracion_plantillaatributo_id_seq'::regclass);
 R   ALTER TABLE public.administracion_plantillaatributo ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    217    216    217            >           2604    136511    administracion_proyecto id    DEFAULT     �   ALTER TABLE ONLY public.administracion_proyecto ALTER COLUMN id SET DEFAULT nextval('public.administracion_proyecto_id_seq'::regclass);
 I   ALTER TABLE public.administracion_proyecto ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    219    218    219            C           2604    136576 !   administracion_proyecto_comite id    DEFAULT     �   ALTER TABLE ONLY public.administracion_proyecto_comite ALTER COLUMN id SET DEFAULT nextval('public.administracion_proyecto_comite_id_seq'::regclass);
 P   ALTER TABLE public.administracion_proyecto_comite ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    229    228    229            D           2604    136584 (   administracion_proyecto_participantes id    DEFAULT     �   ALTER TABLE ONLY public.administracion_proyecto_participantes ALTER COLUMN id SET DEFAULT nextval('public.administracion_proyecto_participantes_id_seq'::regclass);
 W   ALTER TABLE public.administracion_proyecto_participantes ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    230    231    231            ?           2604    136519    administracion_rol id    DEFAULT     ~   ALTER TABLE ONLY public.administracion_rol ALTER COLUMN id SET DEFAULT nextval('public.administracion_rol_id_seq'::regclass);
 D   ALTER TABLE public.administracion_rol ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    220    221    221            @           2604    136527    administracion_tipoitem id    DEFAULT     �   ALTER TABLE ONLY public.administracion_tipoitem ALTER COLUMN id SET DEFAULT nextval('public.administracion_tipoitem_id_seq'::regclass);
 I   ALTER TABLE public.administracion_tipoitem ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    222    223    223            B           2604    136563 #   administracion_tipoitem_proyecto id    DEFAULT     �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto ALTER COLUMN id SET DEFAULT nextval('public.administracion_tipoitem_proyecto_id_seq'::regclass);
 R   ALTER TABLE public.administracion_tipoitem_proyecto ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    226    227    227            A           2604    136538    administracion_usuarioxrol id    DEFAULT     �   ALTER TABLE ONLY public.administracion_usuarioxrol ALTER COLUMN id SET DEFAULT nextval('public.administracion_usuarioxrol_id_seq'::regclass);
 L   ALTER TABLE public.administracion_usuarioxrol ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    224    225    225            5           2604    136363 
   auth_group id    DEFAULT     n   ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);
 <   ALTER TABLE public.auth_group ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    203    202    203            6           2604    136373    auth_group_permissions id    DEFAULT     �   ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);
 H   ALTER TABLE public.auth_group_permissions ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    205    204    205            4           2604    136355    auth_permission id    DEFAULT     x   ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);
 A   ALTER TABLE public.auth_permission ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    201    200    201            N           2604    136806    configuracion_lineabase id    DEFAULT     �   ALTER TABLE ONLY public.configuracion_lineabase ALTER COLUMN id SET DEFAULT nextval('public.configuracion_lineabase_id_seq'::regclass);
 I   ALTER TABLE public.configuracion_lineabase ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    247    246    247            R           2604    136869     configuracion_lineabase_items id    DEFAULT     �   ALTER TABLE ONLY public.configuracion_lineabase_items ALTER COLUMN id SET DEFAULT nextval('public.configuracion_lineabase_items_id_seq'::regclass);
 O   ALTER TABLE public.configuracion_lineabase_items ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    255    254    255            O           2604    136814    configuracion_solicitud id    DEFAULT     �   ALTER TABLE ONLY public.configuracion_solicitud ALTER COLUMN id SET DEFAULT nextval('public.configuracion_solicitud_id_seq'::regclass);
 I   ALTER TABLE public.configuracion_solicitud ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    248    249    249            Q           2604    136841 ,   configuracion_solicitud_items_a_modificar id    DEFAULT     �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar ALTER COLUMN id SET DEFAULT nextval('public.configuracion_solicitud_items_a_modificar_id_seq'::regclass);
 [   ALTER TABLE public.configuracion_solicitud_items_a_modificar ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    253    252    253            P           2604    136822    configuracion_votoruptura id    DEFAULT     �   ALTER TABLE ONLY public.configuracion_votoruptura ALTER COLUMN id SET DEFAULT nextval('public.configuracion_votoruptura_id_seq'::regclass);
 K   ALTER TABLE public.configuracion_votoruptura ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    251    250    251            M           2604    136715     desarrollo_atributoparticular id    DEFAULT     �   ALTER TABLE ONLY public.desarrollo_atributoparticular ALTER COLUMN id SET DEFAULT nextval('public.desarrollo_atributoparticular_id_seq'::regclass);
 O   ALTER TABLE public.desarrollo_atributoparticular ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    245    244    245            F           2604    136670    desarrollo_item id    DEFAULT     x   ALTER TABLE ONLY public.desarrollo_item ALTER COLUMN id SET DEFAULT nextval('public.desarrollo_item_id_seq'::regclass);
 A   ALTER TABLE public.desarrollo_item ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    234    235    235            I           2604    136683    desarrollo_item_antecesores id    DEFAULT     �   ALTER TABLE ONLY public.desarrollo_item_antecesores ALTER COLUMN id SET DEFAULT nextval('public.desarrollo_item_antecesores_id_seq'::regclass);
 M   ALTER TABLE public.desarrollo_item_antecesores ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    237    236    237            J           2604    136691    desarrollo_item_hijos id    DEFAULT     �   ALTER TABLE ONLY public.desarrollo_item_hijos ALTER COLUMN id SET DEFAULT nextval('public.desarrollo_item_hijos_id_seq'::regclass);
 G   ALTER TABLE public.desarrollo_item_hijos ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    238    239    239            K           2604    136699    desarrollo_item_padres id    DEFAULT     �   ALTER TABLE ONLY public.desarrollo_item_padres ALTER COLUMN id SET DEFAULT nextval('public.desarrollo_item_padres_id_seq'::regclass);
 H   ALTER TABLE public.desarrollo_item_padres ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    241    240    241            L           2604    136707    desarrollo_item_sucesores id    DEFAULT     �   ALTER TABLE ONLY public.desarrollo_item_sucesores ALTER COLUMN id SET DEFAULT nextval('public.desarrollo_item_sucesores_id_seq'::regclass);
 K   ALTER TABLE public.desarrollo_item_sucesores ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    243    242    243            :           2604    136468    django_admin_log id    DEFAULT     z   ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);
 B   ALTER TABLE public.django_admin_log ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    213    212    213            3           2604    136345    django_content_type id    DEFAULT     �   ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);
 E   ALTER TABLE public.django_content_type ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    199    198    199            2           2604    136334    django_migrations id    DEFAULT     |   ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);
 C   ALTER TABLE public.django_migrations ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    196    197    197            S           2604    136920    django_site id    DEFAULT     p   ALTER TABLE ONLY public.django_site ALTER COLUMN id SET DEFAULT nextval('public.django_site_id_seq'::regclass);
 =   ALTER TABLE public.django_site ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    257    258    258            7           2604    136407    login_usuario id    DEFAULT     t   ALTER TABLE ONLY public.login_usuario ALTER COLUMN id SET DEFAULT nextval('public.login_usuario_id_seq'::regclass);
 ?   ALTER TABLE public.login_usuario ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    206    207    207            8           2604    136422    login_usuario_groups id    DEFAULT     �   ALTER TABLE ONLY public.login_usuario_groups ALTER COLUMN id SET DEFAULT nextval('public.login_usuario_groups_id_seq'::regclass);
 F   ALTER TABLE public.login_usuario_groups ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    208    209    209            9           2604    136430 !   login_usuario_user_permissions id    DEFAULT     �   ALTER TABLE ONLY public.login_usuario_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.login_usuario_user_permissions_id_seq'::regclass);
 P   ALTER TABLE public.login_usuario_user_permissions ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    211    210    211            �          0    136489    administracion_fase 
   TABLE DATA           [   COPY public.administracion_fase (id, nombre, descripcion, estado, proyecto_id) FROM stdin;
    public          postgres    false    215   7�      �          0    136599    administracion_fase_tipos_item 
   TABLE DATA           R   COPY public.administracion_fase_tipos_item (id, fase_id, tipoitem_id) FROM stdin;
    public          postgres    false    233   ��      �          0    136500     administracion_plantillaatributo 
   TABLE DATA           h   COPY public.administracion_plantillaatributo (id, nombre, tipo, es_requerido, tipo_item_id) FROM stdin;
    public          postgres    false    217   ��      �          0    136508    administracion_proyecto 
   TABLE DATA           �   COPY public.administracion_proyecto (id, nombre, fecha_inicio, fecha_ejecucion, fecha_finalizado, fecha_cancelado, estado, numero_fases, cant_comite, gerente) FROM stdin;
    public          postgres    false    219   ��      �          0    136573    administracion_proyecto_comite 
   TABLE DATA           U   COPY public.administracion_proyecto_comite (id, proyecto_id, usuario_id) FROM stdin;
    public          postgres    false    229   ��      �          0    136581 %   administracion_proyecto_participantes 
   TABLE DATA           \   COPY public.administracion_proyecto_participantes (id, proyecto_id, usuario_id) FROM stdin;
    public          postgres    false    231   ��      �          0    136516    administracion_rol 
   TABLE DATA           �   COPY public.administracion_rol (id, nombre, crear_item, modificar_item, desactivar_item, aprobar_item, reversionar_item, crear_relaciones_ph, crear_relaciones_as, borrar_relaciones, activo, proyecto_id) FROM stdin;
    public          postgres    false    221   �      �          0    136524    administracion_tipoitem 
   TABLE DATA           S   COPY public.administracion_tipoitem (id, nombre, descripcion, prefijo) FROM stdin;
    public          postgres    false    223   (�      �          0    136560     administracion_tipoitem_proyecto 
   TABLE DATA           X   COPY public.administracion_tipoitem_proyecto (id, tipoitem_id, proyecto_id) FROM stdin;
    public          postgres    false    227   ��      �          0    136535    administracion_usuarioxrol 
   TABLE DATA           ]   COPY public.administracion_usuarioxrol (id, activo, fase_id, rol_id, usuario_id) FROM stdin;
    public          postgres    false    225   �      �          0    136360 
   auth_group 
   TABLE DATA           .   COPY public.auth_group (id, name) FROM stdin;
    public          postgres    false    203    �      �          0    136370    auth_group_permissions 
   TABLE DATA           M   COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
    public          postgres    false    205   =�      �          0    136352    auth_permission 
   TABLE DATA           N   COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
    public          postgres    false    201   Z�      �          0    136803    configuracion_lineabase 
   TABLE DATA           h   COPY public.configuracion_lineabase (id, fecha_creacion, tipo, estado, creador_id, fase_id) FROM stdin;
    public          postgres    false    247   :�      �          0    136866    configuracion_lineabase_items 
   TABLE DATA           R   COPY public.configuracion_lineabase_items (id, lineabase_id, item_id) FROM stdin;
    public          postgres    false    255   x�      �          0    136811    configuracion_solicitud 
   TABLE DATA           �   COPY public.configuracion_solicitud (id, fecha_solicitud, justificacion, solicitud_activa, linea_base_id, solicitado_por_id) FROM stdin;
    public          postgres    false    249   ��      �          0    136838 )   configuracion_solicitud_items_a_modificar 
   TABLE DATA           ^   COPY public.configuracion_solicitud_items_a_modificar (id, solicitud_id, item_id) FROM stdin;
    public          postgres    false    253   ��      �          0    136819    configuracion_votoruptura 
   TABLE DATA           i   COPY public.configuracion_votoruptura (id, valor_voto, fecha_voto, solicitud_id, votante_id) FROM stdin;
    public          postgres    false    251   ��      �          0    136712    desarrollo_atributoparticular 
   TABLE DATA           Y   COPY public.desarrollo_atributoparticular (id, nombre, tipo, valor, item_id) FROM stdin;
    public          postgres    false    245   ��      �          0    136667    desarrollo_item 
   TABLE DATA           �   COPY public.desarrollo_item (id, nombre, estado, numeracion, version, complejidad, descripcion, id_version, fase_id, tipo_item_id, version_anterior_id) FROM stdin;
    public          postgres    false    235   P�      �          0    136680    desarrollo_item_antecesores 
   TABLE DATA           S   COPY public.desarrollo_item_antecesores (id, from_item_id, to_item_id) FROM stdin;
    public          postgres    false    237   ��      �          0    136688    desarrollo_item_hijos 
   TABLE DATA           M   COPY public.desarrollo_item_hijos (id, from_item_id, to_item_id) FROM stdin;
    public          postgres    false    239   ��      �          0    136696    desarrollo_item_padres 
   TABLE DATA           N   COPY public.desarrollo_item_padres (id, from_item_id, to_item_id) FROM stdin;
    public          postgres    false    241   ��      �          0    136704    desarrollo_item_sucesores 
   TABLE DATA           Q   COPY public.desarrollo_item_sucesores (id, from_item_id, to_item_id) FROM stdin;
    public          postgres    false    243   �      �          0    136465    django_admin_log 
   TABLE DATA           �   COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
    public          postgres    false    213   Q�      �          0    136342    django_content_type 
   TABLE DATA           C   COPY public.django_content_type (id, app_label, model) FROM stdin;
    public          postgres    false    199   n�      �          0    136331    django_migrations 
   TABLE DATA           C   COPY public.django_migrations (id, app, name, applied) FROM stdin;
    public          postgres    false    197   Q�      �          0    136905    django_session 
   TABLE DATA           P   COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
    public          postgres    false    256   ��      �          0    136917    django_site 
   TABLE DATA           7   COPY public.django_site (id, domain, name) FROM stdin;
    public          postgres    false    258   �       �          0    136404 
   login_usuario 
   TABLE DATA           �   COPY public.login_usuario (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email, "localId", id_token, is_gerente) FROM stdin;
    public          postgres    false    207   �       �          0    136419    login_usuario_groups 
   TABLE DATA           H   COPY public.login_usuario_groups (id, usuario_id, group_id) FROM stdin;
    public          postgres    false    209   ?      �          0    136427    login_usuario_user_permissions 
   TABLE DATA           W   COPY public.login_usuario_user_permissions (id, usuario_id, permission_id) FROM stdin;
    public          postgres    false    211   \      �           0    0    administracion_fase_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.administracion_fase_id_seq', 9, true);
          public          postgres    false    214            �           0    0 %   administracion_fase_tipos_item_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.administracion_fase_tipos_item_id_seq', 3, true);
          public          postgres    false    232            �           0    0 '   administracion_plantillaatributo_id_seq    SEQUENCE SET     U   SELECT pg_catalog.setval('public.administracion_plantillaatributo_id_seq', 1, true);
          public          postgres    false    216            �           0    0 %   administracion_proyecto_comite_id_seq    SEQUENCE SET     S   SELECT pg_catalog.setval('public.administracion_proyecto_comite_id_seq', 6, true);
          public          postgres    false    228            �           0    0    administracion_proyecto_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.administracion_proyecto_id_seq', 3, true);
          public          postgres    false    218            �           0    0 ,   administracion_proyecto_participantes_id_seq    SEQUENCE SET     Z   SELECT pg_catalog.setval('public.administracion_proyecto_participantes_id_seq', 9, true);
          public          postgres    false    230            �           0    0    administracion_rol_id_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.administracion_rol_id_seq', 1, false);
          public          postgres    false    220            �           0    0    administracion_tipoitem_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.administracion_tipoitem_id_seq', 3, true);
          public          postgres    false    222            �           0    0 '   administracion_tipoitem_proyecto_id_seq    SEQUENCE SET     U   SELECT pg_catalog.setval('public.administracion_tipoitem_proyecto_id_seq', 6, true);
          public          postgres    false    226             
           0    0 !   administracion_usuarioxrol_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.administracion_usuarioxrol_id_seq', 1, false);
          public          postgres    false    224            
           0    0    auth_group_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);
          public          postgres    false    202            
           0    0    auth_group_permissions_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);
          public          postgres    false    204            
           0    0    auth_permission_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.auth_permission_id_seq', 72, true);
          public          postgres    false    200            
           0    0    configuracion_lineabase_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.configuracion_lineabase_id_seq', 1, true);
          public          postgres    false    246            
           0    0 $   configuracion_lineabase_items_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.configuracion_lineabase_items_id_seq', 2, true);
          public          postgres    false    254            
           0    0    configuracion_solicitud_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.configuracion_solicitud_id_seq', 1, false);
          public          postgres    false    248            
           0    0 0   configuracion_solicitud_items_a_modificar_id_seq    SEQUENCE SET     _   SELECT pg_catalog.setval('public.configuracion_solicitud_items_a_modificar_id_seq', 1, false);
          public          postgres    false    252            
           0    0     configuracion_votoruptura_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.configuracion_votoruptura_id_seq', 1, false);
          public          postgres    false    250            	
           0    0 $   desarrollo_atributoparticular_id_seq    SEQUENCE SET     R   SELECT pg_catalog.setval('public.desarrollo_atributoparticular_id_seq', 4, true);
          public          postgres    false    244            

           0    0 "   desarrollo_item_antecesores_id_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.desarrollo_item_antecesores_id_seq', 8, true);
          public          postgres    false    236            
           0    0    desarrollo_item_hijos_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.desarrollo_item_hijos_id_seq', 1, false);
          public          postgres    false    238            
           0    0    desarrollo_item_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.desarrollo_item_id_seq', 14, true);
          public          postgres    false    234            

           0    0    desarrollo_item_padres_id_seq    SEQUENCE SET     L   SELECT pg_catalog.setval('public.desarrollo_item_padres_id_seq', 1, false);
          public          postgres    false    240            
           0    0     desarrollo_item_sucesores_id_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.desarrollo_item_sucesores_id_seq', 5, true);
          public          postgres    false    242            
           0    0    django_admin_log_id_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);
          public          postgres    false    212            
           0    0    django_content_type_id_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.django_content_type_id_seq', 18, true);
          public          postgres    false    198            
           0    0    django_migrations_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.django_migrations_id_seq', 26, true);
          public          postgres    false    196            
           0    0    django_site_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);
          public          postgres    false    257            
           0    0    login_usuario_groups_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.login_usuario_groups_id_seq', 1, false);
          public          postgres    false    208            
           0    0    login_usuario_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.login_usuario_id_seq', 5, true);
          public          postgres    false    206            
           0    0 %   login_usuario_user_permissions_id_seq    SEQUENCE SET     T   SELECT pg_catalog.setval('public.login_usuario_user_permissions_id_seq', 1, false);
          public          postgres    false    210            �           2606    136497 ,   administracion_fase administracion_fase_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.administracion_fase
    ADD CONSTRAINT administracion_fase_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.administracion_fase DROP CONSTRAINT administracion_fase_pkey;
       public            postgres    false    215            �           2606    136652 Y   administracion_fase_tipos_item administracion_fase_tipo_fase_id_tipoitem_id_ceefa627_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_fase_tipos_item
    ADD CONSTRAINT administracion_fase_tipo_fase_id_tipoitem_id_ceefa627_uniq UNIQUE (fase_id, tipoitem_id);
 �   ALTER TABLE ONLY public.administracion_fase_tipos_item DROP CONSTRAINT administracion_fase_tipo_fase_id_tipoitem_id_ceefa627_uniq;
       public            postgres    false    233    233            �           2606    136604 B   administracion_fase_tipos_item administracion_fase_tipos_item_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_fase_tipos_item
    ADD CONSTRAINT administracion_fase_tipos_item_pkey PRIMARY KEY (id);
 l   ALTER TABLE ONLY public.administracion_fase_tipos_item DROP CONSTRAINT administracion_fase_tipos_item_pkey;
       public            postgres    false    233            �           2606    136505 F   administracion_plantillaatributo administracion_plantillaatributo_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_plantillaatributo
    ADD CONSTRAINT administracion_plantillaatributo_pkey PRIMARY KEY (id);
 p   ALTER TABLE ONLY public.administracion_plantillaatributo DROP CONSTRAINT administracion_plantillaatributo_pkey;
       public            postgres    false    217            �           2606    136622 \   administracion_proyecto_comite administracion_proyecto__proyecto_id_usuario_id_0a62efc1_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_comite
    ADD CONSTRAINT administracion_proyecto__proyecto_id_usuario_id_0a62efc1_uniq UNIQUE (proyecto_id, usuario_id);
 �   ALTER TABLE ONLY public.administracion_proyecto_comite DROP CONSTRAINT administracion_proyecto__proyecto_id_usuario_id_0a62efc1_uniq;
       public            postgres    false    229    229            �           2606    136636 c   administracion_proyecto_participantes administracion_proyecto__proyecto_id_usuario_id_5b51c199_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_participantes
    ADD CONSTRAINT administracion_proyecto__proyecto_id_usuario_id_5b51c199_uniq UNIQUE (proyecto_id, usuario_id);
 �   ALTER TABLE ONLY public.administracion_proyecto_participantes DROP CONSTRAINT administracion_proyecto__proyecto_id_usuario_id_5b51c199_uniq;
       public            postgres    false    231    231            �           2606    136578 B   administracion_proyecto_comite administracion_proyecto_comite_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_comite
    ADD CONSTRAINT administracion_proyecto_comite_pkey PRIMARY KEY (id);
 l   ALTER TABLE ONLY public.administracion_proyecto_comite DROP CONSTRAINT administracion_proyecto_comite_pkey;
       public            postgres    false    229            �           2606    136586 P   administracion_proyecto_participantes administracion_proyecto_participantes_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_participantes
    ADD CONSTRAINT administracion_proyecto_participantes_pkey PRIMARY KEY (id);
 z   ALTER TABLE ONLY public.administracion_proyecto_participantes DROP CONSTRAINT administracion_proyecto_participantes_pkey;
       public            postgres    false    231            �           2606    136513 4   administracion_proyecto administracion_proyecto_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.administracion_proyecto
    ADD CONSTRAINT administracion_proyecto_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.administracion_proyecto DROP CONSTRAINT administracion_proyecto_pkey;
       public            postgres    false    219            �           2606    136521 *   administracion_rol administracion_rol_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.administracion_rol
    ADD CONSTRAINT administracion_rol_pkey PRIMARY KEY (id);
 T   ALTER TABLE ONLY public.administracion_rol DROP CONSTRAINT administracion_rol_pkey;
       public            postgres    false    221            �           2606    136607 _   administracion_tipoitem_proyecto administracion_tipoitem__tipoitem_id_proyecto_id_3492373a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto
    ADD CONSTRAINT administracion_tipoitem__tipoitem_id_proyecto_id_3492373a_uniq UNIQUE (tipoitem_id, proyecto_id);
 �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto DROP CONSTRAINT administracion_tipoitem__tipoitem_id_proyecto_id_3492373a_uniq;
       public            postgres    false    227    227            �           2606    136532 4   administracion_tipoitem administracion_tipoitem_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.administracion_tipoitem
    ADD CONSTRAINT administracion_tipoitem_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.administracion_tipoitem DROP CONSTRAINT administracion_tipoitem_pkey;
       public            postgres    false    223            �           2606    136565 F   administracion_tipoitem_proyecto administracion_tipoitem_proyecto_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto
    ADD CONSTRAINT administracion_tipoitem_proyecto_pkey PRIMARY KEY (id);
 p   ALTER TABLE ONLY public.administracion_tipoitem_proyecto DROP CONSTRAINT administracion_tipoitem_proyecto_pkey;
       public            postgres    false    227            �           2606    136540 :   administracion_usuarioxrol administracion_usuarioxrol_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.administracion_usuarioxrol
    ADD CONSTRAINT administracion_usuarioxrol_pkey PRIMARY KEY (id);
 d   ALTER TABLE ONLY public.administracion_usuarioxrol DROP CONSTRAINT administracion_usuarioxrol_pkey;
       public            postgres    false    225            a           2606    136400    auth_group auth_group_name_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);
 H   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_name_key;
       public            postgres    false    203            f           2606    136386 R   auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);
 |   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
       public            postgres    false    205    205            i           2606    136375 2   auth_group_permissions auth_group_permissions_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_pkey;
       public            postgres    false    205            c           2606    136365    auth_group auth_group_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.auth_group DROP CONSTRAINT auth_group_pkey;
       public            postgres    false    203            \           2606    136377 F   auth_permission auth_permission_content_type_id_codename_01ab375a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);
 p   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq;
       public            postgres    false    201    201            ^           2606    136357 $   auth_permission auth_permission_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_pkey;
       public            postgres    false    201            �           2606    136892 Y   configuracion_lineabase_items configuracion_lineabase__lineabase_id_item_id_18404c05_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_lineabase_items
    ADD CONSTRAINT configuracion_lineabase__lineabase_id_item_id_18404c05_uniq UNIQUE (lineabase_id, item_id);
 �   ALTER TABLE ONLY public.configuracion_lineabase_items DROP CONSTRAINT configuracion_lineabase__lineabase_id_item_id_18404c05_uniq;
       public            postgres    false    255    255            �           2606    136871 @   configuracion_lineabase_items configuracion_lineabase_items_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public.configuracion_lineabase_items
    ADD CONSTRAINT configuracion_lineabase_items_pkey PRIMARY KEY (id);
 j   ALTER TABLE ONLY public.configuracion_lineabase_items DROP CONSTRAINT configuracion_lineabase_items_pkey;
       public            postgres    false    255            �           2606    136808 4   configuracion_lineabase configuracion_lineabase_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.configuracion_lineabase
    ADD CONSTRAINT configuracion_lineabase_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.configuracion_lineabase DROP CONSTRAINT configuracion_lineabase_pkey;
       public            postgres    false    247            �           2606    136874 e   configuracion_solicitud_items_a_modificar configuracion_solicitud__solicitud_id_item_id_cd8a4bdb_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar
    ADD CONSTRAINT configuracion_solicitud__solicitud_id_item_id_cd8a4bdb_uniq UNIQUE (solicitud_id, item_id);
 �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar DROP CONSTRAINT configuracion_solicitud__solicitud_id_item_id_cd8a4bdb_uniq;
       public            postgres    false    253    253            �           2606    136843 X   configuracion_solicitud_items_a_modificar configuracion_solicitud_items_a_modificar_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar
    ADD CONSTRAINT configuracion_solicitud_items_a_modificar_pkey PRIMARY KEY (id);
 �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar DROP CONSTRAINT configuracion_solicitud_items_a_modificar_pkey;
       public            postgres    false    253            �           2606    136816 4   configuracion_solicitud configuracion_solicitud_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.configuracion_solicitud
    ADD CONSTRAINT configuracion_solicitud_pkey PRIMARY KEY (id);
 ^   ALTER TABLE ONLY public.configuracion_solicitud DROP CONSTRAINT configuracion_solicitud_pkey;
       public            postgres    false    249            �           2606    136824 8   configuracion_votoruptura configuracion_votoruptura_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.configuracion_votoruptura
    ADD CONSTRAINT configuracion_votoruptura_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY public.configuracion_votoruptura DROP CONSTRAINT configuracion_votoruptura_pkey;
       public            postgres    false    251            �           2606    136720 @   desarrollo_atributoparticular desarrollo_atributoparticular_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public.desarrollo_atributoparticular
    ADD CONSTRAINT desarrollo_atributoparticular_pkey PRIMARY KEY (id);
 j   ALTER TABLE ONLY public.desarrollo_atributoparticular DROP CONSTRAINT desarrollo_atributoparticular_pkey;
       public            postgres    false    245            �           2606    136740 Z   desarrollo_item_antecesores desarrollo_item_anteceso_from_item_id_to_item_id_385a6480_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_antecesores
    ADD CONSTRAINT desarrollo_item_anteceso_from_item_id_to_item_id_385a6480_uniq UNIQUE (from_item_id, to_item_id);
 �   ALTER TABLE ONLY public.desarrollo_item_antecesores DROP CONSTRAINT desarrollo_item_anteceso_from_item_id_to_item_id_385a6480_uniq;
       public            postgres    false    237    237            �           2606    136685 <   desarrollo_item_antecesores desarrollo_item_antecesores_pkey 
   CONSTRAINT     z   ALTER TABLE ONLY public.desarrollo_item_antecesores
    ADD CONSTRAINT desarrollo_item_antecesores_pkey PRIMARY KEY (id);
 f   ALTER TABLE ONLY public.desarrollo_item_antecesores DROP CONSTRAINT desarrollo_item_antecesores_pkey;
       public            postgres    false    237            �           2606    136754 Q   desarrollo_item_hijos desarrollo_item_hijos_from_item_id_to_item_id_ede29e88_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_hijos
    ADD CONSTRAINT desarrollo_item_hijos_from_item_id_to_item_id_ede29e88_uniq UNIQUE (from_item_id, to_item_id);
 {   ALTER TABLE ONLY public.desarrollo_item_hijos DROP CONSTRAINT desarrollo_item_hijos_from_item_id_to_item_id_ede29e88_uniq;
       public            postgres    false    239    239            �           2606    136693 0   desarrollo_item_hijos desarrollo_item_hijos_pkey 
   CONSTRAINT     n   ALTER TABLE ONLY public.desarrollo_item_hijos
    ADD CONSTRAINT desarrollo_item_hijos_pkey PRIMARY KEY (id);
 Z   ALTER TABLE ONLY public.desarrollo_item_hijos DROP CONSTRAINT desarrollo_item_hijos_pkey;
       public            postgres    false    239            �           2606    136768 S   desarrollo_item_padres desarrollo_item_padres_from_item_id_to_item_id_c457066a_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_padres
    ADD CONSTRAINT desarrollo_item_padres_from_item_id_to_item_id_c457066a_uniq UNIQUE (from_item_id, to_item_id);
 }   ALTER TABLE ONLY public.desarrollo_item_padres DROP CONSTRAINT desarrollo_item_padres_from_item_id_to_item_id_c457066a_uniq;
       public            postgres    false    241    241            �           2606    136701 2   desarrollo_item_padres desarrollo_item_padres_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.desarrollo_item_padres
    ADD CONSTRAINT desarrollo_item_padres_pkey PRIMARY KEY (id);
 \   ALTER TABLE ONLY public.desarrollo_item_padres DROP CONSTRAINT desarrollo_item_padres_pkey;
       public            postgres    false    241            �           2606    136677 $   desarrollo_item desarrollo_item_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.desarrollo_item
    ADD CONSTRAINT desarrollo_item_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.desarrollo_item DROP CONSTRAINT desarrollo_item_pkey;
       public            postgres    false    235            �           2606    136782 Y   desarrollo_item_sucesores desarrollo_item_sucesores_from_item_id_to_item_id_ae4eea69_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_sucesores
    ADD CONSTRAINT desarrollo_item_sucesores_from_item_id_to_item_id_ae4eea69_uniq UNIQUE (from_item_id, to_item_id);
 �   ALTER TABLE ONLY public.desarrollo_item_sucesores DROP CONSTRAINT desarrollo_item_sucesores_from_item_id_to_item_id_ae4eea69_uniq;
       public            postgres    false    243    243            �           2606    136709 8   desarrollo_item_sucesores desarrollo_item_sucesores_pkey 
   CONSTRAINT     v   ALTER TABLE ONLY public.desarrollo_item_sucesores
    ADD CONSTRAINT desarrollo_item_sucesores_pkey PRIMARY KEY (id);
 b   ALTER TABLE ONLY public.desarrollo_item_sucesores DROP CONSTRAINT desarrollo_item_sucesores_pkey;
       public            postgres    false    243            �           2606    136474 &   django_admin_log django_admin_log_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);
 P   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_pkey;
       public            postgres    false    213            W           2606    136349 E   django_content_type django_content_type_app_label_model_76bd3d3b_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);
 o   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq;
       public            postgres    false    199    199            Y           2606    136347 ,   django_content_type django_content_type_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);
 V   ALTER TABLE ONLY public.django_content_type DROP CONSTRAINT django_content_type_pkey;
       public            postgres    false    199            U           2606    136339 (   django_migrations django_migrations_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);
 R   ALTER TABLE ONLY public.django_migrations DROP CONSTRAINT django_migrations_pkey;
       public            postgres    false    197            �           2606    136912 "   django_session django_session_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);
 L   ALTER TABLE ONLY public.django_session DROP CONSTRAINT django_session_pkey;
       public            postgres    false    256            �           2606    136924 ,   django_site django_site_domain_a2e37b91_uniq 
   CONSTRAINT     i   ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_domain_a2e37b91_uniq UNIQUE (domain);
 V   ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_domain_a2e37b91_uniq;
       public            postgres    false    258            �           2606    136922    django_site django_site_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);
 F   ALTER TABLE ONLY public.django_site DROP CONSTRAINT django_site_pkey;
       public            postgres    false    258            l           2606    136416 %   login_usuario login_usuario_email_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.login_usuario
    ADD CONSTRAINT login_usuario_email_key UNIQUE (email);
 O   ALTER TABLE ONLY public.login_usuario DROP CONSTRAINT login_usuario_email_key;
       public            postgres    false    207            t           2606    136424 .   login_usuario_groups login_usuario_groups_pkey 
   CONSTRAINT     l   ALTER TABLE ONLY public.login_usuario_groups
    ADD CONSTRAINT login_usuario_groups_pkey PRIMARY KEY (id);
 X   ALTER TABLE ONLY public.login_usuario_groups DROP CONSTRAINT login_usuario_groups_pkey;
       public            postgres    false    209            w           2606    136436 K   login_usuario_groups login_usuario_groups_usuario_id_group_id_735946fe_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.login_usuario_groups
    ADD CONSTRAINT login_usuario_groups_usuario_id_group_id_735946fe_uniq UNIQUE (usuario_id, group_id);
 u   ALTER TABLE ONLY public.login_usuario_groups DROP CONSTRAINT login_usuario_groups_usuario_id_group_id_735946fe_uniq;
       public            postgres    false    209    209            n           2606    136412     login_usuario login_usuario_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.login_usuario
    ADD CONSTRAINT login_usuario_pkey PRIMARY KEY (id);
 J   ALTER TABLE ONLY public.login_usuario DROP CONSTRAINT login_usuario_pkey;
       public            postgres    false    207            y           2606    136450 ^   login_usuario_user_permissions login_usuario_user_permi_usuario_id_permission_id_8ca7a3fc_uniq 
   CONSTRAINT     �   ALTER TABLE ONLY public.login_usuario_user_permissions
    ADD CONSTRAINT login_usuario_user_permi_usuario_id_permission_id_8ca7a3fc_uniq UNIQUE (usuario_id, permission_id);
 �   ALTER TABLE ONLY public.login_usuario_user_permissions DROP CONSTRAINT login_usuario_user_permi_usuario_id_permission_id_8ca7a3fc_uniq;
       public            postgres    false    211    211            |           2606    136432 B   login_usuario_user_permissions login_usuario_user_permissions_pkey 
   CONSTRAINT     �   ALTER TABLE ONLY public.login_usuario_user_permissions
    ADD CONSTRAINT login_usuario_user_permissions_pkey PRIMARY KEY (id);
 l   ALTER TABLE ONLY public.login_usuario_user_permissions DROP CONSTRAINT login_usuario_user_permissions_pkey;
       public            postgres    false    211            q           2606    136414 (   login_usuario login_usuario_username_key 
   CONSTRAINT     g   ALTER TABLE ONLY public.login_usuario
    ADD CONSTRAINT login_usuario_username_key UNIQUE (username);
 R   ALTER TABLE ONLY public.login_usuario DROP CONSTRAINT login_usuario_username_key;
       public            postgres    false    207            �           1259    136650 (   administracion_fase_proyecto_id_927db44b    INDEX     o   CREATE INDEX administracion_fase_proyecto_id_927db44b ON public.administracion_fase USING btree (proyecto_id);
 <   DROP INDEX public.administracion_fase_proyecto_id_927db44b;
       public            postgres    false    215            �           1259    136663 /   administracion_fase_tipos_item_fase_id_ca39030b    INDEX     }   CREATE INDEX administracion_fase_tipos_item_fase_id_ca39030b ON public.administracion_fase_tipos_item USING btree (fase_id);
 C   DROP INDEX public.administracion_fase_tipos_item_fase_id_ca39030b;
       public            postgres    false    233            �           1259    136664 3   administracion_fase_tipos_item_tipoitem_id_930a98c3    INDEX     �   CREATE INDEX administracion_fase_tipos_item_tipoitem_id_930a98c3 ON public.administracion_fase_tipos_item USING btree (tipoitem_id);
 G   DROP INDEX public.administracion_fase_tipos_item_tipoitem_id_930a98c3;
       public            postgres    false    233            �           1259    136649 6   administracion_plantillaatributo_tipo_item_id_fc95b0d1    INDEX     �   CREATE INDEX administracion_plantillaatributo_tipo_item_id_fc95b0d1 ON public.administracion_plantillaatributo USING btree (tipo_item_id);
 J   DROP INDEX public.administracion_plantillaatributo_tipo_item_id_fc95b0d1;
       public            postgres    false    217            �           1259    136633 3   administracion_proyecto_comite_proyecto_id_80f6c1d8    INDEX     �   CREATE INDEX administracion_proyecto_comite_proyecto_id_80f6c1d8 ON public.administracion_proyecto_comite USING btree (proyecto_id);
 G   DROP INDEX public.administracion_proyecto_comite_proyecto_id_80f6c1d8;
       public            postgres    false    229            �           1259    136634 2   administracion_proyecto_comite_usuario_id_da32f11f    INDEX     �   CREATE INDEX administracion_proyecto_comite_usuario_id_da32f11f ON public.administracion_proyecto_comite USING btree (usuario_id);
 F   DROP INDEX public.administracion_proyecto_comite_usuario_id_da32f11f;
       public            postgres    false    229            �           1259    136647 :   administracion_proyecto_participantes_proyecto_id_99172f79    INDEX     �   CREATE INDEX administracion_proyecto_participantes_proyecto_id_99172f79 ON public.administracion_proyecto_participantes USING btree (proyecto_id);
 N   DROP INDEX public.administracion_proyecto_participantes_proyecto_id_99172f79;
       public            postgres    false    231            �           1259    136648 9   administracion_proyecto_participantes_usuario_id_82571a6e    INDEX     �   CREATE INDEX administracion_proyecto_participantes_usuario_id_82571a6e ON public.administracion_proyecto_participantes USING btree (usuario_id);
 M   DROP INDEX public.administracion_proyecto_participantes_usuario_id_82571a6e;
       public            postgres    false    231            �           1259    136620 '   administracion_rol_proyecto_id_aad9f8cd    INDEX     m   CREATE INDEX administracion_rol_proyecto_id_aad9f8cd ON public.administracion_rol USING btree (proyecto_id);
 ;   DROP INDEX public.administracion_rol_proyecto_id_aad9f8cd;
       public            postgres    false    221            �           1259    136619 5   administracion_tipoitem_proyecto_proyecto_id_4cd19c14    INDEX     �   CREATE INDEX administracion_tipoitem_proyecto_proyecto_id_4cd19c14 ON public.administracion_tipoitem_proyecto USING btree (proyecto_id);
 I   DROP INDEX public.administracion_tipoitem_proyecto_proyecto_id_4cd19c14;
       public            postgres    false    227            �           1259    136618 5   administracion_tipoitem_proyecto_tipoitem_id_99ae5ae5    INDEX     �   CREATE INDEX administracion_tipoitem_proyecto_tipoitem_id_99ae5ae5 ON public.administracion_tipoitem_proyecto USING btree (tipoitem_id);
 I   DROP INDEX public.administracion_tipoitem_proyecto_tipoitem_id_99ae5ae5;
       public            postgres    false    227            �           1259    136551 +   administracion_usuarioxrol_fase_id_7478b3aa    INDEX     u   CREATE INDEX administracion_usuarioxrol_fase_id_7478b3aa ON public.administracion_usuarioxrol USING btree (fase_id);
 ?   DROP INDEX public.administracion_usuarioxrol_fase_id_7478b3aa;
       public            postgres    false    225            �           1259    136552 *   administracion_usuarioxrol_rol_id_5f42bb5b    INDEX     s   CREATE INDEX administracion_usuarioxrol_rol_id_5f42bb5b ON public.administracion_usuarioxrol USING btree (rol_id);
 >   DROP INDEX public.administracion_usuarioxrol_rol_id_5f42bb5b;
       public            postgres    false    225            �           1259    136605 .   administracion_usuarioxrol_usuario_id_cf6ec3da    INDEX     {   CREATE INDEX administracion_usuarioxrol_usuario_id_cf6ec3da ON public.administracion_usuarioxrol USING btree (usuario_id);
 B   DROP INDEX public.administracion_usuarioxrol_usuario_id_cf6ec3da;
       public            postgres    false    225            _           1259    136401    auth_group_name_a6ea08ec_like    INDEX     h   CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);
 1   DROP INDEX public.auth_group_name_a6ea08ec_like;
       public            postgres    false    203            d           1259    136397 (   auth_group_permissions_group_id_b120cbf9    INDEX     o   CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);
 <   DROP INDEX public.auth_group_permissions_group_id_b120cbf9;
       public            postgres    false    205            g           1259    136398 -   auth_group_permissions_permission_id_84c5c92e    INDEX     y   CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);
 A   DROP INDEX public.auth_group_permissions_permission_id_84c5c92e;
       public            postgres    false    205            Z           1259    136383 (   auth_permission_content_type_id_2f476e4b    INDEX     o   CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);
 <   DROP INDEX public.auth_permission_content_type_id_2f476e4b;
       public            postgres    false    201            �           1259    136889 +   configuracion_lineabase_creador_id_87bf2b41    INDEX     u   CREATE INDEX configuracion_lineabase_creador_id_87bf2b41 ON public.configuracion_lineabase USING btree (creador_id);
 ?   DROP INDEX public.configuracion_lineabase_creador_id_87bf2b41;
       public            postgres    false    247            �           1259    136890 (   configuracion_lineabase_fase_id_63b59d50    INDEX     o   CREATE INDEX configuracion_lineabase_fase_id_63b59d50 ON public.configuracion_lineabase USING btree (fase_id);
 <   DROP INDEX public.configuracion_lineabase_fase_id_63b59d50;
       public            postgres    false    247            �           1259    136904 .   configuracion_lineabase_items_item_id_2d569ad9    INDEX     {   CREATE INDEX configuracion_lineabase_items_item_id_2d569ad9 ON public.configuracion_lineabase_items USING btree (item_id);
 B   DROP INDEX public.configuracion_lineabase_items_item_id_2d569ad9;
       public            postgres    false    255            �           1259    136903 3   configuracion_lineabase_items_lineabase_id_4dd72449    INDEX     �   CREATE INDEX configuracion_lineabase_items_lineabase_id_4dd72449 ON public.configuracion_lineabase_items USING btree (lineabase_id);
 G   DROP INDEX public.configuracion_lineabase_items_lineabase_id_4dd72449;
       public            postgres    false    255            �           1259    136886 :   configuracion_solicitud_items_a_modificar_item_id_005c02bb    INDEX     �   CREATE INDEX configuracion_solicitud_items_a_modificar_item_id_005c02bb ON public.configuracion_solicitud_items_a_modificar USING btree (item_id);
 N   DROP INDEX public.configuracion_solicitud_items_a_modificar_item_id_005c02bb;
       public            postgres    false    253            �           1259    136885 ?   configuracion_solicitud_items_a_modificar_solicitud_id_3e5a2030    INDEX     �   CREATE INDEX configuracion_solicitud_items_a_modificar_solicitud_id_3e5a2030 ON public.configuracion_solicitud_items_a_modificar USING btree (solicitud_id);
 S   DROP INDEX public.configuracion_solicitud_items_a_modificar_solicitud_id_3e5a2030;
       public            postgres    false    253            �           1259    136887 .   configuracion_solicitud_linea_base_id_0a18a585    INDEX     {   CREATE INDEX configuracion_solicitud_linea_base_id_0a18a585 ON public.configuracion_solicitud USING btree (linea_base_id);
 B   DROP INDEX public.configuracion_solicitud_linea_base_id_0a18a585;
       public            postgres    false    249            �           1259    136888 2   configuracion_solicitud_solicitado_por_id_05c8b916    INDEX     �   CREATE INDEX configuracion_solicitud_solicitado_por_id_05c8b916 ON public.configuracion_solicitud USING btree (solicitado_por_id);
 F   DROP INDEX public.configuracion_solicitud_solicitado_por_id_05c8b916;
       public            postgres    false    249            �           1259    136830 /   configuracion_votoruptura_solicitud_id_7afcd23a    INDEX     }   CREATE INDEX configuracion_votoruptura_solicitud_id_7afcd23a ON public.configuracion_votoruptura USING btree (solicitud_id);
 C   DROP INDEX public.configuracion_votoruptura_solicitud_id_7afcd23a;
       public            postgres    false    251            �           1259    136872 -   configuracion_votoruptura_votante_id_8044cda9    INDEX     y   CREATE INDEX configuracion_votoruptura_votante_id_8044cda9 ON public.configuracion_votoruptura USING btree (votante_id);
 A   DROP INDEX public.configuracion_votoruptura_votante_id_8044cda9;
       public            postgres    false    251            �           1259    136800 .   desarrollo_atributoparticular_item_id_48a9d917    INDEX     {   CREATE INDEX desarrollo_atributoparticular_item_id_48a9d917 ON public.desarrollo_atributoparticular USING btree (item_id);
 B   DROP INDEX public.desarrollo_atributoparticular_item_id_48a9d917;
       public            postgres    false    245            �           1259    136751 1   desarrollo_item_antecesores_from_item_id_aaccf2f8    INDEX     �   CREATE INDEX desarrollo_item_antecesores_from_item_id_aaccf2f8 ON public.desarrollo_item_antecesores USING btree (from_item_id);
 E   DROP INDEX public.desarrollo_item_antecesores_from_item_id_aaccf2f8;
       public            postgres    false    237            �           1259    136752 /   desarrollo_item_antecesores_to_item_id_73b54def    INDEX     }   CREATE INDEX desarrollo_item_antecesores_to_item_id_73b54def ON public.desarrollo_item_antecesores USING btree (to_item_id);
 C   DROP INDEX public.desarrollo_item_antecesores_to_item_id_73b54def;
       public            postgres    false    237            �           1259    136736     desarrollo_item_fase_id_247257b8    INDEX     _   CREATE INDEX desarrollo_item_fase_id_247257b8 ON public.desarrollo_item USING btree (fase_id);
 4   DROP INDEX public.desarrollo_item_fase_id_247257b8;
       public            postgres    false    235            �           1259    136765 +   desarrollo_item_hijos_from_item_id_bba3ce7a    INDEX     u   CREATE INDEX desarrollo_item_hijos_from_item_id_bba3ce7a ON public.desarrollo_item_hijos USING btree (from_item_id);
 ?   DROP INDEX public.desarrollo_item_hijos_from_item_id_bba3ce7a;
       public            postgres    false    239            �           1259    136766 )   desarrollo_item_hijos_to_item_id_b0e562a5    INDEX     q   CREATE INDEX desarrollo_item_hijos_to_item_id_b0e562a5 ON public.desarrollo_item_hijos USING btree (to_item_id);
 =   DROP INDEX public.desarrollo_item_hijos_to_item_id_b0e562a5;
       public            postgres    false    239            �           1259    136779 ,   desarrollo_item_padres_from_item_id_e7e1191c    INDEX     w   CREATE INDEX desarrollo_item_padres_from_item_id_e7e1191c ON public.desarrollo_item_padres USING btree (from_item_id);
 @   DROP INDEX public.desarrollo_item_padres_from_item_id_e7e1191c;
       public            postgres    false    241            �           1259    136780 *   desarrollo_item_padres_to_item_id_f06a1693    INDEX     s   CREATE INDEX desarrollo_item_padres_to_item_id_f06a1693 ON public.desarrollo_item_padres USING btree (to_item_id);
 >   DROP INDEX public.desarrollo_item_padres_to_item_id_f06a1693;
       public            postgres    false    241            �           1259    136793 /   desarrollo_item_sucesores_from_item_id_ef9ff3a6    INDEX     }   CREATE INDEX desarrollo_item_sucesores_from_item_id_ef9ff3a6 ON public.desarrollo_item_sucesores USING btree (from_item_id);
 C   DROP INDEX public.desarrollo_item_sucesores_from_item_id_ef9ff3a6;
       public            postgres    false    243            �           1259    136794 -   desarrollo_item_sucesores_to_item_id_1cc91086    INDEX     y   CREATE INDEX desarrollo_item_sucesores_to_item_id_1cc91086 ON public.desarrollo_item_sucesores USING btree (to_item_id);
 A   DROP INDEX public.desarrollo_item_sucesores_to_item_id_1cc91086;
       public            postgres    false    243            �           1259    136737 %   desarrollo_item_tipo_item_id_5bd67397    INDEX     i   CREATE INDEX desarrollo_item_tipo_item_id_5bd67397 ON public.desarrollo_item USING btree (tipo_item_id);
 9   DROP INDEX public.desarrollo_item_tipo_item_id_5bd67397;
       public            postgres    false    235            �           1259    136738 ,   desarrollo_item_version_anterior_id_ff7f6136    INDEX     w   CREATE INDEX desarrollo_item_version_anterior_id_ff7f6136 ON public.desarrollo_item USING btree (version_anterior_id);
 @   DROP INDEX public.desarrollo_item_version_anterior_id_ff7f6136;
       public            postgres    false    235            ~           1259    136485 )   django_admin_log_content_type_id_c4bce8eb    INDEX     q   CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);
 =   DROP INDEX public.django_admin_log_content_type_id_c4bce8eb;
       public            postgres    false    213            �           1259    136486 !   django_admin_log_user_id_c564eba6    INDEX     a   CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);
 5   DROP INDEX public.django_admin_log_user_id_c564eba6;
       public            postgres    false    213            �           1259    136914 #   django_session_expire_date_a5c62663    INDEX     e   CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);
 7   DROP INDEX public.django_session_expire_date_a5c62663;
       public            postgres    false    256            �           1259    136913 (   django_session_session_key_c0390e0f_like    INDEX     ~   CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);
 <   DROP INDEX public.django_session_session_key_c0390e0f_like;
       public            postgres    false    256            �           1259    136925     django_site_domain_a2e37b91_like    INDEX     n   CREATE INDEX django_site_domain_a2e37b91_like ON public.django_site USING btree (domain varchar_pattern_ops);
 4   DROP INDEX public.django_site_domain_a2e37b91_like;
       public            postgres    false    258            j           1259    136434 !   login_usuario_email_4bd33bd2_like    INDEX     p   CREATE INDEX login_usuario_email_4bd33bd2_like ON public.login_usuario USING btree (email varchar_pattern_ops);
 5   DROP INDEX public.login_usuario_email_4bd33bd2_like;
       public            postgres    false    207            r           1259    136448 &   login_usuario_groups_group_id_e38af65c    INDEX     k   CREATE INDEX login_usuario_groups_group_id_e38af65c ON public.login_usuario_groups USING btree (group_id);
 :   DROP INDEX public.login_usuario_groups_group_id_e38af65c;
       public            postgres    false    209            u           1259    136447 (   login_usuario_groups_usuario_id_ac4f2bc2    INDEX     o   CREATE INDEX login_usuario_groups_usuario_id_ac4f2bc2 ON public.login_usuario_groups USING btree (usuario_id);
 <   DROP INDEX public.login_usuario_groups_usuario_id_ac4f2bc2;
       public            postgres    false    209            z           1259    136462 5   login_usuario_user_permissions_permission_id_a3c8199c    INDEX     �   CREATE INDEX login_usuario_user_permissions_permission_id_a3c8199c ON public.login_usuario_user_permissions USING btree (permission_id);
 I   DROP INDEX public.login_usuario_user_permissions_permission_id_a3c8199c;
       public            postgres    false    211            }           1259    136461 2   login_usuario_user_permissions_usuario_id_0ae58d2f    INDEX     �   CREATE INDEX login_usuario_user_permissions_usuario_id_0ae58d2f ON public.login_usuario_user_permissions USING btree (usuario_id);
 F   DROP INDEX public.login_usuario_user_permissions_usuario_id_0ae58d2f;
       public            postgres    false    211            o           1259    136433 $   login_usuario_username_4d74bf1a_like    INDEX     v   CREATE INDEX login_usuario_username_4d74bf1a_like ON public.login_usuario USING btree (username varchar_pattern_ops);
 8   DROP INDEX public.login_usuario_username_4d74bf1a_like;
       public            postgres    false    207                       2606    136653 Q   administracion_fase_tipos_item administracion_fase__fase_id_ca39030b_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_fase_tipos_item
    ADD CONSTRAINT administracion_fase__fase_id_ca39030b_fk_administr FOREIGN KEY (fase_id) REFERENCES public.administracion_fase(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.administracion_fase_tipos_item DROP CONSTRAINT administracion_fase__fase_id_ca39030b_fk_administr;
       public          postgres    false    2947    215    233                       2606    136658 U   administracion_fase_tipos_item administracion_fase__tipoitem_id_930a98c3_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_fase_tipos_item
    ADD CONSTRAINT administracion_fase__tipoitem_id_930a98c3_fk_administr FOREIGN KEY (tipoitem_id) REFERENCES public.administracion_tipoitem(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE ONLY public.administracion_fase_tipos_item DROP CONSTRAINT administracion_fase__tipoitem_id_930a98c3_fk_administr;
       public          postgres    false    2958    223    233            �           2606    136592 I   administracion_fase administracion_fase_proyecto_id_927db44b_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_fase
    ADD CONSTRAINT administracion_fase_proyecto_id_927db44b_fk_administr FOREIGN KEY (proyecto_id) REFERENCES public.administracion_proyecto(id) DEFERRABLE INITIALLY DEFERRED;
 s   ALTER TABLE ONLY public.administracion_fase DROP CONSTRAINT administracion_fase_proyecto_id_927db44b_fk_administr;
       public          postgres    false    2953    215    219            �           2606    136587 X   administracion_plantillaatributo administracion_plant_tipo_item_id_fc95b0d1_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_plantillaatributo
    ADD CONSTRAINT administracion_plant_tipo_item_id_fc95b0d1_fk_administr FOREIGN KEY (tipo_item_id) REFERENCES public.administracion_tipoitem(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.administracion_plantillaatributo DROP CONSTRAINT administracion_plant_tipo_item_id_fc95b0d1_fk_administr;
       public          postgres    false    217    223    2958            �           2606    136623 U   administracion_proyecto_comite administracion_proye_proyecto_id_80f6c1d8_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_comite
    ADD CONSTRAINT administracion_proye_proyecto_id_80f6c1d8_fk_administr FOREIGN KEY (proyecto_id) REFERENCES public.administracion_proyecto(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE ONLY public.administracion_proyecto_comite DROP CONSTRAINT administracion_proye_proyecto_id_80f6c1d8_fk_administr;
       public          postgres    false    2953    229    219                        2606    136637 \   administracion_proyecto_participantes administracion_proye_proyecto_id_99172f79_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_participantes
    ADD CONSTRAINT administracion_proye_proyecto_id_99172f79_fk_administr FOREIGN KEY (proyecto_id) REFERENCES public.administracion_proyecto(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.administracion_proyecto_participantes DROP CONSTRAINT administracion_proye_proyecto_id_99172f79_fk_administr;
       public          postgres    false    231    219    2953                       2606    136642 [   administracion_proyecto_participantes administracion_proye_usuario_id_82571a6e_fk_login_usu 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_participantes
    ADD CONSTRAINT administracion_proye_usuario_id_82571a6e_fk_login_usu FOREIGN KEY (usuario_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.administracion_proyecto_participantes DROP CONSTRAINT administracion_proye_usuario_id_82571a6e_fk_login_usu;
       public          postgres    false    207    2926    231            �           2606    136628 T   administracion_proyecto_comite administracion_proye_usuario_id_da32f11f_fk_login_usu 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_proyecto_comite
    ADD CONSTRAINT administracion_proye_usuario_id_da32f11f_fk_login_usu FOREIGN KEY (usuario_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 ~   ALTER TABLE ONLY public.administracion_proyecto_comite DROP CONSTRAINT administracion_proye_usuario_id_da32f11f_fk_login_usu;
       public          postgres    false    229    2926    207            �           2606    136566 G   administracion_rol administracion_rol_proyecto_id_aad9f8cd_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_rol
    ADD CONSTRAINT administracion_rol_proyecto_id_aad9f8cd_fk_administr FOREIGN KEY (proyecto_id) REFERENCES public.administracion_proyecto(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.administracion_rol DROP CONSTRAINT administracion_rol_proyecto_id_aad9f8cd_fk_administr;
       public          postgres    false    221    219    2953            �           2606    136613 W   administracion_tipoitem_proyecto administracion_tipoi_proyecto_id_4cd19c14_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto
    ADD CONSTRAINT administracion_tipoi_proyecto_id_4cd19c14_fk_administr FOREIGN KEY (proyecto_id) REFERENCES public.administracion_proyecto(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto DROP CONSTRAINT administracion_tipoi_proyecto_id_4cd19c14_fk_administr;
       public          postgres    false    227    219    2953            �           2606    136608 W   administracion_tipoitem_proyecto administracion_tipoi_tipoitem_id_99ae5ae5_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto
    ADD CONSTRAINT administracion_tipoi_tipoitem_id_99ae5ae5_fk_administr FOREIGN KEY (tipoitem_id) REFERENCES public.administracion_tipoitem(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.administracion_tipoitem_proyecto DROP CONSTRAINT administracion_tipoi_tipoitem_id_99ae5ae5_fk_administr;
       public          postgres    false    227    2958    223            �           2606    136541 M   administracion_usuarioxrol administracion_usuar_fase_id_7478b3aa_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_usuarioxrol
    ADD CONSTRAINT administracion_usuar_fase_id_7478b3aa_fk_administr FOREIGN KEY (fase_id) REFERENCES public.administracion_fase(id) DEFERRABLE INITIALLY DEFERRED;
 w   ALTER TABLE ONLY public.administracion_usuarioxrol DROP CONSTRAINT administracion_usuar_fase_id_7478b3aa_fk_administr;
       public          postgres    false    215    2947    225            �           2606    136546 L   administracion_usuarioxrol administracion_usuar_rol_id_5f42bb5b_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_usuarioxrol
    ADD CONSTRAINT administracion_usuar_rol_id_5f42bb5b_fk_administr FOREIGN KEY (rol_id) REFERENCES public.administracion_rol(id) DEFERRABLE INITIALLY DEFERRED;
 v   ALTER TABLE ONLY public.administracion_usuarioxrol DROP CONSTRAINT administracion_usuar_rol_id_5f42bb5b_fk_administr;
       public          postgres    false    221    2955    225            �           2606    136553 P   administracion_usuarioxrol administracion_usuar_usuario_id_cf6ec3da_fk_login_usu 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.administracion_usuarioxrol
    ADD CONSTRAINT administracion_usuar_usuario_id_cf6ec3da_fk_login_usu FOREIGN KEY (usuario_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.administracion_usuarioxrol DROP CONSTRAINT administracion_usuar_usuario_id_cf6ec3da_fk_login_usu;
       public          postgres    false    2926    225    207            �           2606    136392 O   auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
       public          postgres    false    201    2910    205            �           2606    136387 P   auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.auth_group_permissions DROP CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
       public          postgres    false    2915    203    205            �           2606    136378 E   auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 o   ALTER TABLE ONLY public.auth_permission DROP CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co;
       public          postgres    false    2905    201    199                       2606    136859 J   configuracion_lineabase configuracion_lineab_fase_id_63b59d50_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_lineabase
    ADD CONSTRAINT configuracion_lineab_fase_id_63b59d50_fk_administr FOREIGN KEY (fase_id) REFERENCES public.administracion_fase(id) DEFERRABLE INITIALLY DEFERRED;
 t   ALTER TABLE ONLY public.configuracion_lineabase DROP CONSTRAINT configuracion_lineab_fase_id_63b59d50_fk_administr;
       public          postgres    false    2947    247    215                       2606    136898 P   configuracion_lineabase_items configuracion_lineab_item_id_2d569ad9_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_lineabase_items
    ADD CONSTRAINT configuracion_lineab_item_id_2d569ad9_fk_desarroll FOREIGN KEY (item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.configuracion_lineabase_items DROP CONSTRAINT configuracion_lineab_item_id_2d569ad9_fk_desarroll;
       public          postgres    false    2990    235    255                       2606    136893 U   configuracion_lineabase_items configuracion_lineab_lineabase_id_4dd72449_fk_configura 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_lineabase_items
    ADD CONSTRAINT configuracion_lineab_lineabase_id_4dd72449_fk_configura FOREIGN KEY (lineabase_id) REFERENCES public.configuracion_lineabase(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE ONLY public.configuracion_lineabase_items DROP CONSTRAINT configuracion_lineab_lineabase_id_4dd72449_fk_configura;
       public          postgres    false    255    247    3023                       2606    136854 W   configuracion_lineabase configuracion_lineabase_creador_id_87bf2b41_fk_login_usuario_id 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_lineabase
    ADD CONSTRAINT configuracion_lineabase_creador_id_87bf2b41_fk_login_usuario_id FOREIGN KEY (creador_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.configuracion_lineabase DROP CONSTRAINT configuracion_lineabase_creador_id_87bf2b41_fk_login_usuario_id;
       public          postgres    false    2926    247    207                       2606    136880 \   configuracion_solicitud_items_a_modificar configuracion_solici_item_id_005c02bb_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar
    ADD CONSTRAINT configuracion_solici_item_id_005c02bb_fk_desarroll FOREIGN KEY (item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar DROP CONSTRAINT configuracion_solici_item_id_005c02bb_fk_desarroll;
       public          postgres    false    2990    253    235                       2606    136844 P   configuracion_solicitud configuracion_solici_linea_base_id_0a18a585_fk_configura 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_solicitud
    ADD CONSTRAINT configuracion_solici_linea_base_id_0a18a585_fk_configura FOREIGN KEY (linea_base_id) REFERENCES public.configuracion_lineabase(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.configuracion_solicitud DROP CONSTRAINT configuracion_solici_linea_base_id_0a18a585_fk_configura;
       public          postgres    false    249    3023    247                       2606    136849 T   configuracion_solicitud configuracion_solici_solicitado_por_id_05c8b916_fk_login_usu 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_solicitud
    ADD CONSTRAINT configuracion_solici_solicitado_por_id_05c8b916_fk_login_usu FOREIGN KEY (solicitado_por_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 ~   ALTER TABLE ONLY public.configuracion_solicitud DROP CONSTRAINT configuracion_solici_solicitado_por_id_05c8b916_fk_login_usu;
       public          postgres    false    249    207    2926                       2606    136875 a   configuracion_solicitud_items_a_modificar configuracion_solici_solicitud_id_3e5a2030_fk_configura 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar
    ADD CONSTRAINT configuracion_solici_solicitud_id_3e5a2030_fk_configura FOREIGN KEY (solicitud_id) REFERENCES public.configuracion_solicitud(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.configuracion_solicitud_items_a_modificar DROP CONSTRAINT configuracion_solici_solicitud_id_3e5a2030_fk_configura;
       public          postgres    false    249    253    3026                       2606    136825 Q   configuracion_votoruptura configuracion_votoru_solicitud_id_7afcd23a_fk_configura 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_votoruptura
    ADD CONSTRAINT configuracion_votoru_solicitud_id_7afcd23a_fk_configura FOREIGN KEY (solicitud_id) REFERENCES public.configuracion_solicitud(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.configuracion_votoruptura DROP CONSTRAINT configuracion_votoru_solicitud_id_7afcd23a_fk_configura;
       public          postgres    false    3026    249    251                       2606    136831 O   configuracion_votoruptura configuracion_votoru_votante_id_8044cda9_fk_login_usu 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.configuracion_votoruptura
    ADD CONSTRAINT configuracion_votoru_votante_id_8044cda9_fk_login_usu FOREIGN KEY (votante_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.configuracion_votoruptura DROP CONSTRAINT configuracion_votoru_votante_id_8044cda9_fk_login_usu;
       public          postgres    false    251    207    2926                       2606    136795 P   desarrollo_atributoparticular desarrollo_atributop_item_id_48a9d917_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_atributoparticular
    ADD CONSTRAINT desarrollo_atributop_item_id_48a9d917_fk_desarroll FOREIGN KEY (item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 z   ALTER TABLE ONLY public.desarrollo_atributoparticular DROP CONSTRAINT desarrollo_atributop_item_id_48a9d917_fk_desarroll;
       public          postgres    false    235    2990    245                       2606    136741 S   desarrollo_item_antecesores desarrollo_item_ante_from_item_id_aaccf2f8_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_antecesores
    ADD CONSTRAINT desarrollo_item_ante_from_item_id_aaccf2f8_fk_desarroll FOREIGN KEY (from_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 }   ALTER TABLE ONLY public.desarrollo_item_antecesores DROP CONSTRAINT desarrollo_item_ante_from_item_id_aaccf2f8_fk_desarroll;
       public          postgres    false    237    235    2990                       2606    136746 Q   desarrollo_item_antecesores desarrollo_item_ante_to_item_id_73b54def_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_antecesores
    ADD CONSTRAINT desarrollo_item_ante_to_item_id_73b54def_fk_desarroll FOREIGN KEY (to_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.desarrollo_item_antecesores DROP CONSTRAINT desarrollo_item_ante_to_item_id_73b54def_fk_desarroll;
       public          postgres    false    237    235    2990                       2606    136721 J   desarrollo_item desarrollo_item_fase_id_247257b8_fk_administracion_fase_id 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item
    ADD CONSTRAINT desarrollo_item_fase_id_247257b8_fk_administracion_fase_id FOREIGN KEY (fase_id) REFERENCES public.administracion_fase(id) DEFERRABLE INITIALLY DEFERRED;
 t   ALTER TABLE ONLY public.desarrollo_item DROP CONSTRAINT desarrollo_item_fase_id_247257b8_fk_administracion_fase_id;
       public          postgres    false    235    2947    215            	           2606    136755 M   desarrollo_item_hijos desarrollo_item_hijo_from_item_id_bba3ce7a_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_hijos
    ADD CONSTRAINT desarrollo_item_hijo_from_item_id_bba3ce7a_fk_desarroll FOREIGN KEY (from_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 w   ALTER TABLE ONLY public.desarrollo_item_hijos DROP CONSTRAINT desarrollo_item_hijo_from_item_id_bba3ce7a_fk_desarroll;
       public          postgres    false    239    235    2990            
           2606    136760 U   desarrollo_item_hijos desarrollo_item_hijos_to_item_id_b0e562a5_fk_desarrollo_item_id 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_hijos
    ADD CONSTRAINT desarrollo_item_hijos_to_item_id_b0e562a5_fk_desarrollo_item_id FOREIGN KEY (to_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE ONLY public.desarrollo_item_hijos DROP CONSTRAINT desarrollo_item_hijos_to_item_id_b0e562a5_fk_desarrollo_item_id;
       public          postgres    false    239    235    2990                       2606    136769 N   desarrollo_item_padres desarrollo_item_padr_from_item_id_e7e1191c_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_padres
    ADD CONSTRAINT desarrollo_item_padr_from_item_id_e7e1191c_fk_desarroll FOREIGN KEY (from_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 x   ALTER TABLE ONLY public.desarrollo_item_padres DROP CONSTRAINT desarrollo_item_padr_from_item_id_e7e1191c_fk_desarroll;
       public          postgres    false    241    2990    235                       2606    136774 L   desarrollo_item_padres desarrollo_item_padr_to_item_id_f06a1693_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_padres
    ADD CONSTRAINT desarrollo_item_padr_to_item_id_f06a1693_fk_desarroll FOREIGN KEY (to_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 v   ALTER TABLE ONLY public.desarrollo_item_padres DROP CONSTRAINT desarrollo_item_padr_to_item_id_f06a1693_fk_desarroll;
       public          postgres    false    241    235    2990            
           2606    136783 Q   desarrollo_item_sucesores desarrollo_item_suce_from_item_id_ef9ff3a6_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_sucesores
    ADD CONSTRAINT desarrollo_item_suce_from_item_id_ef9ff3a6_fk_desarroll FOREIGN KEY (from_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.desarrollo_item_sucesores DROP CONSTRAINT desarrollo_item_suce_from_item_id_ef9ff3a6_fk_desarroll;
       public          postgres    false    243    2990    235                       2606    136788 O   desarrollo_item_sucesores desarrollo_item_suce_to_item_id_1cc91086_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item_sucesores
    ADD CONSTRAINT desarrollo_item_suce_to_item_id_1cc91086_fk_desarroll FOREIGN KEY (to_item_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 y   ALTER TABLE ONLY public.desarrollo_item_sucesores DROP CONSTRAINT desarrollo_item_suce_to_item_id_1cc91086_fk_desarroll;
       public          postgres    false    235    2990    243                       2606    136726 B   desarrollo_item desarrollo_item_tipo_item_id_5bd67397_fk_administr 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item
    ADD CONSTRAINT desarrollo_item_tipo_item_id_5bd67397_fk_administr FOREIGN KEY (tipo_item_id) REFERENCES public.administracion_tipoitem(id) DEFERRABLE INITIALLY DEFERRED;
 l   ALTER TABLE ONLY public.desarrollo_item DROP CONSTRAINT desarrollo_item_tipo_item_id_5bd67397_fk_administr;
       public          postgres    false    223    235    2958                       2606    136731 I   desarrollo_item desarrollo_item_version_anterior_id_ff7f6136_fk_desarroll 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.desarrollo_item
    ADD CONSTRAINT desarrollo_item_version_anterior_id_ff7f6136_fk_desarroll FOREIGN KEY (version_anterior_id) REFERENCES public.desarrollo_item(id) DEFERRABLE INITIALLY DEFERRED;
 s   ALTER TABLE ONLY public.desarrollo_item DROP CONSTRAINT desarrollo_item_version_anterior_id_ff7f6136_fk_desarroll;
       public          postgres    false    235    235    2990            �           2606    136475 G   django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;
 q   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co;
       public          postgres    false    213    2905    199            �           2606    136480 F   django_admin_log django_admin_log_user_id_c564eba6_fk_login_usuario_id 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_login_usuario_id FOREIGN KEY (user_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 p   ALTER TABLE ONLY public.django_admin_log DROP CONSTRAINT django_admin_log_user_id_c564eba6_fk_login_usuario_id;
       public          postgres    false    213    2926    207            �           2606    136442 L   login_usuario_groups login_usuario_groups_group_id_e38af65c_fk_auth_group_id 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.login_usuario_groups
    ADD CONSTRAINT login_usuario_groups_group_id_e38af65c_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;
 v   ALTER TABLE ONLY public.login_usuario_groups DROP CONSTRAINT login_usuario_groups_group_id_e38af65c_fk_auth_group_id;
       public          postgres    false    203    209    2915            �           2606    136437 Q   login_usuario_groups login_usuario_groups_usuario_id_ac4f2bc2_fk_login_usuario_id 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.login_usuario_groups
    ADD CONSTRAINT login_usuario_groups_usuario_id_ac4f2bc2_fk_login_usuario_id FOREIGN KEY (usuario_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 {   ALTER TABLE ONLY public.login_usuario_groups DROP CONSTRAINT login_usuario_groups_usuario_id_ac4f2bc2_fk_login_usuario_id;
       public          postgres    false    207    209    2926            �           2606    136456 W   login_usuario_user_permissions login_usuario_user_p_permission_id_a3c8199c_fk_auth_perm 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.login_usuario_user_permissions
    ADD CONSTRAINT login_usuario_user_p_permission_id_a3c8199c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;
 �   ALTER TABLE ONLY public.login_usuario_user_permissions DROP CONSTRAINT login_usuario_user_p_permission_id_a3c8199c_fk_auth_perm;
       public          postgres    false    211    2910    201            �           2606    136451 T   login_usuario_user_permissions login_usuario_user_p_usuario_id_0ae58d2f_fk_login_usu 
   FK CONSTRAINT     �   ALTER TABLE ONLY public.login_usuario_user_permissions
    ADD CONSTRAINT login_usuario_user_p_usuario_id_0ae58d2f_fk_login_usu FOREIGN KEY (usuario_id) REFERENCES public.login_usuario(id) DEFERRABLE INITIALLY DEFERRED;
 ~   ALTER TABLE ONLY public.login_usuario_user_permissions DROP CONSTRAINT login_usuario_user_p_usuario_id_0ae58d2f_fk_login_usu;
       public          postgres    false    207    2926    211            �   G   x�3�tK,NU0��LL�L-*I�4�2��!�CČ��L0�q�b�5�2��k�eΉ�sY��,Qx1z\\\ =�*d      �      x�3�4�4�2�B.cN ����� !��      �   0   x�3�tKM�HT����,IUHIUH�+)JMO�LI,I�L�4����� o�      �   �   x�3��,I��M�KLO-�4202�5��52Eb*ZXX�������p���Pj�BjVjrirf~�1rq�W�&��+@dq�hdfej�gijfb`��L#.c���y��B� Qf^frfbJ>X�1W� �A4�      �   *   x�
�9 0��&3�'h�G�B�5Tn:�Q����<�|f��      �   2   x�
ȹ
 0��7L [ηK��#jX0##)+d��Ō�ˊm�c��|Ҋ      �   
   x������ � �      �   �   x�e�1
�0k���@�'T�pp�FQ�p �l���G�$R����t^o¨b��ĉ�(BC���X7ڛh��\����|<N2���WL"�Z	�G��9�-�Zh�fp�~��g�o�į eA�$,�%s�-���ϋ��p�K�      �   +   x�3�4�4�2�4�Ɯ�@�(b�e
1�2�q��qqq fa�      �   
   x������ � �      �   
   x������ � �      �   
   x������ � �      �   �  x�u�[��@E��V�
F) ����H#:�� рx�tv?`��oP>�_��~VmV]�Y�ݲ�N�����^����\�V�-�K
^c'yI����:�l]Ph���q��Ǳ�Z���.���P�{�~���aO�$9�Yކn�]A�t���ʥ�x	�SBDG�\U@R.6�K�N�o�M�>��Ddi]�:�X��n�(P��|�=n�c��vO�r����*#�v����^��)DVԨ��;��r�sH�T�0�$��K�NE��y��;ғ�q����9L� �����F��1f�� �������;��z��c��0���03,ez8u���j��i�����c�:w�ħBZ�L����x��~ٛ�Ͻf�_v��O'��{�,���ɽ/`�-����0��L�,��[�57J���X.}	�/Eѡ:̾�E��f��J���N�T�]����~ǯ�/! �����@�HQ IN���&�wQؐ~����0�Hcb�!`j���
��0�6�k�xk| Ю���TE& !�'&LR�$��Ӟ���0՗���e�JZ�{���^1}��x�.�x�~0ay�L{|ժ	j�6V����|��ʺ��5d��R�� N�T
ۯ*@��JAM��5����|�l� �0}�B�M���&x@򁨜&�[��a�y�\��i]�%��=�b
���Q���G��-����?#���      �   .   x�3�4202�5��52�H,J�L��tN-*JLI�4�4����� ���      �      x�3�4�4�2�\1z\\\ F      �   
   x������ � �      �   
   x������ � �      �   
   x������ � �      �   J   x�3�tKM�HT����,IUHIUH�+)JMO�LI,I��4�2¯����@��@�؀ӈ˘�if\&TXp��qqq ��,�      �   4  x����n�0���S�	&�Ǳ�8���+�)M�$L�����@b�|�+������z�L#;jl��'j���mPZb�6�!ђ@�ގG��fnnakSK�A��w�����[#M9RC}9��0(!��ц(���ƿ��fD�G���-Mٲ���m1�-LՊR�	&�v�)G�=\�����L�)��>w����Z�SI�l�@����~��J�9����Uj�֢�h����>}���?!�{N�'��?�~�ؓ��;8^�kF�erN��f�MjV�3Ჿ���6�>^��y��b6�� |l2>      �   7   x���
 !�w;�f8s!�8v�Um�L�*���%i�I�5KGΉ���O���/      �   
   x������ � �      �   
   x������ � �      �   ,   x�3�4�4�2� ��@Ғ˄�А�Ј˔�И�Є+F��� d�      �   
   x������ � �      �   �   x�eP�n!<㏩J���^�l-��&��}!�H� {̀w8-�]�9f�v���e!U��
��k����Im-Q�8:���89%k�~¹�����.[4�	��v7�_#Zf��M�Z�����1tʏ�p�Q�­�~?R�z���MQQڜ�m��;��TP�BM(�O�Wn4�煉r�k�?�r�@V'𗁺���bm�� �[��      �   /  x����n� ��������>�J%$E�M
vվ�N�HE��������?c�a��4�?W�:B?��ۡC���7�@�3��A(�7��K�&�1|9s;0��LvtMT~Ǖ((��e�ؿ�)���h�0�h�.�>%�z���t�_�PJ)-hA�
Eo�%���(��P�Faϔ����N$�*�
���M����Ė�]-��+j��܍��ǭ�O�����=ax-���ȗ���!&cO'�bь.%{q��2Mj�d��p�Y��֘��pk:�Fҿ*���&�L�w���r}	ä�d�hs.�Y��D�\c��y�c�>�1�Y�9���/f���Żj��I=AJp�d��W4
_C�	kfsş���lBqI�!{������H��=�e�σ���G�Ǧ�d�	���
�i����{٨5c�6IC�kEI4j��G���=�Н\�y4�!�܏����ֹǺI����;Ҟ彩x�����BϘ|��a]r7����{J(��Ȼ�����jJk�P<4wßB^��Y&��4�Y/�d�:���A��      �   �  x�E�Y��0  ���},B�?T�����"Q� �~f���u
FCKz�n��Oã0)�4��)O:��Lwӥ�w�Xj�c&W1����Sߊ�H�W��l�]�%�[v�P�;�2p���*�;ӻ�ӊ���z��eR�0]�hc��k���㛜�eQÌ"�畓�o<vz���~
��Y�D3�z�-��7�m���Y��x�"�F��z���<��Oz�%���֘cPqjǮ��m�'�I�%���
'�o����
�R��$@�G�����<
�3��I)IC���P���[�=�kAnkr=�Y郂u������tW�2�a���r��3��'O����O��r�v֖y=�\ :O�B"ܹ9�*f����5޵�z�ě�ĻU�9��n��VfV4�ݑ��PB�������F
;KD�7�*�83���*�F�g���佛��-����=+��6�>��R��BQ��J	���?��b�7��      �      x�3�L�H�-�I�K��Efs��qqq �<	�      �   v  x�m�_O�0ş�O��io��OJ�"�(D�K�:�[�ӻM#MO��{~�! @z$�8��n��!՚���#��Y���*_�dU"��� ��8TJI���i�]��¾�ǫ٭xx�q�П��6�h
~}�o�(z�Ei�Q���~f	�Z�����.����q��N]���}�����yŪ�R]���O_���. ��K	B��S�[���Zlu��!��TI�{�?<ɷ��+�P�M<e�.�]���{�Q$9�z��+tW���+J�h͵���q��Ͳ���e4��/�a����3��	�a�0��PL�!��D�,l�� �	,9ڄ+;���r�xNv�$���ϻ|�٤�=����2�u      �   
   x������ � �      �   
   x������ � �     
