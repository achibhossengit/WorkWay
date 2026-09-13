import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apply_review.models import Application

logger = logging.getLogger(__name__)

STATUS_LABELS = {
    Application.PEDING: "Pending",
    Application.REVIEWED: "Reviewed",
    Application.ACCEPT: "Accepted",
    Application.REJECTED: "Rejected",
    Application.CANCELLED: "Cancelled",
}

EMPLOYER_EDITABLE = {
    Application.PEDING,
    Application.REVIEWED,
    Application.ACCEPT,
    Application.REJECTED,
}


def _from_email():
    return settings.EMAIL_HOST_USER or getattr(
        settings, "DEFAULT_FROM_EMAIL", "noreply@workway.local"
    )


def _safe_send(subject, message, recipient):
    if not recipient:
        logger.warning("Skip email %r — missing recipient", subject)
        return
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=_from_email(),
            recipient_list=[recipient],
            fail_silently=False,
        )
    except Exception:
        logger.exception(
            "Failed to send email %r to %s",
            subject,
            recipient,
        )


def _names(application):
    jobseeker_user = application.jobseeker.user
    employer_user = application.job.employer.user
    company = application.job.employer.company or employer_user.username
    jobseeker_name = (
        f"{jobseeker_user.first_name} {jobseeker_user.last_name}".strip()
        or jobseeker_user.username
    )
    employer_name = (
        f"{employer_user.first_name} {employer_user.last_name}".strip()
        or employer_user.username
    )
    return {
        "job_title": application.job.title,
        "jobseeker_name": jobseeker_name,
        "jobseeker_email": jobseeker_user.email,
        "employer_name": employer_name,
        "employer_email": employer_user.email,
        "company": company,
        "status_label": STATUS_LABELS.get(
            application.status, application.status
        ),
    }


@receiver(pre_save, sender=Application)
def cache_previous_application_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_status = None
        return
    try:
        instance._previous_status = (
            Application.objects.only("status").get(pk=instance.pk).status
        )
    except Application.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=Application)
def send_application_lifecycle_emails(sender, instance, created, raw=False, **kwargs):
    if raw:
        return

    previous = getattr(instance, "_previous_status", None)
    current = instance.status
    info = _names(instance)

    # Jobseeker: first apply → notify employer
    if created:
        _safe_send(
            subject=f"New application for {info['job_title']}",
            message=(
                f"Hello {info['employer_name']},\n\n"
                f"{info['jobseeker_name']} has applied for your job posting "
                f"'{info['job_title']}'.\n\n"
                f"Please review the application in your WorkWay dashboard.\n"
            ),
            recipient=info["employer_email"],
        )
        return

    # Jobseeker: re-apply (Cancelled → Pending) → notify employer
    if (
        previous == Application.CANCELLED
        and current == Application.PEDING
    ):
        _safe_send(
            subject=f"Re-application for {info['job_title']}",
            message=(
                f"Hello {info['employer_name']},\n\n"
                f"{info['jobseeker_name']} has reapplied for your job posting "
                f"'{info['job_title']}'.\n\n"
                f"Please review the application in your WorkWay dashboard.\n"
            ),
            recipient=info["employer_email"],
        )
        return

    # Jobseeker: cancel → notify employer
    if (
        previous != Application.CANCELLED
        and current == Application.CANCELLED
    ):
        _safe_send(
            subject=f"Application cancelled for {info['job_title']}",
            message=(
                f"Hello {info['employer_name']},\n\n"
                f"{info['jobseeker_name']} has cancelled their application for "
                f"'{info['job_title']}'.\n"
            ),
            recipient=info["employer_email"],
        )
        return

    # Employer: status change among P/R/A/X → notify jobseeker
    if (
        previous in EMPLOYER_EDITABLE
        and current in EMPLOYER_EDITABLE
        and previous != current
    ):
        _safe_send(
            subject=f"Application update: {info['job_title']}",
            message=(
                f"Dear {info['jobseeker_name']},\n\n"
                f"Your application for '{info['job_title']}' at "
                f"{info['company']} has been updated.\n\n"
                f"Previous status: {STATUS_LABELS.get(previous, previous)}\n"
                f"New status: {info['status_label']}\n\n"
                f"You can check details in your WorkWay dashboard.\n"
            ),
            recipient=info["jobseeker_email"],
        )
