from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView, SignupView, ResetPasswordView, ChangePasswordView
# from .views import CreateProfileView
from .forms import LoginForm
import secrets

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='authorization/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('create-profile/', CreateProfileView.as_view(), name='create_profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authorization/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authorization/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/', views.profile, name='users_profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
