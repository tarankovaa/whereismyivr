from django import forms
from django.forms import ModelForm
from .models import Card


class CreateCardForm(ModelForm):
    class Meta:
        model = Card
        fields = ['title', 'type_of_app', 'customer', 'consultant', 'performer', 'partner', 'product_image']
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название',
            }),
            "product_image": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите образ продукта',
            }),
        }
