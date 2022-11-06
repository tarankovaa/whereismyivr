import secrets

from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
# from .forms import UserEmailForm, UsernameForm, UserPasswordForm
from .forms import LoginForm, SignupForm, ProfileForm
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from .tokens import account_activation_token


class SignupView(View):
    form_class = SignupForm
    template_name = 'authorization/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(SignupView, self).dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class CreateProfileView(View):
    form_class = ProfileForm
    template_name = 'authorization/create_profile.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            profile = user.profile
            profile.profile_pic = form.cleaned_data.get('profile_pic')
            profile.profile_type = form.cleaned_data.get('profile_type')
            profile.telegram_username = form.cleaned_data.get('telegram_username')
            profile.vk_username = form.cleaned_data.get('vk_username')
            profile.is_filled = True
            user.save()
            profile.save()
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.profile.is_filled:
            return redirect('home')
        return super(CreateProfileView, self).dispatch(request, *args, **kwargs)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authorization/password_reset.html'
    email_template_name = 'authorization/password_reset_email.html'
    subject_template_name = 'authorization/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


def activateEmail(request, user, to_email):
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
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and not user.is_active and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    elif user and user.is_active:
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')


'''def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    form = SignupForm()
    return render(request, 'authorization/signup.html', {'form': form})'''


'''def sign_up_password(request, user):
    if not user.email:
        return redirect("signup")
    if request.method == "POST":
        form = UserPasswordForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['password'])
            user.password = form.cleaned_data['password']
            return redirect('signup_username', user=user)
    form = UserPasswordForm()
    context = {
        'field': form['password'],
    }
    return render(request, 'authorization/signup.html', context)


def sign_up_username(request, user):
    if not user.password:
        return redirect("signup")
    if request.method == "POST":
        form = UsernameForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            return redirect('login')
    form = UsernameForm()
    context = {
        'field': form['username'],
    }
    return render(request, 'authorization/signup.html', context)'''


'''def log_in(request):
    return render(request, 'authorization/login.html')'''
