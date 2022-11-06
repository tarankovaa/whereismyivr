from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, SignupView, CreateProfileView
from .forms import LoginForm
import secrets

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='authorization/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create-profile/', CreateProfileView.as_view(), name='create-profile')
]
