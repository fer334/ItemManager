from django.contrib import admin

# Register your models here.
from administracion.models import TipoItem, PlantillaAtributo,Proyecto

admin.site.register(TipoItem)
admin.site.register(PlantillaAtributo)
admin.site.register(Proyecto)