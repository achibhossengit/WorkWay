from django.db import models
from jobs.models import Job
from users.models import JobSeeker, Employer
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Application(models.Model):
    PEDING = 'P'
    REVIEWED = 'R'
    ACCEPT = 'A'
    STATUS_CHOICES = [
        (PEDING, 'Pending'),
        (REVIEWED, 'Reviewed'),
        (ACCEPT, 'ACCEPT'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PEDING)
    applied_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='reviews')
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='reviews')
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)