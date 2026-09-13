import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from apply_review.models import Application

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Application)
def send_application_email(sender, instance, created, raw=False, **kwargs):
    # Only on first create — re-apply updates the same row (created=False).
    if raw or not created:
        return

    from_email = settings.EMAIL_HOST_USER or getattr(
        settings, "DEFAULT_FROM_EMAIL", None
    )
    jobseeker_email = instance.jobseeker.user.email
    employer_email = instance.job.employer.user.email

    jobseeker_subject = "Successfully Applied for a new job!"
    jobseeker_message = (
        f"Dear {instance.jobseeker.user.username},\n\n"
        f"Your application for the job '{instance.job.title}' "
        f"has been successfully submitted."
    )

    employer_subject = "New Applications Received"
    employer_message = (
        f"Hello {instance.job.employer.user.username},\n\n"
        f"You have received a new application for your job posting "
        f"'{instance.job.title}'."
    )

    try:
        send_mail(
            subject=jobseeker_subject,
            message=jobseeker_message,
            from_email=from_email,
            recipient_list=[jobseeker_email],
            fail_silently=False,
        )
        send_mail(
            subject=employer_subject,
            message=employer_message,
            from_email=from_email,
            recipient_list=[employer_email],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Failed to send application emails for application id=%s",
            instance.pk,
        )
