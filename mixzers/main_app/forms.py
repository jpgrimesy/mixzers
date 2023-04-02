from django.forms import ModelForm
from .models import Mixzer
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = Mixzer
        fields = ['location', 'phone_number']

class AddExtraUserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']