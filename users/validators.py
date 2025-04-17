from django.core.exceptions import ValidationError

def validate_file_type(value):
    allowed_file_types = ['image/jpeg', 'image/png', 'application/pdf']
    if value.file.content_type not in allowed_file_types:
        raise ValidationError('Only JPEG, PNG, or PDF files are allowed.')
