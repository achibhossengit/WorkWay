from django.db import models
from jobs.models import Job
from users.models import Employer


class Payment(models.Model):
    FEATURED = 'featured'
    PURPOSE_CHOICES = [
        (FEATURED, 'Featured Job Listing'),
    ]

    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (CANCELLED, 'Cancelled'),
    ]

    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE, related_name='payments'
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='payments'
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default=FEATURED)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default='BDT')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=PENDING)
    tran_id = models.CharField(max_length=40, unique=True)
    val_id = models.CharField(max_length=80, blank=True, default='')
    session_key = models.CharField(max_length=120, blank=True, default='')
    gateway_url = models.URLField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tran_id} ({self.status})"
