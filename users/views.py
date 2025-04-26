from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from api.permissions import IsJobseekerOrAdminReadonly, IsEmployerOrAdminReadonly

class JobseekerViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated, IsJobseekerOrAdminReadonly]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.filter(user_type = 'Jobseeker')
        return CustomUser.objects.filter(user_type = 'Jobseeker', id = self.request.user.id)
    

class EmployerViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdminReadonly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.filter(user_type = 'Employer')
        return CustomUser.objects.filter(user_type = 'Employer', id = self.request.user.id)
        