# administration/views.py
import psutil
import time
from django.shortcuts import get_object_or_404
from .utils import log_activity
from datetime import timedelta
from django.db.models import Avg
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import FileResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth import logout, authenticate
from django.utils import timezone
import os
import os
import subprocess
from pathlib import Path
from .permissions import IsProductionManager, IsSameUserOrManager, IsAdminRole
from datetime import datetime
import subprocess
from .models import BackupConfig, BackupRecord, Department, SystemSetting, HealthMetric, Role, UserProfile, RumMetric, BackgroundJob
from django.contrib.auth.models import User
from .serializers import BackupConfigSerializer, BackupRecordSerializer, DepartmentSerializer, SystemSettingSerializer, HealthMetricSerializer, RoleSerializer, UserSerializer, LoginSerializer, UserProfileSerializer, PasswordChangeSerializer, RumMetricSerializer, BackgroundJobSerializer
from .jobs import enqueue, run_job

class BackupConfigViewSet(viewsets.ModelViewSet):
    queryset = BackupConfig.objects.all()
    serializer_class = BackupConfigSerializer
    permission_classes = [IsAdminRole]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminRole]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminRole]
MARIADB_BIN_PATH = r"C:\Program Files\MariaDB 11.6\bin"
MYSQLDUMP_PATH = os.path.join(MARIADB_BIN_PATH, "mysqldump.exe")
class BackupRecordViewSet(viewsets.ModelViewSet):
    serializer_class = BackupRecordSerializer
    queryset = BackupRecord.objects.all()
    permission_classes = [IsAdminRole]
    @action(detail=False, methods=['post'])
    def enqueue_backup(self, request):
        """Queue a backup instead of blocking the request.

        Returns 202 with the job payload; the client polls
        ``/api/admin/jobs/<id>/`` until ``status`` is terminal.
        """
        job = enqueue(
            'backup.create',
            {'automated': False, 'created_by_id': request.user.id},
            user=request.user,
        )
        if settings.BACKGROUND_JOBS_EAGER:
            job = run_job(job)
        return Response(
            BackgroundJobSerializer(job).data,
            status=status.HTTP_202_ACCEPTED,
        )

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
    permission_classes = [IsAdminRole]




class HealthMetricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HealthMetric.objects.all()
    serializer_class = HealthMetricSerializer
    permission_classes = [IsAdminRole]
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        # Non-blocking: return usage since the previous call instead of
        # freezing the worker for a full second on every dashboard load.
        cpu_usage = psutil.cpu_percent(interval=None)
        
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



class ActivityLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.select_related('user').all()
    permission_classes= [IsAdminRole]
    serializer_class = ActivityLogSerializer
    pagination_class = ActivityLogPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['action', 'model', 'timestamp']
    search_fields = [
        'user__full_name', 'user__email', 'action', 'model',
        'object_id', 'ip_address',
    ]

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


from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'is_read']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not (user.is_superuser or (user.role and user.role.name == 'admin')):
            queryset = queryset.filter(user=user)
        user_id = self.request.query_params.get('user')
        if user_id:
            try:
                queryset = queryset.filter(user_id=int(user_id))
            except (ValueError, TypeError):
                pass
        return queryset


from .models import User
from .serializers import UserSerializer


def _percentile(values, ratio):
    """Nearest-rank percentile; returns 0 for an empty sample."""
    if not values:
        return 0
    ordered = sorted(values)
    index = int(round(ratio * (len(ordered) - 1)))
    return ordered[min(len(ordered) - 1, max(0, index))]


class RumMetricViewSet(viewsets.ModelViewSet):
    """Capture browser performance samples and expose them to admins.

    ``POST`` is open (the browser beacon has no credentials) while listing and
    aggregation are restricted to admins.
    """

    queryset = RumMetric.objects.all()
    serializer_class = RumMetricSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    # (good, poor) thresholds per Core Web Vital.
    THRESHOLDS = {
        'LCP': (2500, 4000),
        'CLS': (0.1, 0.25),
        'INP': (200, 500),
        'FCP': (1800, 3000),
        'TTFB': (800, 1800),
    }

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminRole()]

    def create(self, request, *args, **kwargs):
        payload = request.data
        if isinstance(payload, dict) and 'metrics' in payload:
            payload = payload['metrics']
        items = payload if isinstance(payload, list) else [payload]
        items = [item for item in items if isinstance(item, dict)]
        serializer = self.get_serializer(data=items, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'received': len(serializer.validated_data)},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Aggregate samples into p75/p95 per metric and top pages.

        ``?days=7`` bounds the window (1-90 days). Percentiles are computed on
        the raw samples of that window; the most recent 20k rows are used so a
        busy install cannot make this endpoint expensive.
        """
        try:
            days = int(request.query_params.get('days', 7))
        except (TypeError, ValueError):
            days = 7
        days = max(1, min(days, 90))
        since = timezone.now() - timedelta(days=days)

        rows = list(
            RumMetric.objects.filter(created_at__gte=since)
            .values('name', 'value', 'page_path')[:20000]
        )

        values_by_name = {}
        values_by_page = {}
        for row in rows:
            values_by_name.setdefault(row['name'], []).append(row['value'])
            page = values_by_page.setdefault(
                row['page_path'], {'count': 0, 'metrics': {}})
            page['count'] += 1
            page['metrics'].setdefault(row['name'], []).append(row['value'])

        metrics = []
        for name, (good, poor) in self.THRESHOLDS.items():
            values = values_by_name.get(name, [])
            metrics.append({
                'name': name,
                'count': len(values),
                'median': round(_percentile(values, 0.50), 2),
                'p75': round(_percentile(values, 0.75), 2),
                'p95': round(_percentile(values, 0.95), 2),
                'average': round(sum(values) / len(values), 2) if values else 0,
                'ratings': {
                    'good': sum(1 for value in values if value <= good),
                    'needs_improvement': sum(
                        1 for value in values if good < value <= poor),
                    'poor': sum(1 for value in values if value > poor),
                },
            })

        pages = []
        for path, bucket in sorted(
                values_by_page.items(),
                key=lambda item: item[1]['count'], reverse=True)[:10]:
            pages.append({
                'page_path': path,
                'count': bucket['count'],
                'lcp_p75': self._page_percentile(bucket, 'LCP', 2),
                'cls_p75': self._page_percentile(bucket, 'CLS', 3),
                'inp_p75': self._page_percentile(bucket, 'INP', 2),
            })

        return Response({
            'window_days': days,
            'sample_count': len(rows),
            'metrics': metrics,
            'pages': pages,
            'thresholds': {
                name: {'good': good, 'poor': poor}
                for name, (good, poor) in self.THRESHOLDS.items()
            },
        })

    @staticmethod
    def _page_percentile(bucket, metric, digits):
        """p75 for one metric on a page, or ``None`` when it has no samples."""
        values = bucket['metrics'].get(metric)
        if not values:
            return None
        return round(_percentile(values, 0.75), digits)


class BackgroundJobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BackgroundJob.objects.all()
    serializer_class = BackgroundJobSerializer
    permission_classes = [IsAdminRole]




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related('department', 'role').all()
    serializer_class = UserSerializer
    

    def get_permissions(self):
        if self.action in ['login', 'logout']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'me':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminRole]
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


def _can_manage_user(request, user_id):
    return (request.user.is_superuser or
            (request.user.role and request.user.role.name == 'admin') or
            request.user.id == user_id)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request, user_id):
    if not _can_manage_user(request, user_id):
        return Response({'error': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(User, id=user_id)  # Get user by ID
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request, user_id):
    if not _can_manage_user(request, user_id):
        return Response({'error': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
    user = get_object_or_404(User, id=user_id)
    serializer = PasswordChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    return Response({"status": "password changed"})