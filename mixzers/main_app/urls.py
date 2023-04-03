from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('job_post/', views.near_job, name="jobpost"),
    path('near_job/', views.near_job, name='nearjob'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify, name="verify"),
    path('send-message/<int:user_id>/', views.send_message, name="send_message"),
    path('create-review/<int:user_id>/', views.create_review, name="create_review"),
]
