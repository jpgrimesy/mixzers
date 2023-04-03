from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # path to the self-reflection profile
    path('profile/', views.profile, name='profile'),

    # path to account profile. we need to make a test
    # page of all the information for others to view the specifc user

    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify, name="verify"),
    path('send-message/<int:user_id>/', views.send_message, name="send_message"),
    path('create-review/<int:user_id>/', views.create_review, name="create_review"),
    path('post-job/', views.post_job, name='post_job'),
    path('nearby-jobs/', views.nearby_jobs, name='nearby_jobs'),
    path('apply/<int:job_id>/', views.apply, name='apply'),
    path('hire/<int:job_id>/', views.hire, name='hire'),
]
