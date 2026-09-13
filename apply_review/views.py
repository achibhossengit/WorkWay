from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from apply_review.models import Application, Review
from users.models import JobSeeker
from apply_review.serializers import (
    ApplicationSerializer,
    ReviewSerializer,
    ApplicationSerializerForEmployer,
)
from api.permissions import (
    IsEmployerOwnerOrAdminReadonly,
    IsJobseekerOwnerOrAdminReadonly,
)
from jobs.paginations import CustomPageNumberPagination


class ApplicationViewSetForJobseeker(ModelViewSet):
    """
    A viewset for managing applications submitted by a jobseeker.

    - GET: Retrieve applications for a specific jobseeker.
    - PUT/PATCH: Cancel an application (sets status to Cancelled).
    - DELETE: Same as cancel — does not remove the row from the database.
    """
    permission_classes = [IsAuthenticated, IsJobseekerOwnerOrAdminReadonly]
    serializer_class = ApplicationSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "job"]

    def get_queryset(self):
        return (
            Application.objects.filter(jobseeker=self.kwargs.get("jobseeker_pk"))
            .select_related("job", "job__employer", "job__employer__user")
            .order_by("-applied_at")
        )

    def perform_destroy(self, instance):
        instance.status = Application.CANCELLED
        instance.save(update_fields=["status"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_staff:
            context["job_seeker"] = self.kwargs.get("jobseeker_pk")
        elif self.request.user.is_authenticated:
            context["job_seeker"] = self.request.user.jobseeker
        return context


class ApplicationViewSetForEmployer(ModelViewSet):
    """
    A viewset for managing applications related to jobs posted by an employer.

    - GET: Retrieve applications for a specific job.
    - PUT/PATCH: Update only status of application (Job creator only).
    """
    http_method_names = ["get", "put", "patch", "head", "options"]
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdminReadonly]
    serializer_class = ApplicationSerializerForEmployer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        return (
            Application.objects.filter(job=self.kwargs.get("job_pk"))
            .exclude(status=Application.CANCELLED)
            .select_related("jobseeker__user", "job")
            .order_by("-applied_at")
        )


class ApplicationViewSetForEmployerAll(ReadOnlyModelViewSet):
    """
    List all non-cancelled applications across every job for an employer.

    - GET /employers/{id}/applications/
    """
    http_method_names = ["get", "head", "options"]
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdminReadonly]
    serializer_class = ApplicationSerializerForEmployer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        return (
            Application.objects.filter(
                job__employer_id=self.kwargs.get("employer_pk")
            )
            .exclude(status=Application.CANCELLED)
            .select_related("jobseeker__user", "job")
            .order_by("-applied_at")
        )


class ReviewViewSetForJobseeker(ModelViewSet):
    """
    A viewset for managing reviews send by a jobseeker.

    - GET: Retrieve reviews for a specific jobseeker.
    - PUT/PATCH: Update a review (Creator Only).
    - DELETE: Delete a review (Creator Only).
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsJobseekerOwnerOrAdminReadonly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return (
            Review.objects.filter(jobseeker=self.kwargs.get("jobseeker_pk"))
            .select_related("jobseeker__user", "employer__user")
            .order_by("-id")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if "jobseeker_pk" in self.kwargs:
            context["jobseeker"] = JobSeeker.objects.get(
                pk=self.kwargs.get("jobseeker_pk")
            )
        return context


class ReviewViewSetForEmployer(ModelViewSet):
    """
    A viewset for managing reviews Received by an employer.

    - GET: Retrieve reviews given by jobseekers.
    """
    http_method_names = ["get", "head", "options"]
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return (
            Review.objects.filter(employer=self.kwargs.get("employer_pk"))
            .select_related("jobseeker__user", "employer__user")
            .order_by("-id")
        )


class PublicReviewViewSet(ReadOnlyModelViewSet):
    """Public list of jobseeker reviews about employers."""
    permission_classes = [AllowAny]
    serializer_class = ReviewSerializer
    pagination_class = CustomPageNumberPagination
    queryset = Review.objects.select_related(
        "jobseeker__user", "employer__user"
    ).order_by("-id")
