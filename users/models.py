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
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=JOBSEEKER)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

class Employer(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='employer')
    contact_number = models.CharField(max_length=15, blank=True, null=True)

class JobSeeker(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHERS = 'Others'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    ]
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE, related_name='job_seeker')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=OTHERS)
    resume = models.FileField(upload_to='resumes/', validators=[validate_file_type], blank=True, null=True)

class Company(models.Model):
    SOFTWARE = 'Software'
    MANUFACTURING = 'Manufacturing'
    ECOMMERCE = 'E-commerce'
    TYPE_CHOICES = [
        (SOFTWARE, 'Software'),
        (MANUFACTURING, 'Manufacturing'),
        (ECOMMERCE, 'E-commerce'),
    ]
    employer = models.OneToOneField(Employer, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=SOFTWARE)
    total_emp = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(max_length=400)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

class Address(models.Model):
    BD = 'Bangladesh'
    PAK = 'Pakistan'
    NEP = 'Nepal'
    COUNTRY_CHOICES = [
        (BD, 'Bangladesh'),
        (PAK, 'Pakistan'),
        (NEP, 'Nepal'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=15, choices=COUNTRY_CHOICES, default=BD)
    district = models.CharField(max_length=15, default='Dhaka')
    postal_code = models.CharField(max_length=10, blank=True, null=True)
