from rest_framework import serializers
from work_instructions.models import WorkOrder, JobCard
from .models import Inspection, InspectionChecklist, ReworkRequest


class JobCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCard
        fields = ['id', 'task_name', 'status', 'assigned_to']


class WorkOrderSerializer(serializers.ModelSerializer):
    production_line_name = serializers.SerializerMethodField()
    latest_decision = serializers.SerializerMethodField()

    class Meta:
        model = WorkOrder
        fields = ['id', 'name', 'quantity_required', 'due_date', 'priority',
                  'production_line', 'production_line_name', 'latest_decision']

    def get_production_line_name(self, obj):
        return obj.production_line.line_name if obj.production_line else None

    def get_latest_decision(self, obj):
        # Prefetched by the list view; fall back for detail/single-object use.
        inspections = getattr(obj, 'ordered_inspections', None)
        if inspections is not None:
            return inspections[0].final_decision if inspections else None
        inspection = obj.inspection_set.order_by('-updated_at').first()
        return inspection.final_decision if inspection else None


class WorkOrderDetailSerializer(serializers.ModelSerializer):
    production_line_name = serializers.SerializerMethodField()
    job_cards = JobCardSerializer(many=True, read_only=True)

    class Meta:
        model = WorkOrder
        fields = ['id', 'name', 'quantity_required', 'due_date', 'priority',
                  'production_line', 'production_line_name', 'job_cards']

    def get_production_line_name(self, obj):
        return obj.production_line.line_name if obj.production_line else None


class InspectionChecklistSerializer(serializers.ModelSerializer):
    job_card = JobCardSerializer(read_only=True)

    class Meta:
        model = InspectionChecklist
        fields = ['id', 'inspection', 'job_card', 'state', 'note', 'photo']
        read_only_fields = ['id', 'inspection']
        extra_kwargs = {'photo': {'required': False}}


class InspectionSerializer(serializers.ModelSerializer):
    checklist_items = InspectionChecklistSerializer(many=True, read_only=True)
    work_order_name = serializers.CharField(
        source='work_order.name', read_only=True)

    class Meta:
        model = Inspection
        fields = ['id', 'work_order', 'work_order_name', 'defect_type', 'severity',
                  'affected_component', 'description', 'final_decision',
                  'created_at', 'updated_at', 'checklist_items']

    def create(self, validated_data):
        inspection = super().create(validated_data)
        job_cards = JobCard.objects.filter(work_order=inspection.work_order)
        InspectionChecklist.objects.bulk_create([
            InspectionChecklist(inspection=inspection, job_card=job_card)
            for job_card in job_cards
        ])
        if inspection.final_decision == 'rework':
            ReworkRequest.objects.get_or_create(
                inspection=inspection, defaults={'status': 'pending'})
        return inspection


class ReworkRequestSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='inspection.work_order.name', read_only=True)
    workorder_id = serializers.IntegerField(
        source='inspection.work_order.id', read_only=True)
    defect_type = serializers.CharField(
        source='inspection.defect_type', read_only=True)
    severity = serializers.CharField(
        source='inspection.severity', read_only=True)
    affected_component = serializers.CharField(
        source='inspection.affected_component', read_only=True)
    description = serializers.CharField(
        source='inspection.description', read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, obj):
        return [item.photo.url
                for item in obj.inspection.checklist_items.all()
                if item.photo]

    class Meta:
        model = ReworkRequest
        fields = ['id', 'status', 'product_name', 'workorder_id', 'defect_type',
                  'severity', 'affected_component', 'description', 'photos',
                  'created_at', 'updated_at']
