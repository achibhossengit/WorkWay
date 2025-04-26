from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apply_review.models import Application, Review
from users.models import JobSeeker
from apply_review.serializers import ApplicationSerializer, ReviewSerializer, ApplicationSerializerForEmployer
from api.permissions import IsEmployerOwnerOrAdminReadonly, IsJobseekerOwnerOrAdminReadonly
class ApplicationViewSetForJobseeker(ModelViewSet):
    permission_classes = [IsAuthenticated, IsJobseekerOwnerOrAdminReadonly]
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        return Application.objects.filter(jobseeker = self.kwargs.get('jobseeker_pk'))
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_staff:
            context['job_seeker'] = self.kwargs.get('jobseeker_pk')
        else:
            context['job_seeker'] = self.request.user.jobseeker
        return context
    
class ApplicationViewSetForEmployer(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdminReadonly]
    serializer_class = ApplicationSerializerForEmployer

    def get_queryset(self):
        return Application.objects.filter(job = self.kwargs.get('job_pk'))


class ReviewViewSetForJobseeker(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsJobseekerOwnerOrAdminReadonly]
    def get_queryset(self):
        return Review.objects.filter(jobseeker = self.kwargs.get('jobseeker_pk'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['jobseeker'] = JobSeeker.objects.get(pk=self.kwargs.get('jobseeker_pk'))
        return context


class ReviewViewSetForEmployer(ModelViewSet):
    http_method_names = ['get', 'head', 'options']
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdminReadonly]

    def get_queryset(self):
        return Review.objects.filter(employer = self.kwargs.get('employer_pk'))
