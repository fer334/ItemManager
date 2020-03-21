from django import forms
from django.utils import timezone
from login.models import Usuario


class ProyectoForm(forms.Form):

    nombre = forms.CharField(label='Nombre del Proyecto', max_length=200,
                             widget=forms.TextInput(attrs={'placeholder': 'Ej. Proyecto 1', 'size': 35}),
                             )
    fecha_inicio = forms.DateField(label='Fecha de Inicio', initial=timezone.now().date(),
                                   widget=forms.TextInput(attrs={'placeholder': 'Ej. 2020-09-28', 'type': 'date'}))
    numero_fases = forms.IntegerField(label='Numero de fases del proyecto:', min_value=1,
                                      widget=forms.TextInput(attrs={'placeholder': 'Ej. 7', 'size': 35}))
    cant_comite = forms.IntegerField(label='Cantidad De Miembros del Comité', min_value=3,
                                     help_text='obs: nro. impar >=3',
                                     widget=forms.TextInput(attrs={'placeholder': 'Ej. 5', 'size': 35}))
    gerente = forms.ChoiceField(label='Gerente del proyecto', choices=[('', '')])

    # init para evitar problemas de migraciones con choice cuando la base de datos aun no se creó
    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['gerente'].choices = [('', '')] + [(x.localId, x.username) for x in Usuario.objects.all()]

    def clean_cant_comite(self):
        cant_comite = self.cleaned_data['cant_comite']
        if cant_comite % 2 == 0:
            raise forms.ValidationError('Tiene que ser impar.')
        return cant_comite


class ParticipanteForm(forms.Form):

    participantes = forms.MultipleChoiceField(label='Usuarios Participantes:', choices=[('', '')])

    # init para evitar problemas de migraciones con choice cuando la base de datos aun no se creó
    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['participantes'].choices = [('', '')] + [(x.localId, x.username) for x in Usuario.objects.all()]
