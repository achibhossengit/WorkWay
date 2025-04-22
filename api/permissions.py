from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsEmployerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True
            
        # Check for authenticated Employer user
        if request.user.is_staff:
            return (view.action == 'destroy')

        return (
            request.user.is_authenticated
            and hasattr(request.user, 'user_type')
            and request.user.user_type == 'Employer'
        )
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
            
        # Staff can delete any object
        if request.user.is_staff and view.action == 'destroy':
            return True
            
        # Employers can only modify their own objects
        if hasattr(obj, 'employer'):
            return (
                request.user.is_authenticated
                and hasattr(request.user, 'user_type')
                and request.user.user_type == 'Employer'
                and obj.employer.user == request.user
            )
            
        return False


class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
            
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )
    