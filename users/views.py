from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.models import CustomUser
from users.serializers import CustomUserSerializer
from api.permissions import IsJobseekerOrAdminDeleteOnly, IsEmployerOrAdminDeleteOnly

class JobseekerViewSet(ModelViewSet):
    """
    A viewset for managing jobseeker accounts.

    - GET: Retrieve jobseeker accounts.
        - Admin users can view all jobseekers.
        - Jobseekers can view their own account.
    - PUT/PATCH: Update a jobseeker account.
        - Jobseekers can update their own account.
    - DELETE: Delete a jobseeker account.
        - Admin users can delete any jobseeker account.
        - Jobseekers can delete their own account.
    """
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']
    permission_classes = [IsAuthenticated, IsJobseekerOrAdminDeleteOnly]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.filter(user_type='Jobseeker')
        return CustomUser.objects.filter(user_type='Jobseeker', id=self.request.user.id)


class EmployerViewSet(ModelViewSet):
    """
    A viewset for managing employer accounts.

    - GET: Retrieve employer accounts.
        - Admin users can view all employers.
        - Employers can view their own account.
    - PUT/PATCH: Update an employer account.
        - Employers can update their own account.
    - DELETE: Delete an employer account.
        - Admin users can delete any employer account.
        - Employers can delete their own account.
    """
    http_method_names = ['get', 'put', 'patch', 'delete', 'head', 'options']
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrAdminDeleteOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.filter(user_type='Employer')
        return CustomUser.objects.filter(user_type='Employer', id=self.request.user.id)
