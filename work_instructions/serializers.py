# serializers.py

from rest_framework import serializers
from .models import WorkOrder, JobCard, WorkInstruction
from workcentre.models import WorkCenter  # Assuming WorkCenter is in the workcentre app
from workflow.models import ProductionLine  # Assuming ProductionLine is in the workflow app


class WorkInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInstruction
        fields = ['id', 'title', 'task_steps', 'tools_required', 'materials_required', 'step_description', 'status']


class WorkOrderSerializer(serializers.ModelSerializer):
    work_instruction = serializers.PrimaryKeyRelatedField(queryset=WorkInstruction.objects.all())
    production_line = serializers.PrimaryKeyRelatedField(queryset=ProductionLine.objects.all(), required=False)
    
    class Meta:
        model = WorkOrder
        fields = ['id', 'name', 'quantity_required', 'due_date', 'priority', 'work_instruction', 'production_line']

    def create(self, validated_data):
        work_instruction_data = validated_data.pop('work_instruction')
        work_instruction = WorkInstruction.objects.create(**work_instruction_data)
        work_order = WorkOrder.objects.create(work_instruction=work_instruction, **validated_data)
        return work_order


class JobCardSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer()  # Nested WorkOrder serializer

    class Meta:
        model = JobCard
        fields = ['id', 'work_order', 'task_name', 'required_tools', 'required_materials', 'status', 'assigned_to']
