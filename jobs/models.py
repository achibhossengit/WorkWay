from django.db import models
from users.models import Employer
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Job(models.Model):
    title = models.CharField(max_length=100)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Detail(models.Model):
    HOME = 'H'
    OFFICE = 'O'
    HYBRID = 'Hy'
    WORKPLACE_CHOICES = [
        (HOME, 'Home'),
        (OFFICE, 'Office'),
        (HYBRID, 'Hybrid'),
    ]

    FULL = 'F'
    HALF = 'H'
    INTERN = 'I'
    STATUS_CHOICES = [
        (FULL, 'Full Time'),
        (HALF, 'Half Time'),
        (INTERN, 'Intern'),
    ]

    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='details')
    description = models.TextField(blank=True, null=True)
    workplace = models.CharField(choices=WORKPLACE_CHOICES, max_length=10, default=OFFICE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default=FULL)
    locations = models.CharField(max_length=250, blank=True, null=True)
    min_salary = models.PositiveIntegerField(validators=[MinValueValidator(1000)], blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Details of {self.job.title}"


class Requirement(models.Model):
    JSC = 'J.S.C'
    SSC = 'S.S.C'
    HSC = 'H.S.C'
    MASTER = 'Master'
    EDUCATION_CHOICES = [
        (JSC, 'J.S.C'),
        (SSC, 'S.S.C'),
        (HSC, 'H.S.C'),
        (MASTER, 'Master'),
    ]

    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='requirements')
    education = models.CharField(choices=EDUCATION_CHOICES, default=JSC, max_length=10,)
    experience = models.PositiveIntegerField(validators=[MaxValueValidator(30)], blank=True, null=True)
    skill = models.CharField(blank=True, null=True, max_length=200)