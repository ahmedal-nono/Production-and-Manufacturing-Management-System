
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from administration import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'backup-configs', views.BackupConfigViewSet)
router.register(r'backups', views.BackupRecordViewSet)
router.register(r'settings', views.SystemSettingViewSet)
router.register(r'health-metrics', views.HealthMetricViewSet)
router.register(r'activity-logs', views.ActivityLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/admin/', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ...
]
