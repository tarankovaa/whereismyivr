from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Введите электронную почту',
                             }))
    username = forms.CharField(max_length=32,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Введите имя пользователя',
                               }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите пароль',
                                }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Повторите пароль',
                                }))

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("Данный электронный адрес используется другим аккаунтом.")
        return data


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=32,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Введите имя пользователя',
                               }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Введите пароль',
                               }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=32,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                               }))
    first_name = forms.CharField(max_length=50,
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                 }))
    last_name = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                }))

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic', 'profile_type', 'telegram_username', 'vk_username']
        widgets = {
            "profile_pic": forms.FileInput(attrs={
                'class': 'form-control',
            }),
            "telegram_username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш ник в Telegram',
            }),
            "vk_username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваш ник в VK',
            }),
            "profile_type": forms.Select(attrs={
                'class': 'form-control',
                'required': True,
            })
        }
