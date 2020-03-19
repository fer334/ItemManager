from django import forms
from django.utils import timezone


class ProyectoForm(forms.Form):
    nombre = forms.CharField(label='Nombre del Proyecto', max_length=200,
                             widget=forms.TextInput(attrs={'placeholder': 'Ej. Proyecto 1'}))
    fecha_inicio = forms.DateField(label='Fecha de Inicio', initial=timezone.now(),
                                   widget=forms.TextInput(attrs={'placeholder': 'Ej. 2020-09-28'}))
    numero_fases = forms.IntegerField(label='Numero de fases del proyecto:', min_value=1,
                                      widget=forms.TextInput(attrs={'placeholder': 'Ej. 7'}))
    gerente = forms.CharField(label='Gerente del proyecto', max_length=200,
                              widget=forms.TextInput(attrs={'placeholder': 'Ej. Pedro Parques'}))
    cant_comite = forms.IntegerField(label='Cantidad De Miembros del Comité', min_value=3,
                                     widget=forms.TextInput(attrs={'placeholder': '(obs: nro. impar >=3) Ej. 5'}))

