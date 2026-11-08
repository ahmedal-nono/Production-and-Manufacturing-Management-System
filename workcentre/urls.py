from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkCenterViewSet, WorkstationViewSet, MaintenanceViewSet

router = DefaultRouter()
router.register(r'workcenters', WorkCenterViewSet)
router.register(r'workstations', WorkstationViewSet)
router.register(r'maintenances', MaintenanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]