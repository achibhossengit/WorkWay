from django.contrib import admin
from .models import CustomUser, Employer, JobSeeker

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Employer)
admin.site.register(JobSeeker)