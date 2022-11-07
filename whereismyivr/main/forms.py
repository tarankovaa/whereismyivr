from django import forms
from django.forms import ModelForm, Form
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


class FilterForm(Form):
    it_project = forms.BooleanField(required=False)
    business_project = forms.BooleanField(required=False)
    design = forms.BooleanField(required=False)
    publishing = forms.BooleanField(required=False)
    engineering = forms.BooleanField(required=False)
    media = forms.BooleanField(required=False)
    education_project = forms.BooleanField(required=False)
    events = forms.BooleanField(required=False)
    it_research = forms.BooleanField(required=False)
    business_research = forms.BooleanField(required=False)
    oriental_studies = forms.BooleanField(required=False)
    natural_sciences = forms.BooleanField(required=False)
    art = forms.BooleanField(required=False)
    history = forms.BooleanField(required=False)
    culturology = forms.BooleanField(required=False)
    marketing = forms.BooleanField(required=False)
    maths = forms.BooleanField(required=False)
    management = forms.BooleanField(required=False)
    linguistics = forms.BooleanField(required=False)
    education_research = forms.BooleanField(required=False)
    politics = forms.BooleanField(required=False)
    right = forms.BooleanField(required=False)
    psychology = forms.BooleanField(required=False)
    sociology = forms.BooleanField(required=False)
    philology = forms.BooleanField(required=False)
    philosophy = forms.BooleanField(required=False)
    economy = forms.BooleanField(required=False)