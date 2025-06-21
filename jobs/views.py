from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from jobs.models import Job, Category
from jobs.serializers import JobSerializer, CategorySerializer, NestedJobSerializer
from api.permissions import IsEmployerOrReadOnly, IsAdminOrReadOnly

# Create your views here.
class CategoryViewSet(ModelViewSet):
    """
    A viewset for managing job categories.

    - GET: Retrieve all categories or a specific category.
    - POST: Create a new category (Admin only).
    - PUT/PATCH: Update an existing category (Admin only).
    - DELETE: Delete a category (Admin only).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class JobViewSet(ModelViewSet):
    """
    A viewset for managing jobs.

    - GET: Retrieve all jobs or filter jobs by category.
    - POST: Create a new job (Employers only).
    - PUT/PATCH: Update an existing job (Employers only).
    - DELETE: Delete a job (Employers only).
    - Filters: Supports filtering jobs by category.
    """
    queryset = Job.objects.select_related('employer__user', 'category', 'details', 'requirements').all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    def get_serializer_context(self):
        """
        Add additional context to the serializer.

        - If the user is staff, provide the default context.
        - If the user is authenticated and an Employer, add the employer instance to the context.
        """
        context = super().get_serializer_context()
        if self.request.user.is_staff:
            return context
        if self.request.user.is_authenticated and self.request.user.user_type == 'Employer':
            context['employer'] = self.request.user.employer
        return context


class EmployerJobViewSet(ModelViewSet):
    """
    A viewset for managing jobs posted by a specific employer.

    - GET: Retrieve all jobs created by the specified employer.
    """
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]

    def get_queryset(self):
        """
        Return jobs filtered by the employer's ID passed in the URL.
        """
        return Job.objects.filter(employer=self.kwargs.get('employer_pk'))


class CategoryJobViewSet(ModelViewSet):
    """
    A viewset for managing jobs under a specific category.

    - GET: Retrieve all jobs associated with a specific category.
    - POST: Can create a job for specific category (Employer only)
    - PUT: Can Update a job Of specific category (Only owner)
    """
    serializer_class = NestedJobSerializer
    permission_classes = [IsEmployerOrReadOnly]

    def get_queryset(self):
        """
        Return jobs filtered by the category ID passed in the URL.
        """
        return Job.objects.filter(category=self.kwargs.get('category_pk'))

    def get_serializer_context(self):
        """
        Add additional context to the serializer.

        - If the user is staff, provide the default context.
        - If the user is authenticated and an Employer, add the employer and category instances to the context.
        """
        context = super().get_serializer_context()
        if self.request.user.is_staff:
            return context
        if self.request.user.is_authenticated and self.request.user.user_type == 'Employer':
            context['employer'] = self.request.user.employer
            context['category'] = Category.objects.get(pk=self.kwargs.get('category_pk'))
        return context
