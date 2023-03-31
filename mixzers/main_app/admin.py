from django.contrib import admin
from .models import Employer, Student, Message, Review, Job_Post
# Register your models here.

admin.site.register(Employer)
admin.site.register(Student)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(Job_Post)
