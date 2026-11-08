from rest_framework import serializers
from .models import WorkOrder, JobCard, WorkInstruction
from workcentre.models import WorkCenter  # Assuming WorkCenter is in the workcentre app
from workflow.models import ProductionLine, ProductionOrder  # Assuming ProductionLine is in the workflow app


class WorkInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInstruction
        fields = ['id', 'title', 'task_steps', 'tools_required', 'materials_required', 'step_description', 'status']


class WorkOrderSerializer(serializers.ModelSerializer):
    work_instruction = serializers.PrimaryKeyRelatedField(queryset=WorkInstruction.objects.all())
    production_line = serializers.PrimaryKeyRelatedField(queryset=ProductionLine.objects.all(), required=False)
    production_order = serializers.PrimaryKeyRelatedField(
        queryset=ProductionOrder.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = WorkOrder
        fields = ['id', 'name', 'quantity_required', 'due_date', 'priority', 'work_instruction', 'production_line', 'production_order']
    def create(self, validated_data):
        work_order = super().create(validated_data)
        work_instruction = work_order.work_instruction

        # Get the assigned work center (simplest working version)
        assigned_to = None
        if work_order.production_line and work_order.production_line.work_centers.exists():
            assigned_to = WorkCenter.objects.get(pk=work_order.production_line.work_centers.first().pk)

        # Create job cards
        if work_instruction.task_steps:
            JobCard.objects.bulk_create([
                JobCard(
                    work_order=work_order,
                    task_name=task.strip(),
                    required_tools=work_instruction.tools_required,
                    required_materials=work_instruction.materials_required,
                    status='Not Started',
                    assigned_to=assigned_to
                )
                for task in work_instruction.task_steps.split('\n')
                if task.strip()
            ])

        return work_order
    




class JobCardSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer()  # Nested WorkOrder serializer

    class Meta:
        model = JobCard
        fields = ['id', 'work_order', 'task_name', 'required_tools', 'required_materials', 'status', 'assigned_to']
