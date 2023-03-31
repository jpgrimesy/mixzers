from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('job_post/', views.near_job, name="job_post"),
    path('near_job/', views.near_job, name='near_job'),

]
