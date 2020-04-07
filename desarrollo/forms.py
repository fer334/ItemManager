from django import forms
from desarrollo.models import Item, AtributoParticular


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('nombre', 'complejidad', 'descripcion')
