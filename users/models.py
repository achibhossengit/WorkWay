from django.db import models
from django.contrib.auth.models import AbstractUser
from users.validators import validate_file_type
from django.core.validators import MinValueValidator

# Create your models here.
class CustomUser(AbstractUser):
    EMPLOYER = 'Employer'
    JOBSEEKER = 'Jobseeker'
    USER_TYPE_CHOICES = (
        (EMPLOYER, 'Employer'),
        (JOBSEEKER, 'JobSeeker'),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=JOBSEEKER)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'user_type']  # These fields are mandatory

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='employer')
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

class JobSeeker(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    ]
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='jobseeker')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=OTHERS)
    resume = models.FileField(upload_to='resumes/', validators=[validate_file_type], blank=True, null=True)