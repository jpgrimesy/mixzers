from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Mixzer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    is_student = models.BooleanField(default=False)
    college = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=18, blank=True)

    def verify_student(self):
        return self.user.email.endswith('.edu')

    def get_absolute_url(self):
        return reverse('mixzer_detail', kwargs={'pk': self.id})


class Message(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=250)
    sender = models.ForeignKey(
        Mixzer, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(
        Mixzer, on_delete=models.CASCADE, related_name='recipient')
    created_on = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=250)
    rating = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviewer = models.ForeignKey(
        Mixzer, on_delete=models.CASCADE, related_name='reviewer')
    reviewee = models.ForeignKey(
        Mixzer, on_delete=models.CASCADE, related_name='reviewee')
    created_on = models.DateTimeField(auto_now_add=True)


class Job_Post(models.Model):
    title = models.CharField(max_length=250)
    job_description = models.TextField(max_length=250)
    job_type = models.CharField(max_length=250)
    salary = models.CharField(max_length=250)
    schedule = models.CharField(max_length=250)
    applicants = models.ManyToManyField(Mixzer, related_name='applicants')
    candidates = models.ManyToManyField(Mixzer, related_name='candidates')
    author = models.ForeignKey(
        Mixzer, on_delete=models.CASCADE, related_name='author')
