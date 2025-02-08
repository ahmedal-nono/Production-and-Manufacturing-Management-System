from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CustomUserViewSet, GroupViewSet, PermissionViewSet,CreateBackupView, ListBackupsView, RestoreBackupView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('backups/create/', CreateBackupView.as_view(), name='create-backup'),
    path('backups/list/', ListBackupsView.as_view(), name='list-backups'),
    path('backups/restore/', RestoreBackupView.as_view(), name='restore-backup'),
    
]
