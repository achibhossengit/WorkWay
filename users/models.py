from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MaxValueValidator
from cloudinary.models import CloudinaryField

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
    profile_picture = CloudinaryField('profile_pictures', blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'user_type']  # These fields are mandatory for user creations

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='employer')
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    website = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

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
    resume = CloudinaryField('resumes', validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'pdf'])], blank=True, null=True)
    about = models.TextField(max_length=250, blank=True, null=True)
    skills = models.JSONField(default=list)
    experiences = models.PositiveIntegerField(validators=[MaxValueValidator(100)], default=0)
    current_address = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.user.username