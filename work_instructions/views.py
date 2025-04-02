# views.py

from rest_framework import viewsets
from rest_framework.response import Response
from .models import WorkOrder, JobCard, WorkInstruction
from .serializers import WorkOrderSerializer, JobCardSerializer, WorkInstructionSerializer
from rest_framework.decorators import action

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    @action(detail=True, methods=['post'])
    def generate_job_cards(self, request, pk=None):
        work_order = self.get_object()
        work_instruction = work_order.work_instruction
        
        # Generate job cards for each task in the work instruction
        for task in work_instruction.task_steps.split('\n'):
            JobCard.objects.create(
                work_order=work_order,
                task_name=task,
                required_tools=work_instruction.tools_required,
                required_materials=work_instruction.materials_required,
                status='Not Started',
                assigned_to=work_order.production_line.assigned_work_center,
                step_description=work_instruction.step_description
            )

        return Response({"message": "Job cards generated successfully"})

class JobCardViewSet(viewsets.ModelViewSet):
    queryset = JobCard.objects.all()
    serializer_class = JobCardSerializer

    def get_queryset(self):
        work_order_id = self.request.query_params.get('work_order_id')
        if work_order_id:
            return JobCard.objects.filter(work_order_id=work_order_id)
        return JobCard.objects.all()

class WorkInstructionViewSet(viewsets.ModelViewSet):
    queryset = WorkInstruction.objects.all()
    serializer_class = WorkInstructionSerializer
