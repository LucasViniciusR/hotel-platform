from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return bool(user and user.is_authenticated and (user.is_staff or getattr(user, 'role', None) == 'admin'))

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, 'role', None) == 'admin'

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, 'role', None) == 'staff'
    
class IsClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and getattr(user, 'role', None) == 'client'
