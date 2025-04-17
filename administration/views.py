# administration/views.py
import psutil
import time
from .utils import log_activity
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
from django.contrib.auth import logout, authenticate
import os
import os
import subprocess
from pathlib import Path
from .permissions import IsProductionManager, IsSameUserOrManager
from datetime import datetime
import subprocess
from .models import BackupConfig, BackupRecord, Department, SystemSetting, HealthMetric, Role
from django.contrib.auth.models import User
from .serializers import BackupConfigSerializer, BackupRecordSerializer, DepartmentSerializer, SystemSettingSerializer, HealthMetricSerializer, RoleSerializer, UserSerializer, LoginSerializer

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
MARIADB_BIN_PATH = r"C:\Program Files\MariaDB 11.6\bin"
MYSQLDUMP_PATH = os.path.join(MARIADB_BIN_PATH, "mysqldump.exe")
class BackupRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BackupRecordSerializer
    queryset = BackupRecord.objects.all()
    permission_classes = []
    @action(detail=False, methods=['post'])
    def create_backup(self, request):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"fpms_backup_{timestamp}.sql"
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
        backup_path = os.path.join(backup_dir, filename)
        
        # Create backup directory if not exists
        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        
        db_settings = settings.DATABASES['default']
        
        command = [
            MYSQLDUMP_PATH,
            f"--user={db_settings['USER']}",
            f"--password={db_settings['PASSWORD']}",
            f"--host={db_settings['HOST']}",
            f"--port={db_settings.get('PORT', '3306')}",
            db_settings['NAME'],
            f"--result-file={backup_path}"
        ]
        
        try:
            # Set the PATH environment variable temporarily
            env = os.environ.copy()
            env['PATH'] = f"{MARIADB_BIN_PATH};{env['PATH']}"
            
            result = subprocess.run(
                command,
                check=True,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(
                    result.returncode, 
                    command, 
                    result.stdout, 
                    result.stderr
                )
            
            file_size = os.path.getsize(backup_path)
            
            backup = BackupRecord.objects.create(
                backup_file=f'backups/{filename}',
                created_by=None,
                file_size=file_size,
                is_automated=False
            )
            
            return Response({
                'status': 'success',
                'backup_id': backup.id,
                'file_path': backup_path
            })
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Backup failed: {e.stderr}" if e.stderr else str(e)
            return Response(
                {'status': 'error', 'message': error_msg},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        backup = self.get_object()
        
        if not backup.backup_file:
            return Response(
                {"error": "Backup file not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            if not os.path.exists(backup.backup_file.path):
                return Response(
                    {"error": "File does not exist on server"},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            response = FileResponse(
                open(backup.backup_file.path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(backup.backup_file.path)
            )
            return response
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        try:
            backup = self.get_object()
            file_path = backup.backup_file.path
            
            if not os.path.exists(file_path):
                return Response(
                    {"error": f"Backup file not found at {file_path}"},
                    status=status.HTTP_404_NOT_FOUND
                )

            db_settings = settings.DATABASES['default']
            mysql_path = r"C:\Program Files\MariaDB 11.6\bin\mysql.exe"
            
            # Method 1: Using command list with shell=False (recommended)
            command = [
                mysql_path,
                f"--user={db_settings['USER']}",
                f"--password={db_settings['PASSWORD']}",
                f"--host={db_settings['HOST']}",
                db_settings['NAME'],
                f"--execute=source {file_path}"
            ]

            # Method 2: Alternative approach using file input
            # command = [
            #     mysql_path,
            #     f"--user={db_settings['USER']}",
            #     f"--password={db_settings['PASSWORD']}",
            #     f"--host={db_settings['HOST']}",
            #     db_settings['NAME']
            # ]

            try:
                # For Method 1:
                result = subprocess.run(
                    command,
                    shell=False,
                    check=True,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    text=True,
                    timeout=300  # 5 minute timeout
                )

                # For Method 2:
                # with open(file_path, 'r') as f:
                #     result = subprocess.run(
                #         command,
                #         stdin=f,
                #         stderr=subprocess.PIPE,
                #         stdout=subprocess.PIPE,
                #         text=True,
                #         timeout=300
                #     )

                return Response({
                    "status": "success",
                    "message": "Database restored successfully",
                    "output": result.stdout
                })

            except subprocess.TimeoutExpired:
                return Response({
                    "status": "error",
                    "message": "Restore timed out after 5 minutes"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            except subprocess.CalledProcessError as e:
                error_msg = e.stderr if e.stderr else "Unknown error occurred"
                return Response({
                    "status": "error",
                    "message": "Restore failed",
                    "error": error_msg,
                    "command": ' '.join(command),
                    "returncode": e.returncode
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except BackupRecord.DoesNotExist:
            return Response(
                {"error": "Backup record not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    




class SystemSettingViewSet(viewsets.ModelViewSet):
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [permissions.IsAdminUser]




class HealthMetricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer
    permission_classes = []
    
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
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ActivityLog
from .serializers import ActivityLogSerializer



class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all()
    permission_classes= []
    serializer_class = ActivityLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action', 'model', 'timestamp']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Handle user filtering safely
        user_id = self.request.query_params.get('user')
        if user_id:
            try:
                user_id = int(user_id)
                queryset = queryset.filter(user_id=user_id)
            except (ValueError, TypeError):
                pass  # Ignore invalid user IDs
                
        return queryset
from .models import User
from .serializers import UserSerializer





class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'logout':
            permission_classes = [permissions.AllowAny]  # No auth required
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            # log_activity(
            # action="login_failed",
            # model="user",
            # details={"email": email, "reason": "invalid_credentials"},
            # request=request
        # )
            return Response(
                {'error': 'Username or password is wrong'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        log_activity(
        user=user,
        action="login",
        model="user",
        details={"email": email},
        request=request
    )

        refresh = RefreshToken.for_user(user)
        response = Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

        # Set secure cookies
        response.set_cookie(
            'access_token',
            str(refresh.access_token),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=60 * 60  # 1 hour
        )
        response.set_cookie(
            'refresh_token',
            str(refresh),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=24 * 60 * 60  # 1 day
        )

        return response

    @action(detail=False, methods=['post'])
    def logout(self, request):
        response = Response(
            {'detail': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
        
        # Clear cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        # Blacklist refresh token if provided
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass
                
        return response

    @action(detail=False, methods=['get'])
    def me(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        return Response({'error': 'Not authenticated'}, status=401)