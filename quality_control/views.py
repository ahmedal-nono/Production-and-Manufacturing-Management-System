from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from work_instructions.models import WorkOrder
from .models import Inspection, InspectionChecklist, ReworkRequest
from .serializers import *


class WorkOrderListView(generics.ListAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer


class WorkOrderDetailView(generics.RetrieveAPIView):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderDetailSerializer


class InspectionCreateView(generics.CreateAPIView):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer


class InspectionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.final_decision == 'rework' and not hasattr(instance, 'rework_request'):
            ReworkRequest.objects.create(inspection=instance, status='pending')


class InspectionChecklistUpdateView(generics.UpdateAPIView):
    queryset = InspectionChecklist.objects.all()
    serializer_class = InspectionChecklistSerializer
    parser_classes = (MultiPartParser, FormParser)


class ReworkRequestListView(generics.ListAPIView):
    queryset = ReworkRequest.objects.all()
    serializer_class = ReworkRequestSerializer


class ReworkRequestUpdateView(generics.UpdateAPIView):
    queryset = ReworkRequest.objects.all()
    serializer_class = ReworkRequestSerializer
    fields = ['status']
