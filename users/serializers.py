from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import CustomUser, Employer, JobSeeker
from djoser.serializers import UserCreateSerializer

class CustomCreateUserSerializer(UserCreateSerializer):
    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.user_type == 'Employer':
            Employer.objects.create(user=instance)
        else:
            JobSeeker.objects.create(user=instance)
        return instance
        

class EmployerSerializer(ModelSerializer):
    class Meta:
        model = Employer
        fields = ['company', 'location']

class JobseekerSerializer(ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['gender', 'resume']


class CustomUserSerializer(ModelSerializer):
    employer = EmployerSerializer() 
    jobseeker = JobseekerSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_type', 'first_name', 'last_name', 'email', 'contact_number', 'profile_picture', 'employer', 'jobseeker']
        read_only_fields = ['user_type']

    def update(self, instance, validated_data):
        employer_data = validated_data.pop('employer', None)
        jobseeker_data = validated_data.pop('jobseeker', None)

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()

        if employer_data:
            Employer.objects.update_or_create(user=instance, defaults=employer_data)
        if jobseeker_data:
            JobSeeker.objects.update_or_create(user=instance, defaults=jobseeker_data)

        return instance

