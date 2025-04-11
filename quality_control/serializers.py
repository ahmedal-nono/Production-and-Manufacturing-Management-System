from rest_framework import serializers
from work_instructions.models import WorkOrder, JobCard
from workflow.models import ProductionOrder
from .models import Inspection, InspectionChecklist, ReworkRequest


class WorkOrderSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder
        fields = ['id', 'product_name', 'quantity', 'due_date', 'status']

    def get_status(self, obj):
        # Access through reverse relationship
        production_order = obj.productionorder_set.first()
        return production_order.status if production_order else None


class WorkOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = ['id', 'product_name', 'production_line']


class JobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = ['id', 'name']  # Update with actual fields


class InspectionChecklistSerializer(serializers.ModelSerializer):
    job_card = JobCardSerializer(read_only=True)

    class Meta:
        model = InspectionChecklist
        fields = ['id', 'job_card', 'state', 'note', 'photo']
        extra_kwargs = {'photo': {'required': False}}


class InspectionSerializer(serializers.ModelSerializer):
    checklist_items = InspectionChecklistSerializer(many=True, read_only=True)

    class Meta:
        model = Inspection
        fields = '__all__'

    def create(self, validated_data):
        inspection = super().create(validated_data)
        job_cards = JobCard.objects.filter(work_order=inspection.work_order)
        for job_card in job_cards:
            InspectionChecklist.objects.create(
                inspection=inspection, job_card=job_card)
        return inspection


class ReworkRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='inspection.work_order.product_name')
    workorder_id = serializers.IntegerField(source='inspection.work_order.id')
    defect_type = serializers.CharField(source='inspection.defect_type')
    severity = serializers.CharField(source='inspection.severity')
    description = serializers.CharField(source='inspection.description')
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        return [item.photo.url for item in obj.inspection.checklist_items.all() if item.photo]

    class Meta:
        model = ReworkRequest
        fields = ['id', 'status', 'product_name', 'workorder_id', 'defect_type',
                  'severity', 'description', 'photos', 'created_at']
