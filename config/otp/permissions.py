from rest_framework.permissions import BasePermission

class IsOwnerOfOTPCode(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj.user:
                return True
        return False