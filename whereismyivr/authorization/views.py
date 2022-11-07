from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView
from django.core.mail import EmailMessage
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.safestring import mark_safe
from django.views import View

from .forms import LoginForm, SignupForm, UpdateUserForm, UpdateProfileForm
from .tokens import account_activation_token


class SignupView(View):
    # обработка страницы регистрации пользователя
    form_class = SignupForm
    template_name = 'authorization/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # регистрация нового пользователя
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        # ограничение доступа к странице
        if request.user.is_authenticated:
            return redirect('home')
        return super(SignupView, self).dispatch(request, *args, **kwargs)


def activateEmail(request, user, to_email):
    # отправка ссылки для активации на email
    mail_subject = 'where is my ivr? Активируйте ваш аккаунт'
    message = render_to_string('authorization/activate_account_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'''Пожалуйста, перейдите в почтовый ящик адреса {to_email} и 
        нажмите на ссылку активации. Если вы не получили письмо, проверьте папку со спамом''')
    else:
        messages.error(request,
                       f'''Возникла проблема при отправлении письма подтверждения по адресу {to_email},
                        убедитесь, что ввели адрес корректно''')


def activate(request, uidb64, token):
    # обработка активации пользователя
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and not user.is_active and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, mark_safe(
            'Спасибо за подтверждение электронной почты. Теперь вы можете войти в аккаунт'))
        return redirect('login')
    elif user and user.is_active:
        return redirect('home')
    else:
        messages.error(request, 'Ссылка активации некорректна!')
    return redirect('home')


class CustomLoginView(LoginView):
    # расширение функционала класса входа
    form_class = LoginForm

    def form_valid(self, form):
        # обработка поля Запомнить меня
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    # настройка параметров сброса пароля
    template_name = 'authorization/password_reset.html'
    email_template_name = 'authorization/password_reset_email.html'
    subject_template_name = 'authorization/password_reset_subject'
    success_message = '''Мы отправили на ваш адрес инструкцию по сбросу пароля. Если вы не получили письмо, убедитесь, 
    что введенный адрес совпадает с указанным при регистрации и проверьте спам'''
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    # настройка параметров смены пароля
    template_name = 'authorization/change_password.html'
    success_message = "Пароль успешно изменен"
    success_url = reverse_lazy('home')


@login_required
def profile(request):
    # страница редактирования профиля пользователя
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            prof = profile_form.save()
            prof.is_filled = True
            prof.save()
            messages.success(request, 'Данные профиля успешно обновлены')
            return redirect('users_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'authorization/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def change_email(request):
    # смена email (не реализовано)
    messages.error(request, "К сожалению, в настоящее время невозможно изменить электронный адрес. Попробуйте позже")
    return redirect('users_profile')
