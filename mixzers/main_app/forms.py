from django.forms import ModelForm
from .models import Mixzer

class UserForm(ModelForm):
    class Meta:
        model = Mixzer
        fields = ['location', 'phone_number']