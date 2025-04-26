from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.is_staff
    
    
class IsEmployerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # Check for authenticated Employer user
        if request.user.is_staff:
            return (view.action == 'destroy')

        return request.user.is_authenticated and request.user.user_type == 'Employer'
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Staff can delete any object
        if request.user.is_staff and view.action == 'destroy':
            return True
        # Employers can only modify their own objects
        if hasattr(obj, 'employer'):
            return (
                obj.employer.user == request.user
            )
            
        return False
    
class IsJobseekerOrAdminReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        if request.user.user_type == 'Jobseeker':
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        print('it is from has object permissions')
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        
        return request.user.id == int(view.kwargs.get('pk'))
    
class IsEmployerOrAdminReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        if request.user.user_type == 'Employer':
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        
        return request.user.id == int(view.kwargs.get('pk'))


class IsEmployerOwnerOrAdminReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 'Employer' and request.user.id == int(view.kwargs.get('employer_pk')):
            return True
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        # obj of Application class
        if request.user.user_type == 'Employer':
            return request.user.id == obj.job.employer.user.id
                
        return False
    
class IsJobseekerOwnerOrAdminReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_type == 'Jobseeker' and request.user.id == int(view.kwargs.get('jobseeker_pk')):
            return True
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return view.action in ['list', 'retrieve']
        # obj of Application class
        if request.user.user_type == 'Jobseeker':
            return request.user.id == obj.jobseeker.user.id
                
        return False
    
