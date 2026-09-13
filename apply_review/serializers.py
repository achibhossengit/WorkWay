from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apply_review.models import Application, Review

class ApplicationSerializer(ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['jobseeker', 'job_title', 'applied_at']

    def validate(self, attrs):
        if self.instance:
            return attrs
        job = attrs.get("job")
        jobseeker = self.context.get("job_seeker")
        if job and jobseeker:
            existing = Application.objects.filter(job=job, jobseeker=jobseeker).first()
            if existing and existing.status != Application.CANCELLED:
                raise serializers.ValidationError("You have already applied for this job.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('status', None)
        jobseeker = self.context.get('job_seeker')
        validated_data['jobseeker'] = jobseeker
        existing = Application.objects.filter(
            job=validated_data.get('job'),
            jobseeker=jobseeker,
        ).first()
        if existing:
            existing.status = Application.PEDING
            existing.applied_at = timezone.now()
            existing.save(update_fields=['status', 'applied_at'])
            return existing
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('status') != Application.CANCELLED:
            raise serializers.ValidationError(
                {'status': 'You can only cancel your application.'}
            )
        instance.status = Application.CANCELLED
        instance.save(update_fields=['status'])
        return instance

class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['jobseeker']

    def create(self, validated_data):
        validated_data['jobseeker'] = self.context['jobseeker']
        return super().create(validated_data)


class ApplicationSerializerForEmployer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['job', 'jobseeker']