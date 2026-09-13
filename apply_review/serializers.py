from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apply_review.models import Application, Review

class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['status', 'jobseeker']

    def validate(self, attrs):
        job = attrs.get("job")
        jobseeker = self.context.get("job_seeker")
        if job and jobseeker and Application.objects.filter(job=job, jobseeker=jobseeker).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        return attrs

    def create(self, validated_data):
        validated_data['jobseeker'] = self.context.get('job_seeker')
        return super().create(validated_data)

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