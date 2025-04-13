# administration/views.py
import psutil
import time
from datetime import timedelta
from django.db.models import Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.http import FileResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout
import os
from .permissions import IsProductionManager, IsSameUserOrManager
from datetime import datetime
import subprocess
from .models import BackupConfig, BackupRecord, Department, SystemSetting, HealthMetric, Role
from django.contrib.auth.models import User
from .serializers import BackupConfigSerializer, BackupRecordSerializer, DepartmentSerializer, SystemSettingSerializer, HealthMetricSerializer, RoleSerializer, UserSerializer

class BackupConfigViewSet(viewsets.ModelViewSet):
    queryset = BackupConfig.objects.all()
    serializer_class = BackupConfigSerializer
    permission_classes = [permissions.AllowAny]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAdminUser]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]

class BackupRecordViewSet(viewsets.ModelViewSet):
    queryset = BackupRecord.objects.all()
    serializer_class = BackupRecordSerializer
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def create_backup(self, request):
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fpms_backup_{timestamp}.sql"
        backup_path = os.path.join(settings.MEDIA_ROOT, 'backups', filename)
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Run mysqldump command
        db_settings = settings.DATABASES['default']
        command =  f"""
            "mysqldump" 
            --user={db_settings['USER']}
            --password={db_settings['PASSWORD']}
            --host={db_settings['HOST']}
            {db_settings['NAME']}
            --result-file="{backup_path}"
             subprocess.run(command, shell=True, check=True)
            """
           

        try:
            subprocess.run(command, check=True)
            
            # Get file size
            file_size = os.path.getsize(backup_path)
            
            # Create backup record
            backup = BackupRecord.objects.create(
                backup_file=f'backups/{filename}',
                created_by=request.user,
                file_size=file_size,
                is_automated=False
            )
            
            return Response({
                'status': 'success',
                'backup_id': backup.id
            })
        except subprocess.CalledProcessError as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        backup = self.get_object()
        file_path = backup.backup_file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        if not request.user.is_superuser:
            return Response({'status': 'error', 'message': 'Only superusers can restore backups'}, status=403)
        
        backup = self.get_object()
        file_path = backup.backup_file.path
        
        db_settings = settings.DATABASES['default']
        command = [
            'mysql',
            '-u', db_settings['USER'],
            '-p' + db_settings['PASSWORD'],
            '-h', db_settings['HOST'],
            db_settings['NAME'],
            '<', file_path
        ]
        
        try:
            subprocess.run(' '.join(command), shell=True, check=True)
            return Response({'status': 'success'})
        except subprocess.CalledProcessError as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)




class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [permissions.IsAdminUser]




class HealthMetricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        # Calculate CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Calculate memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Calculate disk usage
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        disk_space = disk.free / (1024 ** 3)  # Convert to GB
        
        # Calculate response time (simplified)
        start_time = time.time()
        # Make a simple DB query to measure response time
        _ = SystemSetting.objects.first()
        response_time = (time.time() - start_time) * 1000  # Convert to ms
        
        data = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'disk_space': round(disk_space, 2),
            'response_time': round(response_time, 2),
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in database if needed
        if request.query_params.get('store') == 'true':
            HealthMetric.objects.create(**data)
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        time_range = request.query_params.get('range', '1h')
        
        if time_range == '1h':
            delta = timedelta(hours=1)
        elif time_range == '24h':
            delta = timedelta(days=1)
        elif time_range == '7d':
            delta = timedelta(days=7)
        else:
            delta = timedelta(hours=1)
        
        cutoff = datetime.now() - delta
        metrics = HealthMetric.objects.filter(timestamp__gte=cutoff)
        
        if not metrics.exists():
            return Response({'detail': 'No metrics available'}, status=404)
        
        # Calculate averages
        avg_cpu = metrics.aggregate(Avg('cpu_usage'))['cpu_usage__avg']
        avg_memory = metrics.aggregate(Avg('memory_usage'))['memory_usage__avg']
        avg_disk = metrics.aggregate(Avg('disk_usage'))['disk_usage__avg']
        avg_response = metrics.aggregate(Avg('response_time'))['response_time__avg']
        
        return Response({
            'time_range': time_range,
            'avg_cpu_usage': round(avg_cpu, 2),
            'avg_memory_usage': round(avg_memory, 2),
            'avg_disk_usage': round(avg_disk, 2),
            'avg_response_time': round(avg_response, 2),
            'sample_count': metrics.count()
        })
    

from django_filters.rest_framework import DjangoFilterBackend
from .models import ActivityLog
from .serializers import ActivityLogSerializer



class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'action', 'model', 'timestamp']
    
    def get_queryset(self):
        # Non-admin users can only see their own logs
        if not self.request.user.is_staff:
            return self.queryset.filter(user=self.request.user)
        return self.queryset
from .models import User
from .serializers import UserSerializer





class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsSameUserOrManager | permissions.IsAdminUser | IsProductionManager]
        elif self.action == 'logout':
            permission_classes = [permissions.AllowAny]  # No auth required
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Public logout endpoint that safely handles:
        - Token invalidation (if provided)
        - Session cleanup (if exists)
        - Always returns success
        """
        response = Response(
            {"detail": "Logout completed"},
            status=status.HTTP_200_OK
        )
        
        # Safely handle token deletion if exists
        if hasattr(request, 'auth') and request.auth:
            try:
                request.auth.delete()
            except:
                pass  # Silently fail if token is invalid
        
        # Clear session if exists
        if request.user.is_authenticated:
            logout(request)
            response.delete_cookie('sessionid')
            response.delete_cookie('csrftoken')
        
        return response