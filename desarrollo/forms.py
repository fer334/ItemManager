"""
Formularios para la aplicacion administración
"""
from django import forms
from desarrollo.models import Item, AtributoParticular, Relacion


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


class RelacionForm(forms.ModelForm):
    """
    Formulario para la creacion de relaciones entre items
    """

    class Meta:
        model = Relacion
        fields = ('inicio', 'fin')

    def clean(self):
        """
        Verifica los datos del formulario.

        :return: los datos limpiados
        """
        data = super().clean()
        inicio = data['inicio']
        fin = data['fin']

        # no se puede relacionar a si mismo
        if inicio.id == fin.id:
            raise forms.ValidationError('No se puede relacionar un item a si mismo')
        if abs(inicio.fase.id - fin.fase.id) > 1:
            raise forms.ValidationError(
                'Solo se puede relacionar items de la misma fase o fases inmediatas'
            )
        if inicio.fase.id - fin.fase.id == 1:
            raise forms.ValidationError(
                'Las relaciones entre fases deben ser hacia fases posteriores'
            )
        if Relacion.objects.filter(inicio=inicio, fin=fin, is_active=True).count() > 0:
            raise forms.ValidationError(
                'Esta relacion ya existe'
            )

        return data
