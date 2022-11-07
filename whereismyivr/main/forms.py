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


'''class FilterForm(ModelForm):
    it = forms.BooleanField(required=False) IT
    business = forms.BooleanField(required=False) Бизнес
    design = forms.BooleanField(required=False) Дизайн
    publishing = forms.BooleanField(required=False) Издательское дело
    engineering = forms.BooleanField(required=False) Инженерия
    media = forms.BooleanField(required=False) Медиа
    education = forms.BooleanField(required=False) Образование
    events = forms.BooleanField(required=False) Организация событий
    oriental_studies = forms.BooleanField(required=False) Востоковедение
    natural_sciences = forms.BooleanField(required=False) Естественные науки
    art = forms.BooleanField(required=False) Искусствоведение
    history = forms.BooleanField(required=False) История
    culturology = forms.BooleanField(required=False) Культурология
    marketing = forms.BooleanField(required=False) Маркетинг
    maths = forms.BooleanField(required=False) Математика
    management = forms.BooleanField(required=False) Менеджмент
    linguistics = forms.BooleanField(required=False) Лингвистика
    politics = forms.BooleanField(required=False) Политология
    right = forms.BooleanField(required=False) Право
    psychology = forms.BooleanField(required=False) Психология
    sociology = forms.BooleanField(required=False) Социология
    philology = forms.BooleanField(required=False) Филология
    philosophy = forms.BooleanField(required=False) Философия
    economy = forms.BooleanField(required=False) Экономика

    class Meta:
        class Meta:
            fields = ['it', 'business', 'design', 'publishing', 'engineering', 'media', 'education', 'events',
                      'oriental_studies', 'natural_sciences', 'art', 'history', 'culturology', 'marketing', 'maths',
                      'management', 'linguistics', 'politics', 'right', 'psychology', 'sociology', 'philology',
                      'philosophy', 'economy']'''