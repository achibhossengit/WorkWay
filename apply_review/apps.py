from django.apps import AppConfig


class ApplyReviewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apply_review'

    def ready(self):
        import apply_review.signals