from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# EMPLOYER MODEL
class Employer(models.Model):
    name = models.CharField(max_length=250)
    # location

# STUDENT MODEL
# emily: to be completed on her end


class Student (models.Model):
    name = models.CharField(max_length=250)
    # location
    # primary key to be incorporated

# MESSAGE MODEL


class Message(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=250)
    # sender_id with foriegn key to be added
    # recipient_id with foriegn key to be added

# REVIEW MODEL
# emily for review model to commit on her end


class Review(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=250)
    # reviewer_id with foriegn key to be added
    # reviewee_id with foriegn key to be added

# JOB POST MODEL


class Job_Post(models.Model):
    title = models.CharField(max_length=250)
    job_description = models.TextField(max_length=250)
    location = models.CharField(max_length=250)
    job_type = models.CharField(max_length=250)
    salary = models.CharField(max_length=250)
    schedule = models.CharField(max_length=250)
    students = models.ManyToManyField(Student)
