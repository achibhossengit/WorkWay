import json
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import CustomUser, Employer, JobSeeker


def absolute_file_url(request, file_field):
    if not file_field:
        return None
    url = file_field.url
    if request and not str(url).startswith("http"):
        return request.build_absolute_uri(url)
    return url

class CustomCreateUserSerializer(UserCreateSerializer):

    def create(self, validated_data):
        instance = super().create(validated_data)
        if instance.user_type == 'Employer':
            Employer.objects.create(user=instance)
        else:
            JobSeeker.objects.create(user=instance)
        return instance
    
class JobSeekerProfileSerializer(ModelSerializer):
    resume = serializers.SerializerMethodField()

    class Meta:
        model = JobSeeker
        exclude = ['user']
        extra_kwargs = {
            'gender': {'required': False},
        }

    def get_resume(self, obj):
        return absolute_file_url(self.context.get("request"), obj.resume)

    def to_internal_value(self, data):
        if hasattr(data, "copy"):
            data = data.copy()
        resume = data.pop("resume", serializers.empty) if isinstance(data, dict) else serializers.empty
        validated = super().to_internal_value(data)
        if resume is not serializers.empty and resume not in (None, "", "null"):
            validated["resume"] = resume
        return validated

    def update(self, instance, validated_data):
        resume = validated_data.pop("resume", serializers.empty)
        instance = super().update(instance, validated_data)
        if resume is not serializers.empty and resume not in (None, "", "null"):
            if instance.resume:
                instance.resume.delete(save=False)
            instance.resume = resume
            instance.save(update_fields=["resume"])
        return instance


class EmployerProfileSerializer(ModelSerializer):
    class Meta:
        model = Employer
        exclude = ['user']
        extra_kwargs = {
            'company': {'required': False},
            'location': {'required': False},
        }

class CustomUserSerializer(ModelSerializer):
    jobseeker = JobSeekerProfileSerializer(required=False, allow_null=True)
    employer = EmployerProfileSerializer(required=False, allow_null=True)
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name','user_type','profile_picture', 'contact_number','jobseeker', 'employer']
        read_only_fields = ['user_type']

    def to_internal_value(self, data):
        payload = {key: data.get(key) for key in data.keys()}
        self._clear_resume = str(data.get("clear_resume", "")).lower() in (
            "1",
            "true",
            "yes",
        )

        for key in ("jobseeker", "employer"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                payload[key] = json.loads(value)

        resume = data.get("resume")
        jobseeker_data = payload.get("jobseeker")
        if resume and not self._clear_resume:
            if isinstance(jobseeker_data, dict):
                jobseeker_data = {**jobseeker_data, "resume": resume}
            else:
                jobseeker_data = {"resume": resume}
            payload["jobseeker"] = jobseeker_data

        profile_picture = payload.pop("profile_picture", None)
        validated = super().to_internal_value(payload)
        if profile_picture:
            validated["profile_picture"] = profile_picture
        return validated

    def get_profile_picture(self, obj):
        return absolute_file_url(self.context.get("request"), obj.profile_picture)

    def update(self, instance, validated_data):
        jobseeker_data = validated_data.pop("jobseeker", None)
        employer_data = validated_data.pop("employer", None)
        clear_resume = getattr(self, "_clear_resume", False)

        if instance.user_type == "Employer" and employer_data:
            EmployerProfileSerializer().update(instance.employer, employer_data)
        elif instance.user_type == "Jobseeker":
            if jobseeker_data:
                JobSeekerProfileSerializer().update(instance.jobseeker, jobseeker_data)
            if clear_resume:
                jobseeker = instance.jobseeker
                if jobseeker.resume:
                    jobseeker.resume.delete(save=False)
                jobseeker.resume = None
                jobseeker.save(update_fields=["resume"])

        return super().update(instance, validated_data)
