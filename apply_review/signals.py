from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from apply_review.models import Application

@receiver(post_save, sender=Application)
def send_application_email(sender, instance, created, **kwargs):
    if created:
        jobseeker_email = instance.jobseeker.user.email
        employer_email = instance.job.employer.user.email

        # email body
        jobseeker_sub = "Successfully Applied for a new job!"
        jobseeker_message = f"Dear {instance.jobseeker.user.username}, \n\nYour application for the job '{instance.job.title}' has been successfully submitted."

        employer_sub = "New Applications Received"
        employer_message = f"Hello {instance.job.employer.user.username}, \n\nYou have received a new applications for your job posting '{instance.job.title}'. "

        send_mail(
            subject=jobseeker_sub,
            message=jobseeker_message,
            from_email='mail.achibhossen@gmail.com',
            recipient_list= [jobseeker_email]
        )
        send_mail(
            subject=employer_sub,
            message=employer_message,
            from_email='mail.achibhossen@gmail.com',
            recipient_list= [employer_email]
        )