from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

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

    REQUIRED_FIELDS = ['email', 'user_type']  # These fields are mandatory for user creations

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='employer')
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

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
    resume = models.FileField(upload_to='resumes/', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'pdf'])], blank=True, null=True)

    def __str__(self):
        return self.user.username