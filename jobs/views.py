from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from jobs.models import Job, Category, Detail
from jobs.serializers import JobSerializer, CategorySerializer, DetailSerializer, NestedJobSerializer
from api.permissions import IsEmployerOrReadOnly, IsAdminOrReadOnly

# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_staff:
            return context
        if self.request.user.is_authenticated and self.request.user.user_type=='Employer':
            context['employer'] = self.request.user.employer
        return context
    

class NestedJobViewSet(ModelViewSet):
    serializer_class = NestedJobSerializer
    permission_classes = [IsEmployerOrReadOnly]

    def get_queryset(self):
        return Job.objects.filter(category = self.kwargs.get('category_pk'))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_staff:
            return context
        if self.request.user.is_authenticated and self.request.user.user_type == 'Employer':
            context['employer'] = self.request.user.employer
            context['category'] = Category.objects.get(pk=self.kwargs.get('category_pk'))
        return context