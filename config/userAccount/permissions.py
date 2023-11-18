from rest_framework.permissions import BasePermission

class ISOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return True
            elif request.user == obj:
                return True
        return False




class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj:
                return True
        return False
