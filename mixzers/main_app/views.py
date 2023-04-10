import os, requests, uuid, boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from .forms import UserForm, AddExtraUserCreationForm, MessageForm, ReviewForm, JobPostForm, AddCollegeForm, ChangeRadius
from .models import Mixzer, Message, Review, Job_Post, JobPoint, Photo
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView, UpdateView
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


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


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


@login_required
def profile(request):
    user = Mixzer.objects.get(user=request.user)
    user_messages = Message.objects.filter(recipient=user)
    reviews = Review.objects.filter(reviewee=user)
    jobs = Job_Post.objects.filter(author=user)
    applied = Job_Post.objects.filter(applicants=user)
    return render(request, 'test_profile.html', {
        'mixzer': user,
        'user_messages': user_messages,
        'reviews': reviews,
        'jobs': jobs,
        'applied': applied
    })


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
    return render(request, 'main_app/review_form.html', {
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
      return redirect('profile')
  form = JobPostForm()
  return render(request, 'jobpost.html', {
    'form': form
  })


@login_required
def nearby_jobs(request):
    user_location = get_coordinates(request.user.mixzer.location)
    radius = 10
    if request.method == 'POST':
        form = ChangeRadius(request.POST)
        if form.is_valid():
            radius = form.cleaned_data['radius']
            jobs = Job_Post.objects.filter(jobpoint__location__distance_lte=(Point(user_location), Distance(mi=radius)))
    else:
        form = ChangeRadius(initial={'radius': radius})
        jobs = Job_Post.objects.filter(jobpoint__location__distance_lte=(Point(user_location), Distance(mi=radius)))
    
    return render(request, 'nearjob.html', {
        'jobs': jobs,
        'form': form,
        'radius': radius
    })


@login_required
def apply(request, job_id):
    user = Mixzer.objects.get(user=request.user)
    Job_Post.objects.get(id=job_id).applicants.add(user.id)
    return redirect('nearby_jobs')


@login_required
def hire(request, job_id, mixzer_id):
    mixzer = Mixzer.objects.get(id=mixzer_id)
    Job_Post.objects.get(id=job_id).candidates.add(mixzer.id)
    return redirect('nearby_jobs')


class MixzerDetail(LoginRequiredMixin, DetailView):
    model = Mixzer

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['reviews'] = Review.objects.filter(reviewee=self.object)
      return context


class PostJobUpdate(UpdateView):
    model = Job_Post
    fields = ['title', 'job_description',
              'job_type', 'salary', 'schedule']
    success_url = '/profile/'

    def get_absolute_url(self):
        return reverse('post_job_update', kwargs={'job_id': self.id})


class PostJobDelete(LoginRequiredMixin, DeleteView):
    model = Job_Post
    success_url = '/profile/'


def delete_user(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.mixzer.delete()
        user.delete()
        return redirect('/')
    return render(request, 'main_app/mixzer_confirm_delete.html')


@login_required
def update_profile(request):
    error_message = ''
    if request.method == 'POST':
        add_form = AddExtraUserCreationForm(
            request.POST, instance=request.user)
        addtl_form = UserForm(request.POST, instance=request.user.mixzer)
        college_form = AddCollegeForm(request.POST, instance=request.user.mixzer)
        if add_form.is_valid() and addtl_form.is_valid():
            add_form.save()
            addtl_form.save()
            college_form.save()
            return redirect('/profile/')
        else:
            error_message = 'Invalid - try again'

    add_form = AddExtraUserCreationForm(instance=request.user)
    addtl_form = UserForm(instance=request.user.mixzer)
    college_form = AddCollegeForm(instance=request.user.mixzer)
    context = {
        'add_form': add_form, 'addtl_form': addtl_form, 'college_form': college_form, 'error_message': error_message}
    return render(request, 'mixzer_form.html', context)


@login_required
def add_photo(request, user_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, mixzer_id=user_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('profile')
