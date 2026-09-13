from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apply_review.models import Application, Review
from users.models import JobSeeker
from users.serializers import absolute_file_url

class ApplicationSerializer(ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    employer_id = serializers.IntegerField(source="job.employer_id", read_only=True)
    employer_company = serializers.CharField(
        source="job.employer.company", read_only=True
    )
    employer_username = serializers.CharField(
        source="job.employer.user.username", read_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'job_title',
            'jobseeker',
            'status',
            'applied_at',
            'employer_id',
            'employer_company',
            'employer_username',
        ]
        read_only_fields = [
            'jobseeker',
            'job_title',
            'applied_at',
            'employer_id',
            'employer_company',
            'employer_username',
        ]

    def validate(self, attrs):
        if self.instance:
            return attrs
        job = attrs.get("job")
        jobseeker = self.context.get("job_seeker")
        if jobseeker is not None and not isinstance(jobseeker, JobSeeker):
            jobseeker = JobSeeker.objects.filter(pk=jobseeker).first()
        elif isinstance(jobseeker, JobSeeker):
            jobseeker.refresh_from_db()
        if jobseeker and not jobseeker.resume:
            raise serializers.ValidationError(
                "Upload a resume before applying for a job."
            )
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
    jobseeker_name = serializers.SerializerMethodField()
    jobseeker_username = serializers.CharField(source='jobseeker.user.username', read_only=True)
    employer_company = serializers.CharField(source='employer.company', read_only=True)
    employer_username = serializers.CharField(source='employer.user.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id',
            'employer',
            'jobseeker',
            'ratings',
            'comment',
            'jobseeker_name',
            'jobseeker_username',
            'employer_company',
            'employer_username',
        ]
        read_only_fields = [
            'jobseeker',
            'jobseeker_name',
            'jobseeker_username',
            'employer_company',
            'employer_username',
        ]

    def get_jobseeker_name(self, obj):
        user = obj.jobseeker.user
        name = f"{user.first_name} {user.last_name}".strip()
        return name or user.username

    def validate(self, attrs):
        if self.instance:
            return attrs
        jobseeker = self.context.get('jobseeker')
        employer = attrs.get('employer')
        if (
            jobseeker
            and employer
            and Review.objects.filter(jobseeker=jobseeker, employer=employer).exists()
        ):
            raise serializers.ValidationError("You have already reviewed this employer.")
        if jobseeker and employer:
            finished = Application.objects.filter(
                jobseeker=jobseeker,
                job__employer=employer,
                status__in=[Application.ACCEPT, Application.REJECTED],
            ).exists()
            if not finished:
                raise serializers.ValidationError(
                    "You can only review an employer after an application is accepted or rejected."
                )
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop('employer', None)
        return super().update(instance, validated_data)


    def create(self, validated_data):
        validated_data['jobseeker'] = self.context['jobseeker']
        return super().create(validated_data)


class ApplicantSerializer(ModelSerializer):
    id = serializers.IntegerField(source='user_id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    contact_number = serializers.CharField(source='user.contact_number', read_only=True)
    profile_picture = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()

    class Meta:
        model = JobSeeker
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'contact_number',
            'profile_picture',
            'resume',
            'about',
            'skills',
            'experiences',
            'current_address',
            'gender',
        ]

    def get_resume(self, obj):
        return absolute_file_url(self.context.get('request'), obj.resume)

    def get_profile_picture(self, obj):
        return absolute_file_url(self.context.get('request'), obj.user.profile_picture)


class ApplicationSerializerForEmployer(ModelSerializer):
    applicant = ApplicantSerializer(source='jobseeker', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'job_title',
            'jobseeker',
            'applicant',
            'status',
            'applied_at',
        ]
        read_only_fields = ['job', 'jobseeker', 'applicant', 'job_title', 'applied_at']

    def validate_status(self, value):
        allowed = {
            Application.PEDING,
            Application.REVIEWED,
            Application.ACCEPT,
            Application.REJECTED,
        }
        if value not in allowed:
            raise serializers.ValidationError(
                'Status must be Pending, Reviewed, Accept, or Rejected.'
            )
        return value