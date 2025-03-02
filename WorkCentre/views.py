from rest_framework import viewsets
from .models import WorkCenter, Workstation, Maintenance
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import WorkCenterSerializer, WorkstationSerializer, MaintenanceSerializer

class WorkCenterViewSet(viewsets.ModelViewSet):
    queryset = WorkCenter.objects.all()
    serializer_class = WorkCenterSerializer

class WorkstationViewSet(viewsets.ModelViewSet):
    queryset = Workstation.objects.all()
    serializer_class = WorkstationSerializer
    filter_backends = [DjangoFilterBackend]  # Enable filtering
    filterset_fields = ['work_center']  # Allow filtering by work_center

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer