from django.urls import path
from . import views
from .models import Mixzer

urlpatterns = [
    path('', views.profile, name='home'),
    path('mixzer/signup/', views.signup, name='signup'),
    path('verify/', views.verify, name="verify"),
]
