"""
Formularios para la aplicacion de desarrollo
"""
# Django
from django import forms
from django.utils import timezone

from django import forms


class GeeksForm(forms.Form):
    name = forms.CharField()
    geeks_field = forms.FileField()


class ItemForm(forms.Form):
    """Formulario para la creación de items"""

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

    archivo_adjunto = forms.FileField(required=False, widget=forms.FileInput(attrs={'class' : ''}))


