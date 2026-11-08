# views.py

from rest_framework import viewsets
from rest_framework.response import Response
from .models import WorkOrder, JobCard, WorkInstruction
from .serializers import WorkOrderSerializer, JobCardSerializer, WorkInstructionSerializer
from rest_framework.decorators import action
from administration.permissions import RoleWritePermission

WORKORDER_ROLES = ('admin', 'production_manager')


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [RoleWritePermission]
    required_roles = WORKORDER_ROLES

    def get_queryset(self):
        queryset = super().get_queryset()
        po_id = self.request.query_params.get('production_order')
        if po_id:
            try:
                queryset = queryset.filter(production_order_id=int(po_id))
            except (ValueError, TypeError):
                pass
        return queryset

    @action(detail=True, methods=['post'])
    def generate_job_cards(self, request, pk=None):
        work_order = self.get_object()
        work_instruction = work_order.work_instruction

        assigned_to = None
        line = work_order.production_line
        if line:
            assigned_to = line.work_centers.first()

        steps = [step.strip()
                 for step in work_instruction.task_steps.split('\n')
                 if step.strip()]

        created = 0
        for task in steps:
            _, was_created = JobCard.objects.get_or_create(
                work_order=work_order,
                task_name=task,
                defaults={
                    'required_tools': work_instruction.tools_required,
                    'required_materials': work_instruction.materials_required,
                    'status': 'Not Started',
                    'assigned_to': assigned_to,
                },
            )
            if was_created:
                created += 1

        return Response({
            "message": "Job cards generated successfully",
            "created": created,
            "total": JobCard.objects.filter(work_order=work_order).count(),
        })

class JobCardViewSet(viewsets.ModelViewSet):
    queryset = JobCard.objects.all()
    serializer_class = JobCardSerializer
    permission_classes = [RoleWritePermission]
    required_roles = WORKORDER_ROLES

    def get_queryset(self):
        work_order_id = self.request.query_params.get('work_order_id')
        if work_order_id:
            return JobCard.objects.filter(work_order_id=work_order_id)
        return JobCard.objects.all()

class WorkInstructionViewSet(viewsets.ModelViewSet):
    queryset = WorkInstruction.objects.all()
    serializer_class = WorkInstructionSerializer
    permission_classes = [RoleWritePermission]
    required_roles = WORKORDER_ROLES
