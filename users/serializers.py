from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import CustomUser, Employer, JobSeeker

class CustomCreateUserSerializer(UserCreateSerializer):

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.user_type == 'Employer':
            Employer.objects.create(user=instance)
        else:
            JobSeeker.objects.create(user=instance)
        return instance
    
class JobSeekerProfileSerializer(ModelSerializer):
    resume = serializers.ImageField(required=False)
    class Meta:
        model = JobSeeker
        fields = ['gender', 'resume', 'about', 'skills', 'experiences']
        extra_kwargs = {
            'gender': {'required': False},
            'resume': {'required': False},
        }

class EmployerProfileSerializer(ModelSerializer):
    class Meta:
        model = Employer
        fields = ['company', 'location']
        extra_kwargs = {
            'company': {'required': False},
            'location': {'required': False},
        }

class CustomUserSerializer(ModelSerializer):
    jobseeker = JobSeekerProfileSerializer()
    employer = EmployerProfileSerializer()
    profile_picture = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name','user_type','profile_picture', 'jobseeker', 'employer']
        read_only_fields = ['user_type']

    def update(self, instance, validated_data):
        jobseeker = validated_data.pop('jobseeker')
        employer = validated_data.pop('employer')
        if instance.user_type == 'Employer':
            serializer = EmployerProfileSerializer()
            update_instance = serializer.update(instance.employer, employer)
        elif instance.user_type == 'Jobseeker':
            serializer = JobSeekerProfileSerializer()
            update_instance = serializer.update(instance.jobseeker, jobseeker)
        return super().update(instance, validated_data)