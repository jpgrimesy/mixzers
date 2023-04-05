import os, requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from .forms import UserForm, AddExtraUserCreationForm, MessageForm, ReviewForm, JobPostForm
from .models import Mixzer, Message, Review, Job_Post, JobPoint
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin



def get_coordinates(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': os.environ['GOOGLE_API_KEY']}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['status'] == 'OK':
            location = result['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
    return None
# Create your views here.

# HOME PAGE  
def home(request):
    return render(request, 'home.html')


# ABOUT PAGE
def about(request):
    return render(request, 'about.html')


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
            return redirect('/profile/')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    add_form = AddExtraUserCreationForm()
    addtl_form = UserForm()
    context = {'form': form, 'add_form': add_form,
               'addtl_form': addtl_form, 'error_message': error_message}
    return render(request, 'test.html', context)


# PROFILE PAGE, TEST PAGE MADE JUST TO SHOW INFO
@login_required
def profile(request):
    user = Mixzer.objects.get(user=request.user)
    user_messages = Message.objects.filter(recipient=user)
    reviews = Review.objects.filter(reviewee=user)
    return render(request, 'test_profile.html', {
        'abc': user,
        'user_messages': user_messages,
        'reviews': reviews
    })


# VERIFIES EDU EMAIL
@login_required
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


@login_required
def send_message(request, user_id):
    sender = Mixzer.objects.get(user=request.user)
    recipient = Mixzer.objects.get(id=user_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()
            return redirect('profile')
    form = MessageForm()
    return render(request, 'main_app/message_form.html', {
        'form': form
    })


@login_required
def create_review(request, user_id):
    reviewer = Mixzer.objects.get(user=request.user)
    reviewee = Mixzer.objects.get(id=user_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = reviewer
            review.reviewee = reviewee
            review.save()
            return redirect('profile')
    form = ReviewForm()
    return render(request, 'main_app/message_form.html', {
        'form': form
    })


@login_required
def post_job(request):
  author = Mixzer.objects.get(user=request.user)
  if request.method == 'POST':
    form = JobPostForm(request.POST)
    if form.is_valid():
      post = form.save(commit=False)
      post.author = author
      post.save()
      location = author.location
      coordinates = get_coordinates(location)
      job_point = JobPoint(job_post=post, location=Point(coordinates))
      job_point.save()
      return redirect('nearby_jobs')
  form = JobPostForm()
  return render(request, 'jobpost.html', {
    'form': form
  })


@login_required
def nearby_jobs(request):
  user_location = get_coordinates(request.user.mixzer.location)
  jobs = Job_Post.objects.filter(jobpoint__location__distance_lte=(Point(user_location), Distance(mi=20)))
  return render(request, 'nearjob.html', {
    'jobs': jobs
  })


@login_required
def apply(request, job_id):
    user = Mixzer.objects.get(user=request.user)
    Job_Post.objects.get(id=job_id).applicants.add(user.id)
    return redirect('nearby_jobs')


@login_required
def hire(request, job_id):
    user = Mixzer.objects.get(user=request.user)
    Job_Post.objects.get(id=job_id).candidates.add(user.id)
    return redirect('nearby_jobs')


class MixzerDetail(LoginRequiredMixin, DetailView):
    model = Mixzer


# JOB POST UPDATE VIEW
class PostJobUpdate(LoginRequiredMixin, UpdateView):
  model = Job_Post
  fields = '__all__'


# JOB POST DELETE VIEW
class PostJobDelete(LoginRequiredMixin, DeleteView):
  model = Job_Post
  success_url = '/profile/'


# PROFILE UPDATE VIEW
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Mixzer
    fields = ['location', 'is_student', 'college', 'phone_number']


# PROFILE DELETE VIEW
class ProfileDelete(LoginRequiredMixin, DeleteView):
  model=Mixzer
  success_url='/'

