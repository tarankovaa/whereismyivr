from django import forms
from django.forms import ModelForm
from .models import Card


class CreateCardForm(ModelForm):

    class Meta:
        model = Card
        fields = ['title', 'type_of_card', 'field_of_card', 'customer', 'consultant', 'performer', 'partner',
                  'product_image']
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название',
                'required': True,
            }),
            "type_of_card": forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            }),
            "product_image": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите образ продукта',
                'rows': 7,
                'required': True,
            }),
            "field_of_card": forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            })
        }
