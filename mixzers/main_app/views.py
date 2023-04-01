from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserForm, AddExtraUserCreationForm
from .models import Mixzer
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
    

# SIGNUP PAGE, STILL NEED TO FIX THE REDIRECTS 
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    add_form = AddExtraUserCreationForm(request.POST)
    addtl_form = UserForm(request.POST)
    if form.is_valid() and addtl_form.is_valid() and add_form.is_valid():
      user = form.save()
      add_user = add_form.save(commit=False)
      user.email = add_user.email
      user.first_name = add_user.first_name
      user.last_name = add_user.last_name
      form.save()
      addtl_user = addtl_form.save(commit=False)
      addtl_user.user = user
      addtl_user.save()
      login(request, user)
      return redirect('/admin/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  add_form = AddExtraUserCreationForm()
  addtl_form = UserForm()
  context = {'form': form, 'add_form': add_form, 'addtl_form': addtl_form ,'error_message': error_message}
  return render(request, 'test.html', context)


# PROFILE PAGE, TEST PAGE MADE JUST TO SHOW INFO
def profile(request):
  user = Mixzer.objects.get(user=request.user)
  return render(request, 'test_profile.html', {
    'user': user
  })
  

# VERIFIES EDU EMAIL
def verify(request):
  user = Mixzer.objects.get(user=request.user)
  verified = user.verify_student()

  if verified:
    user.is_student = verified
    user.save()
  else:
    error_message = 'E-mail must be .edu to be verified'
    messages.error(request, error_message)

  return redirect('profile')
