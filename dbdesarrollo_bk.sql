--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.23
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: administracion_proyecto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_proyecto (id, nombre, fecha_inicio, fecha_ejecucion, fecha_finalizado, fecha_cancelado, estado, numero_fases, cant_comite, gerente) FROM stdin;
1	ItemManager	2020-09-25	2020-09-25 18:10:53.0576-04	\N	\N	en ejecucion	3	3	1
2	Proyecto en eje	2020-09-25	2020-09-25 18:26:57.956404-04	\N	\N	en ejecucion	3	3	2
3	Proyecto Ini	2020-09-25	\N	\N	\N	iniciado	3	3	3
4	Proyecto sin iniciar	2020-10-05	\N	\N	\N	iniciado	3	3	1
5	Proyecto iniciado (sin items)	2020-10-05	2020-10-05 20:57:47.15107-03	\N	\N	en ejecucion	3	3	1
6	Proyecto avanzado	2020-10-05	2020-10-05 21:17:26.353276-03	\N	\N	en ejecucion	3	3	1
7	Proyecto para finalizar	2020-10-06	2020-10-05 21:49:39.340554-03	\N	\N	en ejecucion	3	3	1
\.


--
-- Data for Name: administracion_fase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_fase (id, nombre, descripcion, estado, proyecto_id) FROM stdin;
1	Fase 1		abierta	1
2	Fase 2		abierta	1
3	Fase 3		abierta	1
4	Fase 1		abierta	2
5	Fase 2		abierta	2
6	Fase 3		abierta	2
7			abierta	3
8			abierta	3
9			abierta	3
10			abierta	4
11			abierta	4
12			abierta	4
13	Fase inicial		abierta	5
14	Fase media		abierta	5
15	Fase final		abierta	5
17	Fase intermedia		abierta	6
18	Fase final		abierta	6
16	Fase inicio		cerrada	6
19	Fase desarrollo		cerrada	7
20	Fase de pruebas		cerrada	7
21	Fase de implementacion		cerrada	7
\.


--
-- Data for Name: administracion_tipoitem; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_tipoitem (id, nombre, descripcion, prefijo) FROM stdin;
1	Caso de Uso	Se definen los casos de uso	CU
2	Requisito Funcional	Se describen las funciones que va cumplir es sistema	RF
3	Requisito No Funcional	Requisitos que va cumplir el sistema pero no son prioritarios	RNF
4	Prototipo	Prototipo del producto	PT
\.


--
-- Data for Name: administracion_fase_tipos_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_fase_tipos_item (id, fase_id, tipoitem_id) FROM stdin;
1	1	1
2	2	2
3	3	3
4	16	2
5	17	1
6	18	4
7	19	2
8	20	1
9	21	4
\.


--
-- Data for Name: administracion_plantillaatributo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_plantillaatributo (id, nombre, tipo, es_requerido, tipo_item_id) FROM stdin;
1	Fecha limite de entrega	date	f	1
2	Cantidad de comentarios	number	f	4
\.


--
-- Data for Name: login_usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.login_usuario (id, password, last_login, is_superuser, username, first_name, last_name, is_staff, is_active, date_joined, email, "localId", id_token, is_gerente) FROM stdin;
5		2020-10-05 21:15:19.232167-03	t	admin	Administrador		f	f	2020-09-25 18:03:41.977761-04	admin@itemmanager.com	au5ThzeG2BXV6V2qcKS2tXDvONx1	\N	f
2		2020-09-25 18:24:29.662563-04	f	mati	Matias		f	t	2020-09-25 18:00:55.581768-04	mati@itemmanager.com	4TYndyaROsej7iMcS3ZeDmeDYjt2	\N	t
3		2020-09-25 18:27:26.940183-04	f	pao	Pao		f	t	2020-09-25 18:01:13.710353-04	pao@itemmanager.com	kAcOfqln67enJlDXmQFHVJ9ttx62	\N	t
4		\N	f	david	David		f	t	2020-09-25 18:01:46.865033-04	david@itemmanager.com	ijKpuB2HVBWlSEs3sSl7L7fIB1b2	\N	t
6		\N	f	Comite1			f	t	2020-10-05 21:14:12.527246-03	comite1@itemmanager.com	WnTsGirfw5cpYvVn2rna38kp46m2	\N	f
7		\N	f	Comite2			f	t	2020-10-05 21:14:36.888025-03	comite2@itemmanager.com	9jjJ3c2ysHgFtSYIWKNXyJHFj0E3	\N	f
8		\N	f	Comite3			f	t	2020-10-05 21:15:04.147847-03	comite3@itemmanager.com	J4Xrqsn7XRbMKzH5aiNW4XSx5V53	\N	f
1		2020-10-05 21:15:43.295528-03	f	fer	Fernando		f	t	2020-09-25 18:00:35.643582-04	fer@itemmanager.com	oJRGK2Rcp9RwwdcDOQZwmuqqfEH2	\N	t
\.


--
-- Data for Name: administracion_proyecto_comite; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_proyecto_comite (id, proyecto_id, usuario_id) FROM stdin;
1	1	4
2	1	3
3	1	1
4	2	2
5	2	3
6	2	4
7	5	1
8	5	2
9	5	4
10	6	6
11	6	7
12	6	8
13	7	6
14	7	7
15	7	8
\.


--
-- Data for Name: administracion_proyecto_participantes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_proyecto_participantes (id, proyecto_id, usuario_id) FROM stdin;
1	1	1
2	1	3
3	1	4
4	1	2
5	2	2
6	2	3
7	2	4
8	2	1
9	3	3
10	4	1
11	5	1
12	5	4
13	5	2
14	5	3
15	6	1
16	6	4
17	6	2
18	6	3
19	6	6
20	6	7
21	6	8
22	7	1
23	7	2
24	7	3
25	7	4
26	7	6
27	7	7
28	7	8
\.


--
-- Data for Name: administracion_rol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_rol (id, nombre, crear_item, modificar_item, desactivar_item, aprobar_item, reversionar_item, crear_relaciones_ph, crear_relaciones_as, borrar_relaciones, activo, proyecto_id) FROM stdin;
1	Aprobador	f	f	f	t	f	f	f	f	f	6
2	Creador	t	f	f	f	f	f	f	f	f	6
3	Relacionador	f	f	f	f	f	t	t	t	f	6
4	Reversor	f	f	f	f	t	f	f	f	f	6
5	Editor	f	t	t	f	f	f	f	f	f	6
6	Dev	t	t	t	f	t	t	t	t	t	6
7	Tester	f	f	t	t	f	f	f	f	t	6
8	All in	t	t	t	t	t	t	t	t	t	7
\.


--
-- Data for Name: administracion_tipoitem_proyecto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_tipoitem_proyecto (id, tipoitem_id, proyecto_id) FROM stdin;
1	1	1
2	2	1
3	3	1
4	1	2
5	2	2
6	3	2
7	2	5
8	3	5
9	1	5
10	2	6
11	1	6
12	4	6
13	1	7
14	2	7
15	4	7
\.


--
-- Data for Name: administracion_usuarioxrol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.administracion_usuarioxrol (id, activo, fase_id, rol_id, usuario_id) FROM stdin;
1	t	16	6	4
2	t	17	6	2
3	t	18	6	3
4	t	18	7	3
5	t	17	7	3
6	t	16	7	3
7	t	19	8	4
8	t	20	8	4
9	t	21	8	4
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	sites	site
7	login	usuario
8	administracion	fase
9	administracion	plantillaatributo
10	administracion	proyecto
11	administracion	rol
12	administracion	tipoitem
13	administracion	usuarioxrol
14	desarrollo	item
15	desarrollo	atributoparticular
16	configuracion	lineabase
17	configuracion	solicitud
18	configuracion	votoruptura
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add site	6	add_site
22	Can change site	6	change_site
23	Can delete site	6	delete_site
24	Can view site	6	view_site
25	Can add user	7	add_usuario
26	Can change user	7	change_usuario
27	Can delete user	7	delete_usuario
28	Can view user	7	view_usuario
29	Can add fase	8	add_fase
30	Can change fase	8	change_fase
31	Can delete fase	8	delete_fase
32	Can view fase	8	view_fase
33	Can add plantilla atributo	9	add_plantillaatributo
34	Can change plantilla atributo	9	change_plantillaatributo
35	Can delete plantilla atributo	9	delete_plantillaatributo
36	Can view plantilla atributo	9	view_plantillaatributo
37	Can add proyecto	10	add_proyecto
38	Can change proyecto	10	change_proyecto
39	Can delete proyecto	10	delete_proyecto
40	Can view proyecto	10	view_proyecto
41	Can add rol	11	add_rol
42	Can change rol	11	change_rol
43	Can delete rol	11	delete_rol
44	Can view rol	11	view_rol
45	Can add tipo item	12	add_tipoitem
46	Can change tipo item	12	change_tipoitem
47	Can delete tipo item	12	delete_tipoitem
48	Can view tipo item	12	view_tipoitem
49	Can add usuariox rol	13	add_usuarioxrol
50	Can change usuariox rol	13	change_usuarioxrol
51	Can delete usuariox rol	13	delete_usuarioxrol
52	Can view usuariox rol	13	view_usuarioxrol
53	Can add item	14	add_item
54	Can change item	14	change_item
55	Can delete item	14	delete_item
56	Can view item	14	view_item
57	Can add atributo particular	15	add_atributoparticular
58	Can change atributo particular	15	change_atributoparticular
59	Can delete atributo particular	15	delete_atributoparticular
60	Can view atributo particular	15	view_atributoparticular
61	Can add linea base	16	add_lineabase
62	Can change linea base	16	change_lineabase
63	Can delete linea base	16	delete_lineabase
64	Can view linea base	16	view_lineabase
65	Can add solicitud	17	add_solicitud
66	Can change solicitud	17	change_solicitud
67	Can delete solicitud	17	delete_solicitud
68	Can view solicitud	17	view_solicitud
69	Can add voto ruptura	18	add_votoruptura
70	Can change voto ruptura	18	change_votoruptura
71	Can delete voto ruptura	18	delete_votoruptura
72	Can view voto ruptura	18	view_votoruptura
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: configuracion_lineabase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracion_lineabase (id, fecha_creacion, tipo, estado, creador_id, fase_id) FROM stdin;
1	2020-09-25	Parcial	Cerrada	1	1
2	2020-10-05	Parcial	Cerrada	1	16
3	2020-10-05	Parcial	Cerrada	1	19
4	2020-10-05	Parcial	Cerrada	1	20
5	2020-10-05	Parcial	Cerrada	1	21
\.


--
-- Data for Name: desarrollo_item; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.desarrollo_item (id, nombre, estado, numeracion, version, complejidad, descripcion, id_version, fase_id, tipo_item_id, version_anterior_id) FROM stdin;
1	Crear relaciones	Desactivado	1	1	5	\N	1	1	1	\N
3	Relacionar items de la misma fase	Desactivado	1	1	5	\N	3	2	2	\N
6	Crear relaciones	Desactivado	1	2	5	\N	1	1	1	1
4	Relacionar items en fases anteriores y posteriores	Desactivado	2	1	5	\N	4	2	2	\N
9	Relacionar items en fases anteriores y posteriores	Desactivado	2	2	5	\N	4	2	2	4
7	Relacionar items de la misma fase	Desactivado	1	2	5	\N	3	2	2	3
5	Las relaciones se muestran en colores representativos segun su tipo	Desactivado	1	1	2	\N	5	3	3	\N
11	Relacionar items de la misma fase	Aprobado	1	3	5	\N	3	2	2	7
10	Relacionar items en fases anteriores y posteriores	Desactivado	2	3	6	None	4	2	2	9
12	Las relaciones se muestran en colores representativos segun su tipo	Desactivado	1	2	2	\N	5	3	3	5
13	Relacionar items en fases anteriores y posteriores	Aprobado	2	4	6	None	4	2	2	10
14	Las relaciones se muestran en colores representativos segun su tipo	En Desarrollo	1	3	2	\N	5	3	3	12
2	Detallar proyecto	En Linea Base	2	1	5	\N	2	1	1	\N
8	Crear relaciones	En Linea Base	1	3	5	\N	1	1	1	6
30	Creando un proyecto	Desactivado	1	4	3	1. Entrar a crear proyecto, 2. Seleccionar un Nombre, 3. Guardar cambios	18	17	1	29
19	Vista creacion de proyecto	Desactivado	1	1	2	\N	19	18	4	\N
32	Creando un proyecto	Aprobado	1	5	3	1. Entrar a crear proyecto, 2. Seleccionar un Nombre, 3. Guardar cambios	18	17	1	30
15	Crear proyecto	Desactivado	1	1	5	\N	15	16	2	\N
21	Crear proyecto	Desactivado	1	2	5	Descripcion modificada	15	16	2	15
18	Creando un proyecto	Desactivado	1	1	3	\N	18	17	1	\N
33	Vista creacion de proyecto	En Desarrollo	1	2	2	\N	19	18	4	19
24	Crear proyecto	En Linea Base	1	4	4	Descripcion modificada	15	16	2	22
22	Crear proyecto	Desactivado	1	3	4	Descripcion modificada	15	16	2	21
16	Crear fase	Desactivado	2	1	5	\N	16	16	2	\N
26	Crear fase	En Linea Base	2	3	5	\N	16	16	2	25
28	Crear item	En Linea Base	3	3	9	\N	17	16	2	27
25	Crear fase	Desactivado	2	2	5	\N	16	16	2	16
17	Crear item	Desactivado	3	1	9	\N	17	16	2	\N
27	Crear item	Desactivado	3	2	9	\N	17	16	2	17
23	Creando un proyecto	Desactivado	1	2	3	1. Entrar a crear proyecto, 2. Seleccionar un Nombre, 3. Guardar cambios	18	17	1	18
29	Creando un proyecto	Desactivado	1	3	3	1. Entrar a crear proyecto, 2. Seleccionar un Nombre, 3. Guardar cambios	18	17	1	23
20	Vista creacion de fase	Desactivado	2	1	7	\N	20	18	4	\N
31	Vista creacion de fase	En Desarrollo	2	2	7	\N	20	18	4	20
34	RF1	Desactivado	1	1	1	\N	34	19	2	\N
35	CU1	Desactivado	1	1	2	\N	35	20	1	\N
38	CU1	Desactivado	1	2	2	\N	35	20	1	35
36	PT3	Desactivado	1	1	5	\N	36	21	4	\N
37	RF1	En Linea Base	1	2	1	\N	34	19	2	34
39	CU1	En Linea Base	1	3	2	\N	35	20	1	38
40	PT3	En Linea Base	1	2	5	\N	36	21	4	36
\.


--
-- Data for Name: configuracion_lineabase_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracion_lineabase_items (id, lineabase_id, item_id) FROM stdin;
1	1	2
2	1	8
3	2	24
4	2	26
5	2	28
6	3	37
7	4	39
8	5	40
\.


--
-- Data for Name: configuracion_solicitud; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracion_solicitud (id, fecha_solicitud, justificacion, solicitud_activa, linea_base_id, solicitado_por_id) FROM stdin;
\.


--
-- Data for Name: configuracion_solicitud_items_a_modificar; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracion_solicitud_items_a_modificar (id, solicitud_id, item_id) FROM stdin;
\.


--
-- Data for Name: configuracion_votoruptura; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracion_votoruptura (id, valor_voto, fecha_voto, solicitud_id, votante_id) FROM stdin;
\.


--
-- Data for Name: desarrollo_atributoparticular; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.desarrollo_atributoparticular (id, nombre, tipo, valor, item_id) FROM stdin;
1	Fecha limite de entrega	date		1
2	Fecha limite de entrega	date	2020-10-30	2
3	Fecha limite de entrega	date		6
4	Fecha limite de entrega	date		8
5	Fecha limite de entrega	date	2020-10-31	18
6	Cantidad de comentarios	number		19
7	Cantidad de comentarios	number		20
8	Fecha limite de entrega	date	2020-11-30	23
9	Fecha limite de entrega	date	2020-11-30	29
10	Fecha limite de entrega	date	2020-11-30	30
11	Cantidad de comentarios	number		31
12	Fecha limite de entrega	date	2020-11-30	32
13	Cantidad de comentarios	number		33
14	Fecha limite de entrega	date		35
15	Cantidad de comentarios	number		36
16	Fecha limite de entrega	date		38
17	Fecha limite de entrega	date		39
18	Cantidad de comentarios	number		40
\.


--
-- Data for Name: desarrollo_item_antecesores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.desarrollo_item_antecesores (id, from_item_id, to_item_id) FROM stdin;
1	7	6
2	9	8
3	10	8
4	11	8
5	12	11
6	13	8
7	14	11
8	14	13
9	29	28
10	30	28
11	31	30
12	32	28
13	33	32
14	38	37
15	39	37
16	40	39
\.


--
-- Data for Name: desarrollo_item_hijos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.desarrollo_item_hijos (id, from_item_id, to_item_id) FROM stdin;
1	24	25
2	26	27
\.


--
-- Data for Name: desarrollo_item_padres; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.desarrollo_item_padres (id, from_item_id, to_item_id) FROM stdin;
1	25	24
2	26	24
3	27	26
4	28	26
\.


--
-- Data for Name: desarrollo_item_sucesores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.desarrollo_item_sucesores (id, from_item_id, to_item_id) FROM stdin;
1	6	7
2	8	7
3	8	9
4	11	12
5	13	14
6	28	29
7	30	31
8	32	31
9	32	33
10	37	38
11	39	40
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-10-05 20:42:33.829521-03
2	contenttypes	0002_remove_content_type_name	2020-10-05 20:42:33.856758-03
3	auth	0001_initial	2020-10-05 20:42:33.916822-03
4	auth	0002_alter_permission_name_max_length	2020-10-05 20:42:33.988278-03
5	auth	0003_alter_user_email_max_length	2020-10-05 20:42:34.005184-03
6	auth	0004_alter_user_username_opts	2020-10-05 20:42:34.014847-03
7	auth	0005_alter_user_last_login_null	2020-10-05 20:42:34.024399-03
8	auth	0006_require_contenttypes_0002	2020-10-05 20:42:34.029575-03
9	auth	0007_alter_validators_add_error_messages	2020-10-05 20:42:34.042765-03
10	auth	0008_alter_user_username_max_length	2020-10-05 20:42:34.057192-03
11	auth	0009_alter_user_last_name_max_length	2020-10-05 20:42:34.068169-03
12	auth	0010_alter_group_name_max_length	2020-10-05 20:42:34.076828-03
13	auth	0011_update_proxy_permissions	2020-10-05 20:42:34.085397-03
14	auth	0012_alter_user_first_name_max_length	2020-10-05 20:42:34.094357-03
15	login	0001_initial	2020-10-05 20:42:34.158083-03
16	admin	0001_initial	2020-10-05 20:42:34.271264-03
17	admin	0002_logentry_remove_auto_add	2020-10-05 20:42:34.323529-03
18	admin	0003_logentry_add_action_flag_choices	2020-10-05 20:42:34.351538-03
19	admin	0004_auto_20200314_0204	2020-10-05 20:42:34.398828-03
20	admin	0005_auto_20200314_0208	2020-10-05 20:42:34.431214-03
21	admin	0006_auto_20200314_0210	2020-10-05 20:42:34.47701-03
22	admin	0007_auto_20200314_0212	2020-10-05 20:42:34.511739-03
23	admin	0008_auto_20200314_0236	2020-10-05 20:42:34.555053-03
24	admin	0009_auto_20200314_0237	2020-10-05 20:42:34.583251-03
25	admin	0010_auto_20200314_0411	2020-10-05 20:42:34.60748-03
26	admin	0011_auto_20200314_0532	2020-10-05 20:42:34.626027-03
27	administracion	0001_initial	2020-10-05 20:42:34.703908-03
28	administracion	0002_auto_20200922_1120	2020-10-05 20:42:34.944551-03
29	desarrollo	0001_initial	2020-10-05 20:42:35.237758-03
30	configuracion	0001_initial	2020-10-05 20:42:35.421038-03
31	configuracion	0002_auto_20200922_1120	2020-10-05 20:42:35.635107-03
32	sessions	0001_initial	2020-10-05 20:42:35.763021-03
33	sites	0001_initial	2020-10-05 20:42:35.793372-03
34	sites	0002_alter_domain_unique	2020-10-05 20:42:35.816749-03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
so54urdt8mov2txuiou5djbeelhxgbsv	.eJxVjMsKwjAQRf8la5HUvLsU3PkPIZOZ2KCkpbGgiP9usrObC_fcx4f5sD0nv1VafUY2MsEO_wxCvFPpwWO-5XK8dj03eCm4M_vZFOrUNkTaRqdSdIIkDEZZ3gglLg0qN1iJBgAjOBSWhNPJIQbAE3FuWlH100q15rl4ei15fbNRaM6_P397PDs:1kLwBa:4eTxkcXeTW1Vfkt6WpF5-v39LmLKlKZvRkKD8SNv7V4	2020-09-25 19:27:26.958723-04
9djn8h89bv9rk1t3v5d2o52yzq766dep	.eJxVi8EOwiAQRP9lz8aAQGE9mnjzHwjLLtJoMGntyfTfS2_2Msm8mfeDmJZvjcssUxwZrqDh9M8o5Ze0fXh_nmM7P_a8dXhvfChHraa5dkdkCBldyWjEkvYuqE6kKOvZoQ6WPRFnQjZBDA4FmRPxRZTy_ehg3QBo3TRj:1kPadr:VJrGcn2D0wjNOqhxDwxA4UAWVDXzqcdqIz-i3sgsDE4	2020-10-19 21:15:43.305243-03
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: login_usuario_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.login_usuario_groups (id, usuario_id, group_id) FROM stdin;
\.


--
-- Data for Name: login_usuario_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.login_usuario_user_permissions (id, usuario_id, permission_id) FROM stdin;
\.


--
-- Name: administracion_fase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_fase_id_seq', 21, true);


--
-- Name: administracion_fase_tipos_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_fase_tipos_item_id_seq', 9, true);


--
-- Name: administracion_plantillaatributo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_plantillaatributo_id_seq', 2, true);


--
-- Name: administracion_proyecto_comite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_proyecto_comite_id_seq', 15, true);


--
-- Name: administracion_proyecto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_proyecto_id_seq', 7, true);


--
-- Name: administracion_proyecto_participantes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_proyecto_participantes_id_seq', 28, true);


--
-- Name: administracion_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_rol_id_seq', 8, true);


--
-- Name: administracion_tipoitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_tipoitem_id_seq', 4, true);


--
-- Name: administracion_tipoitem_proyecto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_tipoitem_proyecto_id_seq', 15, true);


--
-- Name: administracion_usuarioxrol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.administracion_usuarioxrol_id_seq', 9, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 72, true);


--
-- Name: configuracion_lineabase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configuracion_lineabase_id_seq', 5, true);


--
-- Name: configuracion_lineabase_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configuracion_lineabase_items_id_seq', 8, true);


--
-- Name: configuracion_solicitud_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configuracion_solicitud_id_seq', 1, false);


--
-- Name: configuracion_solicitud_items_a_modificar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configuracion_solicitud_items_a_modificar_id_seq', 1, false);


--
-- Name: configuracion_votoruptura_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configuracion_votoruptura_id_seq', 1, false);


--
-- Name: desarrollo_atributoparticular_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.desarrollo_atributoparticular_id_seq', 18, true);


--
-- Name: desarrollo_item_antecesores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.desarrollo_item_antecesores_id_seq', 16, true);


--
-- Name: desarrollo_item_hijos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.desarrollo_item_hijos_id_seq', 2, true);


--
-- Name: desarrollo_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.desarrollo_item_id_seq', 40, true);


--
-- Name: desarrollo_item_padres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.desarrollo_item_padres_id_seq', 4, true);


--
-- Name: desarrollo_item_sucesores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.desarrollo_item_sucesores_id_seq', 11, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 18, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 26, true);


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_site_id_seq', 1, true);


--
-- Name: login_usuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.login_usuario_groups_id_seq', 1, false);


--
-- Name: login_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.login_usuario_id_seq', 8, true);


--
-- Name: login_usuario_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.login_usuario_user_permissions_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

