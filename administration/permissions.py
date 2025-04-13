from rest_framework import permissions

class IsProductionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user and 
                request.user.is_authenticated and 
                request.user.role and 
                request.user.role.name == 'production_manager')

class IsSameUserOrManager(permissions.BasePermission):
    """Allows users to edit their own profile or managers to edit any."""
    
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser or
            request.user.role.name in ['production_manager', 'quality_control_manager'] or
            obj == request.user
        )