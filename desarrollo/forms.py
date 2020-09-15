"""
Formularios para la aplicacion administración
"""
from django import forms
from desarrollo.models import Item


class ItemForm(forms.ModelForm):
    """
    Formulario para la creación de ítems
    """

    class Meta:
        model = Item
        fields = ('nombre', 'complejidad', 'descripcion')
        help_texts = {
            'complejidad': 'número entero entre 1 y 10',
        }

    def __init__(self, *args, **kwargs):
        """
        Añadimos al constructor de la clase las restricciones de que el campo complejidad solo pueda tomar valores
        entre 1 y 10 y modificamos el campo descripcion para que no sea requerido
        """
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['complejidad'].widget.attrs['min'] = 1
        self.fields['complejidad'].widget.attrs['max'] = 10
        self.fields['descripcion'].required = False

    def clean_complejidad(self):
        """
        modificamos clean_data de complejidad para que controle que el valor esté entre 1 y 10

        :return: retornará el valor de complejidad o alzará un error de validacion
        """
        complejidad = self.cleaned_data['complejidad']
        if complejidad > 10 or complejidad < 1:
            raise forms.ValidationError('Tiene que estar en el rango de [1,10].')
        return complejidad


class EditarItemForm(forms.Form):
    """Formulario para la modificar Items"""

    nombre = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                          'value': 'Item'}))
    complejidad = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'numberinput form-control',
                                                                                  'type': 'number',
                                                                                  'min': '1', 'max': '10',
                                                                                  'value': '5'}))
    descripcion = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3',
                                                                              'value': ''}))

    def __init__(self, *args, **kwargs):
        super(EditarItemForm, self).__init__(*args, **kwargs)