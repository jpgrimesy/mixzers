from django.urls import path
from . import views
from .models import Mixzer

urlpatterns = [
    path('mixzer/signup/', views.signup, name='signup'),
]
