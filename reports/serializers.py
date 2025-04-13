from rest_framework import serializers
from .models import Issue, Report
from workflow.models import ProductionLine
from workcentre.models import Workstation


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
            raise serializers.ValidationError(
                "End date must be after start date.")
        return data
