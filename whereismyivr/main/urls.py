from django.urls import path
from . import views
from .views import CreateCardView

urlpatterns = [
    path('', views.index, name='home'),
    path('search/<param>', views.search),
    path('create-card/', CreateCardView.as_view(), name='create_card')
]
