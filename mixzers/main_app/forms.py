from django.forms import ModelForm
from .models import Mixzer, Message, Review, Job_Post
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = Mixzer
        fields = ['location', 'phone_number']


class AddExtraUserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'content']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'rating', 'content' ]


class JobPostForm(ModelForm):
    class Meta:
        model = Job_Post
        fields = ['title', 'job_description', 'job_type', 'salary', 'schedule']