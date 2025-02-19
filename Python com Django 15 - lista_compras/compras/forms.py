from django import forms
from .models import Nota, Item

class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['nome_produto', 'quantidade_peso', 'preco']
