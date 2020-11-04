from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, TA_CENTER
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.platypus import (
    Paragraph,
    Table,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
    Paragraph)

from administracion.models import Proyecto, Fase
from configuracion.models import Solicitud
from desarrollo.models import Item


class ReporteProyecto(object):

    def __init__(self):
        self.buf = BytesIO()

    def run(self, id_proyecto, fases, fecha_ini, fecha_fin):
        self.doc = SimpleDocTemplate(self.buf)
        self.story = []
        self.titulo()
        proyecto = Proyecto.objects.get(pk=id_proyecto)
        try:
            for id_fase in fases:
                fase = Fase.objects.get(pk=id_fase)
                self.encabezado("Items de la fase: "+fase.nombre)
                self.crearTabla(fase.item_set.all())
        except:
            self.encabezado("No ha seleccionado fases")

        self.encabezado("Informe de todos los items pendiente y en desarrollo")
        self.tabla_items_proyecto(proyecto)

        self.solicitudes(fecha_ini, fecha_fin)

        self.doc.build(self.story, onFirstPage=self.numeroPagina,
                       onLaterPages=self.numeroPagina)
        pdf = self.buf.getvalue()
        self.buf.close()
        return pdf

    def titulo(self):
        p = Paragraph("Reporte Proyecto", self.estiloPC())
        self.story.append(p)
        self.story.append(Spacer(1, 0.5 * inch))

    def encabezado(self, nombre):
        p = Paragraph(nombre, self.estiloPC())
        self.story.append(p)
        self.story.append(Spacer(1, 0.1 * inch))

    def solicitudes(self, fecha_ini, fecha_fin):
        solicitudes = Solicitud.objects.filter(fecha_solicitud__range=[fecha_ini, fecha_fin])
        num = len(solicitudes)
        texto = 'En el rango: {0}/{1}/{2}-{3}/{4}/{5}. '.format(fecha_ini.day,fecha_ini.month,fecha_ini.year,fecha_fin.day,fecha_fin.month,fecha_fin.year)
        if num ==1:
            p1 = Paragraph(texto +"Se tiene una solicitud", self.estiloPC())
        else:
            p1 = Paragraph(texto +"Se tiene "+str(num)+" solicitudes", self.estiloPC())
        self.story.append(p1)
        self.story.append(Spacer(1, 0.1 * inch))

    def crearTabla(self, items):
        data = [["Id", "Nombre", "Estado"]] \
               + [[x.id, x.nombre, x.estado]
                  for x in items if x == Item.objects.filter(id_version=x.id_version).order_by('id').last()]

        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ])

        t = Table(data)
        t.setStyle(style)
        self.story.append(t)
        self.story.append(Spacer(1, 0.5 * inch))

    def tabla_items_proyecto(self, proyecto):
        items = []
        for f in proyecto.fase_set.all():
            for i in f.item_set.all():
                if i.estado in [Item.ESTADO_PENDIENTE,Item.ESTADO_DESARROLLO]:
                    if i == Item.objects.filter(id_version=i.id_version).order_by('id').last():
                        items.append(i)

        data = [["Id", "Nombre", "Estado"]] \
               + [[x.id, x.nombre, x.estado]
                  for x in items]

        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ])

        t = Table(data)
        t.setStyle(style)
        self.story.append(t)
        self.story.append(Spacer(1, 0.5 * inch))

    def estiloPC(self):
        return ParagraphStyle(name="centrado", alignment=TA_CENTER)

    def numeroPagina(self, canvas, doc):
        num = canvas.getPageNumber()
        text = "Pagina %s" % num
        canvas.drawRightString(200 * mm, 20 * mm, text)
