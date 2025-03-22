from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import Group, Permission
from .models import CustomUser
from .serializers import CustomUserSerializer, GroupSerializer, PermissionSerializer
import subprocess
from django.conf import settings
import os
import sys
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Backup
from .serializers import BackupSerializer   

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissions]

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
    # permission_classes = [IsAuthenticated]

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
    # permission_classes = [IsAuthenticated]

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
"loigic of backups"
def create_backup():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'FPMS.settings'
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path = os.path.join(settings.BACKUP_ROOT, backup_name)

    # Run the dumpdata command
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'dumpdata', '--indent', '2'],
            capture_output=True,
            text=True,
            env=os.environ  # Pass current environment variables
        )

        if result.stdout.strip():
            with open(backup_path, 'w') as f:
                f.write(result.stdout)
            return backup_path, True
        else:
            return "Dumpdata returned empty output.", False

    except Exception as e:
        return str(e), False

class CreateBackupView(APIView):
    def post(self, request):
        backup_path, success = create_backup()
        if success:
            backup = Backup.objects.create(
                name=f"Backup_{Backup.objects.count() + 1}",
                file_path=backup_path,
                status="Completed"
            )
            serializer = BackupSerializer(backup)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": backup_path}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"response "
class ListBackupsView(APIView):
    def get(self, request):
        backups = Backup.objects.all()
        serializer = BackupSerializer(backups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

"restore backup logik"
def restore_backup(backup_path):
    try:
        subprocess.call(
            ['python', 'manage.py', 'loaddata', backup_path]
        )
        return True
    except Exception as e:
        return str(e)

class RestoreBackupView(APIView):
    def post(self, request):
        backup_id = request.data.get('backup_id')
        try:
            backup = Backup.objects.get(id=backup_id)
            success = restore_backup(backup.file_path)
            if success:
                return Response({"message": "Data restored successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to restore data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Backup.DoesNotExist:
            return Response({"error": "Backup not found"}, status=status.HTTP_404_NOT_FOUND)
