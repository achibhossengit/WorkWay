from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apply_review.models import Application, Review
from users.models import JobSeeker
from apply_review.serializers import ApplicationSerializer, ReviewSerializer, ApplicationSerializerForEmployer
from api.permissions import IsEmployerOwnerOrAdminReadonly, IsJobseekerOwnerOrAdminReadonly


class ApplicationViewSetForJobseeker(ModelViewSet):
    """
    A viewset for managing applications submitted by a jobseeker.

    - GET: Retrieve applications for a specific jobseeker.
    - PUT/PATCH: Update an application (Only application creator).
    - DELETE: Delete an application (Only applicaton creator).
    """
    permission_classes = [IsAuthenticated, IsJobseekerOwnerOrAdminReadonly]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(jobseeker=self.kwargs.get('jobseeker_pk'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_staff:
            context['job_seeker'] = self.kwargs.get('jobseeker_pk')
        elif self.request.user.is_authenticated:
            context['job_seeker'] = self.request.user.jobseeker
        return context


class ApplicationViewSetForEmployer(ModelViewSet):
    """
    A viewset for managing applications related to jobs posted by an employer.

    - GET: Retrieve applications for a specific job.
    - PUT/PATCH: Update only status of application (Job creator only).
    """
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdminReadonly]
    serializer_class = ApplicationSerializerForEmployer

    def get_queryset(self):
        return Application.objects.filter(job=self.kwargs.get('job_pk'))


class ReviewViewSetForJobseeker(ModelViewSet):
    """
    A viewset for managing reviews send by a jobseeker.

    - GET: Retrieve reviews for a specific jobseeker.
    - PUT/PATCH: Update a review (Creator Only).
    - DELETE: Delete a review (Creator Only).
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsJobseekerOwnerOrAdminReadonly]

    def get_queryset(self):
        return Review.objects.filter(jobseeker=self.kwargs.get('jobseeker_pk'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'jobseeker_pk' in self.kwargs:
            context['jobseeker'] = JobSeeker.objects.get(pk=self.kwargs.get('jobseeker_pk'))
        return context


class ReviewViewSetForEmployer(ModelViewSet):
    """
    A viewset for managing reviews Received by an employer.

    - GET: Retrieve reviews given by jobseekers.
    """
    http_method_names = ['get', 'head', 'options']
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdminReadonly]

    def get_queryset(self):
        return Review.objects.filter(employer=self.kwargs.get('employer_pk'))
