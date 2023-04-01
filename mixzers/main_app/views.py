from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import UserForm
from .models import Mixzer
# Create your views here.


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    addtl_form = UserForm(request.POST)
    if form.is_valid() and addtl_form.is_valid():
      user = form.save()
      addtl_user = addtl_form.save(commit=False)
      addtl_user.user = user
      addtl_user.save()
      login(request, user)
      return redirect('/admin/')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  addtl_form = UserForm()
  context = {'form': form, 'add_form': addtl_form ,'error_message': error_message}
  return render(request, 'test.html', context)


def profile(request):
  user = Mixzer.objects.filter(user=request.user)
  return render(request, 'test_profile.html', {
    'user': user[0]
  })