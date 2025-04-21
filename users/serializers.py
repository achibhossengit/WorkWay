from rest_framework.serializers import ModelSerializer
from djoser.serializers import UserCreateSerializer
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
    class Meta:
        model = JobSeeker
        fields = ['gender', 'resume']
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

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email','user_type', 'jobseeker', 'employer']
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