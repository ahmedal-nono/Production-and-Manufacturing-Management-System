from datetime import timedelta
from rest_framework import serializers
from workcentre.models import Workstation
from .models import Issue, Report, ReportTemplate, ScheduledReport
from workflow.models import ProductionLine, ProductionOrder, Workflow, Stage
from workflow.serializers import ProductionOrderSerializer, WorkflowSerializer, StageSerializer

# Basic Model Serializers
class IssueListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'category', 'priority', 'affected_item', 'created_at']

class IssueDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'report_type', 'created_at']

class ReportDetailSerializer(serializers.ModelSerializer):
    production_line = serializers.SlugRelatedField(
        slug_field='line_name',
        queryset=ProductionLine.objects.all()
    )
    workstation = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Workstation.objects.all()
    )

    class Meta:
        model = Report
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = '__all__'

class ScheduledReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReport
        fields = '__all__'

class ProductionPerformanceReportSerializer(serializers.Serializer):
    production_line = serializers.CharField()
    total_orders = serializers.IntegerField(min_value=0)
    completed_orders = serializers.IntegerField(min_value=0)
    completion_rate = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=0, max_value=100)
    average_duration = serializers.DurationField(allow_null=True)
    delayed_orders = serializers.IntegerField(min_value=0)

    def validate(self, data):
        if data['completed_orders'] > data['total_orders']:
            raise serializers.ValidationError("Completed orders cannot exceed total orders")
        return data

class WorkflowAnalysisReportSerializer(serializers.Serializer):
    workflow = serializers.SerializerMethodField()
    total_stages = serializers.IntegerField(min_value=0)
    avg_stage_duration = serializers.IntegerField(min_value=0)
    total_inspection_points = serializers.IntegerField(min_value=0)
    longest_stage = serializers.SerializerMethodField()

    def get_workflow(self, obj):
        """Serialize the workflow object"""
        from workflow.serializers import WorkflowSerializer
        return WorkflowSerializer(obj['workflow']).data

    def get_longest_stage(self, obj):
        """Serialize the stage object"""
        from workflow.serializers import StageSerializer
        return StageSerializer(obj['longest_stage']).data if obj['longest_stage'] else None

class ProductionOrderStatusSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField(min_value=0)
    total_quantity = serializers.IntegerField(min_value=0)

    def to_representation(self, instance):
        """Handle direct conversion of queryset results"""
        return {
            'status': instance['status'],
            'count': instance['count'],
            'total_quantity': instance['total_quantity']
        }
class StageDurationSerializer(serializers.Serializer):
    workflow_name = serializers.CharField(source='workflow__name')
    stage_name = serializers.CharField(source='name')
    avg_duration_minutes = serializers.FloatField(source='avg_duration')
    min_duration_minutes = serializers.IntegerField(source='min_duration')
    max_duration_minutes = serializers.IntegerField(source='max_duration')
    
    # Add these if you really need seconds
    avg_duration_seconds = serializers.SerializerMethodField()
    min_duration_seconds = serializers.SerializerMethodField()
    max_duration_seconds = serializers.SerializerMethodField()
    
    def get_avg_duration_seconds(self, obj):
        return obj['avg_duration'] * 60 if obj['avg_duration'] else 0
    
    def get_min_duration_seconds(self, obj):
        return obj['min_duration'] * 60
    
    def get_max_duration_seconds(self, obj):
        return obj['max_duration'] * 60