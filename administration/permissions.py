from rest_framework import permissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


def _is_admin(user):
    if not (user and user.is_authenticated):
        return False
    if user.is_superuser:
        return True
    return bool(user.role and user.role.name == 'admin')


class IsAdminRole(permissions.BasePermission):
    """Allows access only to superusers or users with the ``admin`` role."""

    def has_permission(self, request, view):
        return _is_admin(getattr(request, 'user', None))


class RoleWritePermission(permissions.BasePermission):
    """
    Any authenticated user may read (safe methods). Writes require the
    user's role to be listed in ``required_roles`` (either a view attribute
    or the class default). Superusers and the ``admin`` role always pass.
    """

    required_roles = ()

    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        if _is_admin(user):
            return True
        role = user.role.name if user.role else None
        required = getattr(view, 'required_roles', None) or self.required_roles
        return role in required


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
            (request.user.role and request.user.role.name in [
                'production_manager', 'quality_control_manager']) or
            obj == request.user
        )
