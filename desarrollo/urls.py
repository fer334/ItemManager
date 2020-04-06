from django.urls import path

from desarrollo import views

app_name = 'desarrollo'
urlpatterns = [
    # URLs de Mati
    path('desarrollo/<int:id_proyecto>/<int:id_tipo>', views.crear_item, name='crearItem'),
]
