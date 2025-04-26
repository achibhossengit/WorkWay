from rest_framework.permissions import BasePermission

# class IsReviewOwnerOrReadonly(BasePermission):
#     def has_permission(self, request, view):
#         if request.user.is_staff:
#             return True
#         if 