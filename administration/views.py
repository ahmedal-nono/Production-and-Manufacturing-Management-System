from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import Group, Permission
from .models import CustomUser
from .serializers import CustomUserSerializer, GroupSerializer, PermissionSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a user account."""
        user = self.get_object()
        if user.is_active:
            return Response({'status': 'User is already active'}, status=400)
        user.is_active = True
        user.save()
        return Response({'status': 'User activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a user account."""
        user = self.get_object()
        if not user.is_active:
            return Response({'status': 'User is already deactivated'}, status=400)
        user.is_active = False
        user.save()
        return Response({'status': 'User deactivated'})

    # Debugging added here
    def list(self, request, *args, **kwargs):
        user_permissions = request.user.get_all_permissions()
        required_permissions = ['administration.view_customuser']
        print(f"Authenticated User: {request.user}")
        print(f"User Permissions: {request.user.get_all_permissions()}")
        if not any(perm in user_permissions for perm in required_permissions):
            raise PermissionDenied("User does not have the required permissions.")
        return super().list(request, *args, **kwargs)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def assign_user(self, request, pk=None):
        """Assign a user to a group."""
        group = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(pk=user_id)
            group.user_set.add(user)
            return Response({'status': f'User {user.username} added to group {group.name}'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    @action(detail=True, methods=['post'])
    def remove_user(self, request, pk=None):
        """Remove a user from a group."""
        group = self.get_object()
        user_id = request.data.get('user_id')
        try:
            user = CustomUser.objects.get(pk=user_id)
            group.user_set.remove(user)
            return Response({'status': f'User {user.username} removed from group {group.name}'})
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def assign_to_group(self, request, pk=None):
        """Assign a permission to a group."""
        permission = self.get_object()
        group_id = request.data.get('group_id')
        try:
            group = Group.objects.get(pk=group_id)
            group.permissions.add(permission)
            return Response({'status': f'Permission {permission.name} added to group {group.name}'})
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=404)

    @action(detail=True, methods=['post'])
    def remove_from_group(self, request, pk=None):
        """Remove a permission from a group."""
        permission = self.get_object()
        group_id = request.data.get('group_id')
        try:
            group = Group.objects.get(pk=group_id)
            group.permissions.remove(permission)
            return Response({'status': f'Permission {permission.name} removed from group {group.name}'})
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=404)
