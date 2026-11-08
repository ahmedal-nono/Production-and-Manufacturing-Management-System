from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from work_instructions.models import WorkOrder
from administration.permissions import RoleWritePermission
from .models import Inspection, InspectionChecklist, ReworkRequest
from .serializers import *

QUALITY_ROLES = (
    'admin',
    'production_manager',
    'quality_control_manager',
    'quality_control_inspector',
    'operator',
)


class WorkOrderListView(generics.ListAPIView):
    queryset = WorkOrder.objects.select_related('production_line').prefetch_related(
        Prefetch(
            'inspection_set',
            queryset=Inspection.objects.order_by('-updated_at'),
            to_attr='ordered_inspections',
        )
    )
    serializer_class = WorkOrderSerializer
    permission_classes = [IsAuthenticated]


class WorkOrderDetailView(generics.RetrieveAPIView):
    queryset = WorkOrder.objects.select_related('production_line').prefetch_related(
        'job_cards',
        'job_cards__assigned_to',
    )
    serializer_class = WorkOrderDetailSerializer
    permission_classes = [IsAuthenticated]


class InspectionCreateView(generics.CreateAPIView):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [RoleWritePermission]
    required_roles = QUALITY_ROLES


class InspectionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Inspection.objects.select_related('work_order').prefetch_related(
        'checklist_items',
        'checklist_items__job_card',
    )
    serializer_class = InspectionSerializer
    permission_classes = [RoleWritePermission]
    required_roles = QUALITY_ROLES

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.final_decision == 'rework' and not hasattr(instance, 'rework_request'):
            ReworkRequest.objects.create(inspection=instance, status='pending')


class InspectionChecklistUpdateView(generics.UpdateAPIView):
    queryset = InspectionChecklist.objects.all()
    serializer_class = InspectionChecklistSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [RoleWritePermission]
    required_roles = QUALITY_ROLES


class ReworkRequestListView(generics.ListAPIView):
    queryset = ReworkRequest.objects.select_related(
        'inspection', 'inspection__work_order'
    ).prefetch_related('inspection__checklist_items')
    serializer_class = ReworkRequestSerializer
    permission_classes = [IsAuthenticated]


class ReworkRequestUpdateView(generics.UpdateAPIView):
    queryset = ReworkRequest.objects.select_related(
        'inspection', 'inspection__work_order'
    ).prefetch_related('inspection__checklist_items')
    serializer_class = ReworkRequestSerializer
    fields = ['status']
    permission_classes = [RoleWritePermission]
    required_roles = QUALITY_ROLES
