from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Mixzer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    is_student = models.BooleanField(default=False)
    college = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=18, blank=True)

    def verify_student(self):
        return self.user.email.endswith('.edu')