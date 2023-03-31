from django.shortcuts import render

# Create your views here.

# HOME PAGE
def home(request):
    return render(request, 'home.html')
    
# ABOUT PAGE    
def about(request):
    return render(request, 'about.html')

# POST A JOB PAGE
def job_post(request):
    return render(request, 'jobpost.html')

# NEAR JOB PAGE
def near_job(request):
    return render(request, 'nearjob.html')